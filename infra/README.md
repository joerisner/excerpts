# Terraform IaC

## Provider isolation

- Each provider has its own directory to ensure state and credentials are isolated and to prevent one provider from being blocked by another, in occasions where a provider may be down.
- State is stored in S3 with each provider having its own key in the bucket.
- Run `terraform` commands from each provider's directory.
- There are a couple of `make` targets that can be ran from the root of the project for formatting and validating all providers as well.

**Example:**

```sh
# From ./infra/github directory:
terraform init -backend-config="./backend.hcl"
terraform plan
terraform apply
```
