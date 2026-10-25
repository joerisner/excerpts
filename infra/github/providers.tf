terraform {
  required_version = "~> 1.16"

  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    # `bucket` and `region` supplied by ./backend.hcl.
    key          = "excerpts/github/terraform.tfstate"
    encrypt      = true
    use_lockfile = true
  }
}

provider "github" {
  owner = "joerisner"
  token = var.excerpts_token
}
