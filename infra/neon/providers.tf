terraform {
  required_version = "~> 1.16"

  required_providers {
    neon = {
      source  = "kislerdm/neon"
      version = "~> 0.18.0"
    }
  }

  backend "s3" {
    # `bucket` and `region` supplied by ./backend.hcl.
    key          = "excerpts/neon/terraform.tfstate"
    encrypt      = true
    use_lockfile = true
  }
}

# API key read from ENV.
provider "neon" {}
