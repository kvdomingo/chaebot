from google.cloud import secretmanager


def get_secret_string(name: str, version="latest"):
    secret_id = f"projects/my-projects-306716/secrets/KVISUALBOT_{name}/versions/{version}"
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": secret_id})
    return response.payload.data.decode()
