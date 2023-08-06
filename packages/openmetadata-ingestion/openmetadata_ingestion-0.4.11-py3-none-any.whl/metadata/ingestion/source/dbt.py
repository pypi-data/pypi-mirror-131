import json
import re
import uuid
from typing import Dict, Iterable, Optional

from metadata.config.common import ConfigModel
from metadata.generated.schema.entity.data.database import Database
from metadata.generated.schema.entity.data.model import Model
from metadata.generated.schema.entity.data.table import Column
from metadata.generated.schema.entity.services.databaseService import (
    DatabaseServiceType,
)
from metadata.generated.schema.type.entityReference import EntityReference
from metadata.ingestion.api.common import IncludeFilterPattern, Record
from metadata.ingestion.api.source import Source, SourceStatus
from metadata.ingestion.models.ometa_table_db import OMetaDatabaseAndModel
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.ingestion.ometa.openmetadata_rest import MetadataServerConfig
from metadata.ingestion.source.sql_source import SQLSourceStatus
from metadata.utils.column_helpers import get_column_type
from metadata.utils.helpers import get_database_service_or_create


class DBTSourceConfig(ConfigModel):
    service_type: str
    service_name: str
    manifest_file: str
    catalog_file: str
    run_results_file: Optional[str]
    database: str
    host_port: str = "localhost"
    filter_pattern: IncludeFilterPattern = IncludeFilterPattern.allow_all()

    def get_service_type(self) -> DatabaseServiceType:
        return DatabaseServiceType[self.service_type]


class DbtSource(Source):
    dbt_manifest: Dict
    dbt_catalog: Dict
    dbt_run_results: Dict
    manifest_schema: str
    manifest_version: str
    catalog_schema: str
    catalog_version: str

    def __init__(
        self, config: DBTSourceConfig, metadata_config: MetadataServerConfig, ctx
    ):
        super().__init__(ctx)
        self.status = SQLSourceStatus()
        self.config = config
        self.metadata_config = metadata_config
        self.metadata = OpenMetadata(metadata_config)
        self.service = get_database_service_or_create(config, metadata_config)

    @classmethod
    def create(cls, config_dict, metadata_config_dict, ctx):
        config = DBTSourceConfig.parse_obj(config_dict)
        metadata_config = MetadataServerConfig.parse_obj(metadata_config_dict)
        return cls(config, metadata_config, ctx)

    def prepare(self):
        self.dbt_catalog = json.load(open(self.config.catalog_file, "r"))
        self.dbt_manifest = json.load(open(self.config.manifest_file, "r"))
        if self.config.run_results_file is not None:
            self.dbt_run_results = json.load(open(self.config.run_results_file, "r"))

        if "metadata" in self.dbt_manifest.keys():
            self.manifest_schema = self.dbt_manifest["metadata"]["dbt_schema_version"]
            self.manifest_version = self.dbt_manifest["metadata"]["dbt_version"]
        if "metadata" in self.dbt_catalog.keys():
            self.catalog_schema = self.dbt_catalog["metadata"]["dbt_schema_version"]
            self.catalog_version = self.dbt_manifest["metadata"]["dbt_version"]

    def next_record(self) -> Iterable[Record]:
        yield from self._parse_dbt()

    def close(self):
        pass

    def get_status(self) -> SourceStatus:
        return self.status

    def _get_database(self, database_name: str) -> Database:
        return Database(
            name=database_name,
            service=EntityReference(id=self.service.id, type=self.config.service_type),
        )

    def _parse_columns(self, model_name: str, cnode: Dict) -> [Column]:
        columns = []
        ccolumns = cnode.get("columns")

        for key in ccolumns:
            ccolumn = ccolumns[key]
            try:
                ctype = ccolumn["type"]
                if re.match("character varying", ctype):
                    ctype = "varchar"

                col_type = get_column_type(self.status, model_name, ctype)
                col = Column(
                    name=ccolumn["name"].lower(),
                    description=ccolumn.get("comment", ""),
                    dataType=col_type,
                    dataLength=1,
                    ordinalPosition=ccolumn["index"],
                )
            except Exception as e:
                print(ccolumn["type"])

            columns.append(col)
        return columns

    def _parse_dbt(self):
        manifest_nodes = self.dbt_manifest["nodes"]
        manifest_sources = self.dbt_manifest["sources"]
        manifest_entities = {**manifest_nodes, **manifest_sources}
        catalog_nodes = self.dbt_catalog["nodes"]
        catalog_sources = self.dbt_catalog["sources"]
        catalog_entities = {**catalog_nodes, **catalog_sources}

        for key, mnode in manifest_entities.items():
            name = mnode["alias"] if "alias" in mnode.keys() else mnode["name"]
            description = mnode.get("description", "")
            cnode = catalog_entities.get(key)
            database = self._get_database(mnode["database"])
            if cnode is not None:
                columns = self._parse_columns(name, cnode)
            else:
                columns = []
            if mnode["resource_type"] == "test":
                continue
            model = Model(
                id=uuid.uuid4(),
                name=name,
                description=description,
                nodeType=mnode["resource_type"].capitalize(),
                viewDefinition=mnode["raw_sql"],
                columns=columns,
            )
            model_and_db = OMetaDatabaseAndModel(model=model, database=database)
            yield model_and_db
