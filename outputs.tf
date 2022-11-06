output "webapp_url" {
  value     = "https://${azurerm_linux_web_app.TerraformOpenCohort21MichaelPursellWebapp.default_hostname}"
  sensitive = false
}

output "webhook_url" {
  value     = "https://${azurerm_linux_web_app.TerraformOpenCohort21MichaelPursellWebapp.site_credential[0].name}:${azurerm_linux_web_app.TerraformOpenCohort21MichaelPursellWebapp.site_credential[0].password}@${azurerm_linux_web_app.TerraformOpenCohort21MichaelPursellWebapp.name}.scm.azurewebsites.net/docker/hook"
  sensitive = true
}

output "callback_uri" {
  value     = azurerm_linux_web_app.TerraformOpenCohort21MichaelPursellWebapp.app_settings.CALLBACK_URI
  sensitive = false
}

output "mongo_db_name" {
  value = azurerm_cosmosdb_mongo_database.terraformtodoappdb0822.name
}