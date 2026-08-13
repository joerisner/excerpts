resource "github_repository" "this" {
  name               = "excerpts"
  description        = "Aggregate and revisit selected texts from books, articles, and other mediums."
  archive_on_destroy = true

  allow_auto_merge       = true
  allow_merge_commit     = true
  allow_rebase_merge     = false
  allow_squash_merge     = false
  allow_update_branch    = false
  delete_branch_on_merge = true
  has_discussions        = false
  has_issues             = true
  has_projects           = true
  has_wiki               = false
  is_template            = false
  visibility             = "public"
}

resource "github_repository_ruleset" "main" {
  name        = "main-branch-protection"
  repository  = github_repository.this.name
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["~DEFAULT_BRANCH"]
      exclude = []
    }
  }

  rules {
    creation         = true
    deletion         = true
    non_fast_forward = true

    pull_request {
      required_approving_review_count = 0
    }

    required_status_checks {
      strict_required_status_checks_policy = true

      required_check {
        context = "ruff-lint"
      }

      required_check {
        context = "ruff-format"
      }

      required_check {
        context = "typecheck"
      }

      required_check {
        context = "tf-format"
      }

      required_check {
        context = "tf-validate"
      }

      required_check {
        context = "pytest"
      }

      required_check {
        context = "trufflehog"
      }

      required_check {
        context = "snyk"
      }
    }
  }
}

resource "github_actions_repository_permissions" "this" {
  repository      = github_repository.this.name
  allowed_actions = "selected"

  allowed_actions_config {
    github_owned_allowed = true # actions/checkout, actions/setup-*, etc.
    verified_allowed     = false
    patterns_allowed = [
      "astral-sh/setup-uv@*",
      "hashicorp/setup-terraform@*",
      "trufflesecurity/trufflehog@*",
      "snyk/actions/setup@*"
    ]
  }
}

resource "github_workflow_repository_permissions" "this" {
  repository                       = github_repository.this.name
  default_workflow_permissions     = "read"
  can_approve_pull_request_reviews = false
}

resource "github_issue_labels" "this" {
  repository = github_repository.this.name

  label {
    name        = "bug-fix"
    description = "Fixes a bug"
    color       = "D16069"
  }

  label {
    name        = "dependencies"
    description = "Update project dependencies"
    color       = "ECDB30"
  }

  label {
    name        = "documentation"
    description = "Improvements or additions to documentation"
    color       = "BFD4F2"
  }

  label {
    name        = "feature"
    description = "New feature or request"
    color       = "15D321"
  }

  label {
    name        = "python"
    description = "Pull requests that update Python code"
    color       = "0DD1FA"
  }

  label {
    name        = "infra"
    description = "Pull requests that update infra code"
    color       = "A97BED"
  }
}

resource "github_actions_secret" "snyk_token" {
  repository  = github_repository.this.name
  secret_name = "SNYK_TOKEN"
  value       = var.snyk_token
}

resource "github_dependabot_secret" "snyk_token" {
  repository  = github_repository.this.name
  secret_name = "SNYK_TOKEN"
  value       = var.snyk_token
}
