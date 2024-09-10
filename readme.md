# Azure Function: Renew Storage Account Secrets and Update Key Vault

## Descripción

Esta Azure Function se encarga de renovar un secreto de una cuenta de almacenamiento de Azure y actualizar estos secretos en un Azure Key Vault a intervalos regulares. Esto garantiza que los secretos de la cuenta de almacenamiento se mantengan actualizados y seguros.

## Roles de IAM Azure Function

    Key Vault Secrets Officer
    Storage Account Key Operator Service Role



## Características

- **Renueva secretos**: Obtiene y renueva los secretos de una cuenta de almacenamiento de Azure.
- **Actualiza Key Vault**: Actualiza los secretos renovados en un Azure Key Vault.
- **Programación periódica**: Utiliza un desencadenador basado en un temporizador para ejecutar el proceso a intervalos regulares.

## Requisitos Previos

- **Cuenta de Almacenamiento de Azure**: Debes tener una cuenta de almacenamiento para la cual deseas renovar los secretos.
- **Azure Key Vault**: Debes tener un Key Vault en el que se almacenarán los secretos renovados.
- **Azure Functions**: La función debe estar configurada en tu suscripción de Azure.
- **Permisos**: Asegúrate de que la función tenga permisos adecuados para acceder a la cuenta de almacenamiento y al Key Vault.

### Instalación de Dependencias

1. **Instalar Azure Functions Core Tools**:
   ```bash
    npm install -g azure-functions-core-tools@4 --unsafe-perm true
   ```
2. **Instalar y configurar dependencias internas**:
    ```bash
        python -m venv .venv
        source .venv/bin/activate  # En Windows usa .venv\Scripts\activate
        pip install -r requirements.txt   
    ```
3. **Archivo de configuracion: (local.settings.json)**
    ```bash
    {
    "IsEncrypted": false,
    "Values": {
        "FUNCTIONS_WORKER_RUNTIME": "python",
        "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
        "AzureWebJobsStorage": "UseDevelopmentStorage=true",
        "SUBSCRIPTION_ID": "",
        "RESOURCE_GROUP_NAME": "",
        "STORAGE_ACCOUNT_NAME": "",
        "KEY_VAULT_NAME": "",
        "FILE_SHARE_NAME": ""
    }
    }
    ```
4. **Ejecutar la Azure Function**
    ```bash
    func start
    ```
5. **Validar el resultado:**
    ir al recurso de azure key vault y validar que la ultima version del secret que se actualizo coincida con la hora en la que ejecutaste la funcion. 