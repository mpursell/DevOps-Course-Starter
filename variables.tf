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

variable "CALLBACK_URI" {
  description = "callback URI"
  sensitive   = true

}
