import azure.functions as func
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.mgmt.storage import StorageManagementClient
from azure.core.exceptions import AzureError
import datetime
import os

def main(timer: func.TimerRequest) -> None:
    logging.info('Python timer trigger function executed.')

    try:
        subscription_id = os.environ["SUBSCRIPTION_ID"]
        resource_group_name = os.environ["RESOURCE_GROUP_NAME"]
        storage_account_name = os.environ["STORAGE_ACCOUNT_NAME"]
        key_vault_name = os.environ["KEY_VAULT_NAME"]
        secret_name = os.environ["FILE_SHARE_NAME"]
    except KeyError as e:
        logging.error(f"Missing environment variable: {str(e)}")
        return

    credential = DefaultAzureCredential()

    try:
       
        storage_client = StorageManagementClient(credential, subscription_id)
        regenerate_key = storage_client.storage_accounts.regenerate_key(
            resource_group_name,
            storage_account_name,
            {"key_name": "key1"}
        )

        new_key = regenerate_key.keys[0].value
        key_vault_url = f"https://{key_vault_name}.vault.azure.net/"
        
        secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
        secret_client.set_secret(secret_name, new_key)

        logging.info(f"Access key regenerated and updated in Key Vault for {storage_account_name}")
    except AzureError as e:
        logging.error(f"An Azure error occurred: {str(e)}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

app = func.FunctionApp()

@app.function_name(name="RotateStorageKey")
@app.schedule(schedule="0 0 1,9 * *", arg_name="timer", run_on_startup=True)
def rotate_storage_key(timer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    if timer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    main(timer)
