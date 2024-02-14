
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.91.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "amse-rg" {
  name     = "amse-resourcegroup"
  location = "West Europe"
}

resource "azurerm_storage_account" "amse-str" {
  name                     = "amsestrassignment"
  resource_group_name      = azurerm_resource_group.amse-rg.name
  location                 = azurerm_resource_group.amse-rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}


resource "azurerm_storage_table" "amse-table" {
  name                 = "amsetableassigment"
  storage_account_name = azurerm_storage_account.amse-str.name
}


resource "azurerm_mssql_server" "amse-sqls" {
  name                         = "amsesqlserverassignment"
  resource_group_name          = azurerm_resource_group.amse-rg.name
  location                     = azurerm_resource_group.amse-rg.location
  version                      = "12.0"
  administrator_login          = "4dm1n157r470r"
  administrator_login_password = "3-v3ry-53cr37-j455w0rt"
}

resource "azurerm_mssql_database" "amse-db" {
  name      = "amsedbassignmentt"
  server_id = azurerm_mssql_server.amse-sqls.id


}

resource "azurerm_data_factory" "amse-adf" {
  name                = "amseadfassignment"
  location            = azurerm_resource_group.amse-rg.location
  resource_group_name = azurerm_resource_group.amse-rg.name

}