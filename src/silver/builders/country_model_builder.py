# src/silver/model_builders/country_model_builder.py

from pyspark.sql import DataFrame, SparkSession
import pyspark.sql.functions as F
from src.common.builders.base_model_builder import BaseModelBuilder
from src.common.enums.model_type import ModelType
from src.common.enums.domain_source import DomainSource # Potrzebne do identyfikacji źródeł
from typing import List, Type, Dict
from src.common.registers.model_builder_registry import ModelBuilderRegistry


@ModelBuilderRegistry.register(ModelType.COUNTRY)
class CountryModelBuilder(BaseModelBuilder):
    def build_model(self) -> DataFrame:
        """
        Główna logika budowania modelu Country.
        1. Pobiera zarejestrowane readery dla ModelType.COUNTRIES.
        2. Czyta dane z każdego źródła (Bronze/Bronze Plus).
        3. Standaryzuje kolumny dla każdego źródła.
        4. Scala wszystkie standaryzowane dane.
        5. Wykonuje unifikację i deduplikację, tworząc finalny model.
        """

        all_raw_country_data: List[DataFrame] = []
        

