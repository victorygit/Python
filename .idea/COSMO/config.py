import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://oceanis-cosmo-test.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'jkgrgOb6UrrlOPDkZSrrAyZuy5sPadzejXGiIIwWbk5a3nlsCDKZ0PiPWQxLDuUzyKLzpDm4Qc4QACDbhTLpzQ=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'Employee'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'Items'),
}