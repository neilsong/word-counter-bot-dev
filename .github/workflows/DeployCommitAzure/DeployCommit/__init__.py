import logging
import os, json

import azure.functions as func
from azure.identity import ManagedIdentityCredential
from azure.mgmt.compute import ComputeManagementClient


async def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    The main entry point to the function.
    """

    credentials = ManagedIdentityCredential()

    subscription_id = os.environ.get(
        "AZURE_SUBSCRIPTION_ID", "11111111-1111-1111-1111-111111111111"
    )

    response = await runcommand(credentials, subscription_id)

    return func.HttpResponse(response, mimetype="application/json")


async def runcommand(credentials, subscription_id):
    """
    Run Deploy Commit Command on VM1
    """

    run_command_parameters = {
        "command_id": "RunShellScript",
        "script": [
            "cd /home/azureuser/word-counter-bot-dev",
            "git pull",
            "screen -d -m /home/azureuser/word-counter-bot-dev/.github/workflows/execution.sh",
        ],
    }
    cm_client = ComputeManagementClient(credentials, subscription_id)

    command = cm_client.virtual_machines.begin_run_command(
        "VM1_group", "VM1", run_command_parameters
    )
    result = command.result()
    return json.dumps(result.value[0].message)
