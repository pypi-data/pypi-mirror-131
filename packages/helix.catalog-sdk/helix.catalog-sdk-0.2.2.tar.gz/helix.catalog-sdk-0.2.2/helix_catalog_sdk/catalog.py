import json
import boto3
import os
from datetime import datetime, timedelta
from types import SimpleNamespace
from typing import List, Optional, Tuple, Dict

from helix_catalog_sdk.data_source import DataSource, ResourceItem

from helix_catalog_sdk.enums import HelixEnvironment
from helix_catalog_sdk.repo import BaseRepo


class Catalog:
    def __init__(
        self,
        repo: BaseRepo,
        environment: HelixEnvironment = HelixEnvironment.PRODUCTION,
    ):
        self._repo = repo
        self.environment = environment
        self._last_updated_data_source_dttm: datetime = datetime.utcnow() + timedelta(
            days=-1
        )
        self._all_data_sources: List[Tuple[str, DataSource]] = []
        self._all_data_sources = self.get_all_data_sources()

    def get_data_source(
        self, data_source: str, environment: HelixEnvironment
    ) -> Optional[DataSource]:
        print(
            f"Data Catalog is reading data source: {data_source} for environment {environment}"
        )
        decoded_contents = self._repo.read_file(data_source)
        contents: SimpleNamespace = json.loads(
            decoded_contents, object_hook=lambda d: SimpleNamespace(**d)
        )

        # Currently only data_sources of type "file" are working in the catalog.
        if getattr(contents, "connection_type", None) != "file":
            return None

        return DataSource(data_source, contents, environment)

    def update_data_source_resource(self, file_path: str) -> Optional[DataSource]:
        for data_source_path, data_source in self._all_data_sources:
            if data_source.matches_path(file_path):
                data_source.update_path_with_latest_file(file_path)
                self.update_data_source(data_source_path, data_source.to_json())
                return data_source
        return None

    def update_resource_last_processed(
        self,
        resource_name: str,
        last_processed_value: str,
        data_source: DataSource,
        environment: HelixEnvironment,
    ) -> None:
        for resource in data_source.resources:
            if resource_name == resource.name and resource.last_processed is not None:
                resource.last_processed.set_last_processed(
                    last_processed_value, environment
                )
                self.update_data_source(data_source.name, data_source.to_json())

    def update_data_source(self, data_source_name: str, updated_contents: str) -> None:
        self._repo.update_file(data_source_name, updated_contents)

    def get_resource_unprocessed_directories(
        self, resource_name: str, data_source: DataSource, environment: HelixEnvironment
    ) -> List[str]:
        paths_to_process: Dict[datetime, str] = {}
        sorted_paths_to_process = []
        resource: ResourceItem = [
            r for r in data_source.resources if r.name == resource_name
        ][0]
        if resource.last_processed:
            date_segment = resource.date_segment if resource.date_segment else 0

            date_format = resource.date_format if resource.date_format else "%Y-%m-%d"
            last_processed = resource.last_processed.get_last_processed(environment)
            all_paths = self.get_all_directories(resource, last_processed)
            path_parts = list(
                filter(None, last_processed.replace("s3:/", "").split("/"))
            )

            if isinstance(date_segment, int):
                last_processed_date = datetime.strptime(
                    path_parts[date_segment], date_format
                )
            if isinstance(date_segment, list):
                last_processed_date_str = ""
                for segment in date_segment:
                    last_processed_date_str = (
                        last_processed_date_str + path_parts[segment]
                    )
                last_processed_date = datetime.strptime(
                    last_processed_date_str, date_format
                )

            for path in all_paths:
                path_parts = list(filter(None, path.replace("s3:/", "").split("/")))
                if isinstance(date_segment, int):
                    path_date = datetime.strptime(path_parts[date_segment], date_format)
                if isinstance(date_segment, list):
                    path_date_str = ""
                    for segment in date_segment:
                        path_date_str = path_date_str + path_parts[segment]
                    path_date = datetime.strptime(path_date_str, date_format)
                if path_date > last_processed_date:
                    paths_to_process[path_date] = path

            for path_date in sorted(paths_to_process):
                sorted_paths_to_process.append(paths_to_process[path_date])
            return sorted_paths_to_process
        else:
            return []

    @staticmethod
    def get_all_directories(resource: ResourceItem, last_processed: str) -> List[str]:
        full_path = resource.full_path
        all_paths: List[str] = []
        if full_path.startswith("s3://"):
            path = full_path.replace("s3://", "")
            bucket = path.split("/")[0]
            prefix = path.replace(f"{bucket}/", "")
            s3 = boto3.client("s3")
            response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
            for s3_file in response["Contents"]:
                if (
                    len(list(filter(None, s3_file["Key"].split("/"))))
                    == resource.date_segment
                    or last_processed.split("/")[-1] == s3_file["Key"].split("/")[-1]
                ):
                    all_paths.append(f"s3://{bucket}/{s3_file['Key']}")
            return all_paths
        else:
            paths = [
                os.path.join(dp, f)
                for dp, dn, fn in os.walk(os.path.expanduser(full_path))
                for f in fn
            ]
            for path in paths:
                all_paths.append(path)
            return all_paths

    def get_all_data_sources(
        self, base_path: str = "catalog"
    ) -> List[Tuple[str, DataSource]]:
        last_repo_update = self._repo.last_update(base_path)
        needs_update = (
            last_repo_update is None
            or last_repo_update > self._last_updated_data_source_dttm
        )
        self._last_updated_data_source_dttm = datetime.utcnow()
        if needs_update or len(self._all_data_sources) == 0:
            print("getting all data sources")
            catalog_contents = self._repo.list_items(base_path)
            data_sources: List[Tuple[str, DataSource]] = []
            while catalog_contents:
                file_path = catalog_contents.pop(0)
                if self._repo.is_dir(file_path):
                    catalog_contents.extend(self._repo.list_items(file_path))
                elif file_path.endswith(".json"):
                    data_source = self.get_data_source(file_path, self.environment)
                    if data_source:
                        data_sources.append((file_path, data_source))
            self._all_data_sources = data_sources
            return data_sources
        else:
            print("returning cached data sources")
            return self._all_data_sources
