variable "prefix" {
  description = "The prefix used for all resources in this environment"
  default     = "terraform"
}

variable "GH_CLIENTID" {
  description = "github client id"
  sensitive   = true

}

variable "GH_ClIENTSECRET" {
  description = "github client secret"
  sensitive   = true

}

variable "DOCKER_USERNAME" {
  description = "Docker registry username"
  sensitive   = false
}

variable "DOCKER_PASSWORD" {
  description = "Docker registry password"
  sensitive   = true
}

variable "FLASK_APP" {
  description = "Flask app path"
  sensitive   = true
}

variable "FLASK_ENV" {
  description = "Flask environment file to use"
  sensitive   = true
}

variable "SECRET_KEY" {
  description = "Flask Secret Key"
  sensitive   = true
}

variable "client_secret" {
  description = "Azure service principal secret"
  sensitive   = true
}

variable "client_id" {
  description = "Azure service principal id"
  sensitive   = true
}

variable "tenant_id" {
  description = "Azure tenant id"
  sensitive   = true
}