import os
import cmd
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

keyVaultName = 'oceans-keyvault-dld-sb'
KVUri = f"https://{keyVaultName}.vault.azure.net"

#credential = DefaultAzureCredential()
credential = DefaultAzureCredential(ExcludeVisualStudioCodeCredential = False);
client = SecretClient(vault_url=KVUri, credential=credential)


print(f"Retrieving your secret from {keyVaultName}.")
secretName = 'dataloadsql'
retrieved_secret = client.get_secret(secretName)

print(f"Your secret is '{retrieved_secret.value}'.")
print(f"Deleting your secret from {keyVaultName} ...")

