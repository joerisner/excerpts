resource "neon_project" "this" {
  name   = "excerpts"
  org_id = var.org_id

  region_id                 = var.region_id
  autoscaling_limit_min_cu  = 0.25
  autoscaling_limit_max_cu  = 2
  history_retention_seconds = 21600
  pg_version                = 18

  branch {
    name          = "prod"
    database_name = "excerpts_prod"
  }
}
