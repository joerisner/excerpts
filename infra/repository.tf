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
      strict_required_status_checks_policy =  true

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
    }
  }
}

resource "github_actions_repository_permissions" "this" {
  repository      = github_repository.this.name
  allowed_actions = "selected"

  # TODO: No CI workflow created yet, but will be added later.
  allowed_actions_config {
    github_owned_allowed = true # actions/checkout, actions/setup-*, etc.
    verified_allowed     = false
    patterns_allowed     = ["astral-sh/setup-uv@*", "hashicorp/setup-terraform@*"]
  }
}

resource "github_workflow_repository_permissions" "this" {
  repository                       = github_repository.this.name
  default_workflow_permissions     = "read"
  can_approve_pull_request_reviews = false
}
