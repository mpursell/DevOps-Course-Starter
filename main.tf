terraform {
  required_providers {

    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }

  backend "azurerm" {
    resource_group_name  = "tfstate"
    storage_account_name = "tfstate23188"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {

  }
}

data "azurerm_resource_group" "main" {
  name = "OpenCohort21_MichaelPursell_ProjectExercise"
}

resource "azurerm_service_plan" "TerraformOpenCohort21MichaelPursellWebappServicePlan" {
  name                = "${var.prefix}-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"

}

resource "azurerm_linux_web_app" "TerraformOpenCohort21MichaelPursellWebapp" {
  name                = "${var.prefix}-OpenCohort21MichaelPursellWebapp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.TerraformOpenCohort21MichaelPursellWebappServicePlan.id


  site_config {
    application_stack {
      docker_image     = "mikerp/todoapp"
      docker_image_tag = "latest"
    }
  }
  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "MONGO_CONN_STRING"          = resource.azurerm_cosmosdb_account.terraformcomosdbaccmp0822.connection_strings[0]
    "MONGO_DB_NAME"              = resource.azurerm_cosmosdb_mongo_database.terraformtodoappdb0822.name
    "GH_CLIENTID"                = var.GH_CLIENTID
    "GH_CLIENTSECRET"            = var.GH_ClIENTSECRET
    "CALLBACK_URI"               = "terraform-OpenCohort21MichaelPursellWebapp/login/callback"
    "FLASK_APP"                  = var.FLASK_APP
    "FLASK_ENV"                  = var.FLASK_ENV
    "SECRET_KEY"                 = var.SECRET_KEY

  }
}

resource "azurerm_cosmosdb_account" "terraformcomosdbaccmp0822" {
  name                = "${var.prefix}-comosdbaccmp0822"
  location            = "uksouth"
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "MongoDB"

  capabilities {
    name = "EnableServerless"
  }
  capabilities {
    name = "EnableMongo"
  }
  lifecycle {
    prevent_destroy = false
  }
  geo_location {
    failover_priority = 0
    location          = "uksouth"
    zone_redundant    = false
  }
  consistency_policy {
    consistency_level       = "Session"
    max_interval_in_seconds = 5
    max_staleness_prefix    = 100
  }
  offer_type = "Standard"

}

resource "azurerm_cosmosdb_mongo_database" "terraformtodoappdb0822" {
  name                = "${var.prefix}todoappdb0822"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = resource.azurerm_cosmosdb_account.terraformcomosdbaccmp0822.name
  lifecycle {
    prevent_destroy = false
  }
}

