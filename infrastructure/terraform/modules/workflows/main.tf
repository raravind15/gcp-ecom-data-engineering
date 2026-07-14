resource "google_workflows_workflow" "workflow" {

  name        = var.name
  region      = var.region
  description = var.description

  service_account = var.service_account

  source_contents = var.source_contents
}