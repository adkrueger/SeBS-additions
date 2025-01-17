import uuid
from typing import List

from azure.storage.blob import BlobServiceClient

from sebs.cache import Cache
from ..faas.storage import PersistentStorage


class BlobStorage(PersistentStorage):
    @staticmethod
    def typename() -> str:
        return "Azure.BlobStorage"

    @staticmethod
    def deployment_name():
        return "azure"

    def __init__(self, region: str, cache_client: Cache, conn_string: str, replace_existing: bool):
        super().__init__(region, cache_client, replace_existing)
        self.client = BlobServiceClient.from_connection_string(conn_string)

    """
        Internal implementation of creating a new container.
    """

    def _create_bucket(self, name: str, containers: List[str] = []) -> str:
        for c in containers:
            if name in c:
                self.logging.info("Container {} for {} already exists, skipping.".format(c, name))
                return c
        random_name = str(uuid.uuid4())[0:16]
        name = "{}-{}".format(name, random_name)
        self.client.create_container(name)
        self.logging.info("Created container {}".format(name))
        return name

    """
        Azure does not allow dots in container names.
    """

    def correct_name(self, name: str) -> str:
        return name.replace(".", "-")

    def list_buckets(self, bucket_name: str) -> List[str]:
        return [
            container["name"]
            for container in self.client.list_containers(name_starts_with=bucket_name)
        ]

    def uploader_func(self, container_idx, file, filepath):
        # Skip upload when using cached containers
        if self.cached and not self.replace_existing:
            return
        container_name = self.input_buckets[container_idx]
        if not self.replace_existing:
            for f in self.input_buckets_files[container_idx]:
                if f == file:
                    self.logging.info(
                        "Skipping upload of {} to {}".format(filepath, container_name)
                    )
                    return
        client = self.client.get_blob_client(container_name, file)
        with open(filepath, "rb") as file_data:
            client.upload_blob(data=file_data, overwrite=True)
        self.logging.info("Upload {} to {}".format(filepath, container_name))

    """
        Download file from bucket.

        :param container_name:
        :param file:
        :param filepath:
    """

    def download(self, container_name: str, key: str, filepath: str):
        self.logging.info("Download {}:{} to {}".format(container_name, key, filepath))
        client = self.client.get_blob_client(container_name, key)
        with open(filepath, "wb") as download_file:
            download_file.write(client.download_blob().readall())

    def upload(self, container_name: str, filepath: str, key: str):
        self.logging.info("Upload {} to {}".format(filepath, container_name))
        client = self.client.get_blob_client(container_name, key)
        with open(filepath, "rb") as upload_file:
            client.upload_blob(upload_file.read())

    """
        Return list of files in a container.

        :param container:
        :return: list of file names. empty if container empty
    """

    def list_bucket(self, container: str):
        objects = list(
            map(
                lambda x: x["name"],
                self.client.get_container_client(container).list_blobs(),
            )
        )
        return objects

    def clean_bucket(self, bucket: str):
        self.logging.info("Clean output container {}".format(bucket))
        container_client = self.client.get_container_client(bucket)
        blobs = list(map(lambda x: x["name"], container_client.list_blobs()))
        if len(blobs) > 0:
            container_client.delete_blobs(*blobs)
