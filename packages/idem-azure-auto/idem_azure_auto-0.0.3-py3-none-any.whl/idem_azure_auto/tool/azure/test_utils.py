import asyncio
import sys


def __virtual__(hub):
    if "pytest" in sys.modules:
        return True
    else:
        return False, "Not running in test environment"


async def wait_for_resource_to_present(
    hub, ctx, url: str, retry_count: int, retry_period: int, retry_policy: list = [404]
):
    """
    Wait for a resource until its provisionState reaches "Succeed". This function is helpful to sequentially provision
    resources that depend on each other.
    :param hub: The redistributed pop central hub. This is required in Idem, so while not used, must appear.
    :param ctx: Idem ctx.
    :param url: The full url to get the resource from Azure.
    :param retry_count: The maximum number of retries to do.
    :param retry_period: The waiting time between each retry.
    :param retry_policy: A list of HTTP status code on which a retry should happen.
    """
    count = 0
    while count < retry_count:
        response_get = await hub.exec.request.json.get(
            ctx,
            url=url,
            success_codes=[200, 201, 204],
            headers=ctx.acct.headers,
        )
        if response_get["result"]:
            ret = response_get["ret"]
            if "properties" in ret and "provisioningState" in ret.get("properties"):
                if ret.get("properties").get("provisioningState") == "Succeeded":
                    return response_get
            else:
                count += 1
                hub.log.info(f"{count}/{retry_count} Wait for resource with url {url}")
                await asyncio.sleep(retry_period)
        elif response_get["status"] in retry_policy:
            count += 1
            hub.log.info(f"{count}/{retry_count} Wait for resource with url {url}")
            await asyncio.sleep(retry_period)
        else:
            raise RuntimeError(
                f"Getting resource with url {url} failed with status {response_get['status']}"
                f" and error: {response_get['ret']}"
            )
    raise RuntimeError(
        f"Resource with url {url} did not reach 'Succeeded' state within time limit."
    )


async def wait_for_resource_to_absent(
    hub,
    ctx,
    url: str,
    retry_count: int,
    retry_period: int,
    retry_policy: list = [200, 201, 204],
):
    """
    Wait for a resource until it's absent (GET operation returns 404).
    :param hub: The redistributed pop central hub. This is required in Idem, so while not used, must appear.
    :param ctx: Idem ctx.
    :param url: The full url to get the resource from Azure.
    :param retry_count: The maximum number of retries to do.
    :param retry_period: The waiting time between each retry.
    :param retry_policy: A list of HTTP status code on which a retry should happen.
    """
    count = 0
    while count < retry_count:
        response_get = await hub.exec.request.json.get(
            ctx,
            url=url,
            success_codes=[200, 201, 204],
            headers=ctx.acct.headers,
        )
        if response_get["result"]:
            count += 1
            hub.log.info(
                f"{count}/{retry_count} Wait for resource with url {url} to be deleted"
            )
            await asyncio.sleep(retry_period)
        elif response_get["status"] in retry_policy:
            count += 1
            hub.log.info(
                f"{count}/{retry_count} Wait for resource with url {url} to be deleted"
            )
            await asyncio.sleep(retry_period)
        elif response_get["status"] == 404:
            return
        else:
            raise RuntimeError(
                f"Getting resource with url {url} failed with status {response_get['status']}"
                f" and error: {response_get['ret']}"
            )
    raise RuntimeError(
        f"Resource with url {url} did not get deleted within time limit."
    )


def check_response_payload(hub, expected_payload: dict, actual_payload: dict):
    """
    Check if a response payload machines the expected payload.
    """
    assert expected_payload is not None
    assert actual_payload is not None
    for parameter_key, parameter_fields in expected_payload.items():
        assert (
            parameter_key in actual_payload
        ), f"{parameter_key} is not in {actual_payload}"
        if isinstance(parameter_fields, str):
            assert parameter_fields == actual_payload.get(
                parameter_key
            ), f"{parameter_fields} is not {actual_payload.get(parameter_key)}"
        elif isinstance(parameter_fields, list):
            for parameter_field in parameter_fields:
                if isinstance(parameter_field, str):
                    assert parameter_field in actual_payload.get(
                        parameter_key
                    ), f"{parameter_fields} is not in {actual_payload.get(parameter_key)}"
                else:
                    # Only support comparing a list of strings.
                    continue
        elif isinstance(parameter_fields, dict):
            check_response_payload(
                hub, parameter_fields, actual_payload.get(parameter_key)
            )
        else:
            # Skip any other type of fields that this function doesn't support
            continue
