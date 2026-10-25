variable "org_id" {
  description = "Neon organization ID."
  type        = string
  sensitive   = true
}

variable "region_id" {
  description = "AWS region where the project is deployed."
  type        = string
}
