terraform {
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = "~> 3.0"

        }
    }
}
provider "azurerm" {
   features{}
}

resource "azurerm_resource_group" "rg-agridrought" {
         name     = "rg-agridrought"
         location = "Spain Central"
}

resource "azurerm_storage_account" "storage" {
  name                = "stagridrought"
  resource_group_name = azurerm_resource_group.rg-agridrought.name

  location                 = azurerm_resource_group.rg-agridrought.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

}

resource "azurerm_storage_container" "bronze" {
  name                  = "bronze"
  storage_account_name   = azurerm_storage_account.storage.name
  container_access_type = "private"
}

