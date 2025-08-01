# infra/databricks/variables.tf (PO KOREKCIE)

variable "resource_group_name" {
  description = "The name of the Azure Resource Group where Databricks Workspace will be deployed."
  type        = string
}

variable "location" {
  description = "The Azure region where Databricks Workspace will be deployed."
  type        = string
}

variable "databricks_name" {
  description = "The name of the Azure Databricks Workspace instance."
  type        = string
}

variable "project_prefix" {
  description = "The project prefix used for resource naming."
  type        = string
}

variable "environment" {
  description = "The environment name (e.g., dev, test, prod)."
  type        = string
  default     = "dev"
}

variable "storage_account_id" {
  description = "The ID of the Azure Storage Account (Data Lake Gen2) to connect Unity Catalog to."
  type        = string
}

variable "storage_account_name" {
  description = "The name of the Azure Storage Account (Data Lake Gen2)."
  type        = string
}

variable "bronze_container_name" {
  description = "The name of the Bronze container in the Storage Account."
  type        = string
}

variable "config_container_name" {
  description = "The name of the Config container in the Storage Account."
  type        = string
}

variable "silver_container_name" {
  description = "The name of the Silver container in the Storage Account."
  type        = string
}



variable "key_vault_id" {
  description = "The ID of the Azure Key Vault to link with Databricks secret scope."
  type        = string
}

variable "key_vault_uri" {
  description = "The URI of the Azure Key Vault to link with Databricks secret scope."
  type        = string
}

variable "azure_data_factory_managed_identity_principal_id" {
  description = "The Principal ID of the Azure Data Factory managed identity to grant Contributor role on Databricks Workspace."
  type        = string
}