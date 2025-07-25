from typing import Any
from dataclasses import dataclass
from pyspark.sql import SparkSession
from src.common.enums.env import Env

class Secrets:
    @classmethod
    def get_secret(cls, dbutils_obj, secret_scope: str, secret_key: str):
        try:
            return dbutils_obj.secrets.get(scope=secret_scope, key=secret_key)
        except Exception as e:
            raise ValueError(f"Nie udało się pobrać sekretu '{secret_key}' z zakresu '{secret_scope}'. Sprawdź uprawnienia i istnienie sekretu. Błąd: {e}")


@dataclass
class BaseCloudConfig:
    dbutils_obj: Any
    spark_session: SparkSession

    DATABRICKS_SECRET_SCOPE: str = "demosur_dev_secret_scope"
    DATABRICKS_ACCESS_CONNECTOR_ID_KEY: str = "databricks-access-connector-id"
    DATALAKE_STORAGE_ACCOUNT_NAME_KEY: str = "datalake-storage-account-name"

    _BRONZE_CONTAINER_PREFIX: str = "bronze"
    _SILVER_CONTAINER_PREFIX: str = "silver"
    _GOLD_CONTAINER_PREFIX: str = "gold"
    _RAW_CONTAINER_PREFIX: str = "raw"

    @property
    def datalake_storage_account_name(self) -> str:
        return Secrets.get_secret(self.dbutils_obj, self.DATABRICKS_SECRET_SCOPE, self.DATALAKE_STORAGE_ACCOUNT_NAME_KEY)

    @property
    def databricks_access_connector_id(self) -> str:
        return Secrets.get_secret(self.dbutils_obj, self.DATABRICKS_SECRET_SCOPE, self.DATABRICKS_ACCESS_CONNECTOR_ID_KEY)

    @property
    def BRONZE_CONTAINER(self) -> str:
        return f"abfss://{self._BRONZE_CONTAINER_PREFIX}@{self.datalake_storage_account_name}.dfs.core.windows.net/"

    @property
    def SILVER_CONTAINER(self) -> str:
        return f"abfss://{self._SILVER_CONTAINER_PREFIX}@{self.datalake_storage_account_name}.dfs.core.windows.net/"

    @property
    def GOLD_CONTAINER(self) -> str:
        return f"abfss://{self._GOLD_CONTAINER_PREFIX}@{self.datalake_storage_account_name}.dfs.core.windows.net/"

    @property
    def RAW_CONTAINER(self) -> str:
        return f"abfss://{self._RAW_CONTAINER_PREFIX}@{self.datalake_storage_account_name}.dfs.core.windows.net/"



class ProjectConfig(BaseCloudConfig): 
    def __init__(self, dbutils_obj: Any, spark_session: SparkSession, env: Env):
        super().__init__(dbutils_obj=dbutils_obj, spark_session=spark_session)
        self.env = env
        self.base_data_lake_path = self._get_base_data_lake_path()

        self.unity_catalog_name = self._get_unity_catalog_name() 

        self._configure_spark_session()
        print(f"ProjectConfig zainicjowany dla środowiska '{self.env}'.")

    def _get_base_data_lake_path(self) -> str:
        if self.env == Env.DEV:
            return Secrets.get_secret(self.dbutils_obj, self.DATABRICKS_SECRET_SCOPE, "datalake-dev-path") 
        elif self.env == Env.PROD:
            return Secrets.get_secret(self.dbutils_obj, self.DATABRICKS_SECRET_SCOPE, "datalake-prod-path") 
        else:
            raise

    def _get_unity_catalog_name(self) -> str:
        if self.env == Env.DEV:
            return "main" 
        elif self.env == Env.PROD:
            return "prod_catalog" 
        else:
            return "dev_catalog" 
            
    def get_unity_catalog_name(self) -> str:
        return self.unity_catalog_name

    def _configure_spark_session(self):
        self.spark.sql(f"USE CATALOG {self.unity_catalog_name}")
        print(f"Ustawiono domyślny katalog Unity Catalog na: {self.unity_catalog_name}")

    def get_raw_location(self) -> str:
        return f"{self.base_data_lake_path}raw/"

    def get_bronze_location(self) -> str:
        return f"{self.base_data_lake_path}bronze/"

    def get_silver_location(self) -> str:
        return f"{self.base_data_lake_path}silver/"

    def get_gold_location(self) -> str:
        return f"{self.base_data_lake_path}gold/"