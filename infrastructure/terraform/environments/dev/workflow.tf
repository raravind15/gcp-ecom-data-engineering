resource "google_workflows_workflow" "daily_transformation" {

  name            = "daily-transformation"
  region          = var.region
  description     = "Daily Transformation Workflow"

  service_account = module.workflow_sa.email

  user_env_vars = {
    PLATFORM_JOBS_URL = module.platform_jobs_cloud_run.uri
  }

  source_contents = file("${path.module}/../../../workflows/daily_transformation.yaml")

  depends_on = [
    module.project_services
  ]
}