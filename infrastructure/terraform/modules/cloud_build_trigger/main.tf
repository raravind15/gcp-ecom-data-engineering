resource "google_cloudbuild_trigger" "trigger" {

  name = var.name

  filename = var.filename

  github {

    owner = var.github_owner
    name  = var.github_repo

    push {
      branch = var.branch
    }
  }

  service_account = var.service_account

  substitutions = var.substitutions
}