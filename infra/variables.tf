variable "excerpts_token" {
  description = "GitHub PAT authorized to make repo changes."
  type        = string
  sensitive   = true
}

variable "snyk_token" {
  description = "Snyk token to authenticate with Snyk project."
  type        = string
  sensitive   = true
}
