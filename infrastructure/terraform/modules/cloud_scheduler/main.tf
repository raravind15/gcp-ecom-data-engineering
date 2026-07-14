resource "google_cloud_scheduler_job" "job" {

  name        = var.job_name
  description = var.description

  region = var.region

  schedule  = var.schedule
  time_zone = var.time_zone

  http_target {

    http_method = var.http_method

    uri = var.uri

    dynamic "oidc_token" {

        for_each = var.auth_type == "OIDC" ? [1] : []

        content {
          service_account_email = var.service_account_email
        }
    }

    dynamic "oauth_token" {

        for_each = var.auth_type == "OAUTH" ? [1] : []

        content {
          service_account_email = var.service_account_email
        }
    }

    body = base64encode(var.request_body)

    headers = {
      "Content-Type" = "application/json"
    }
  }
}