resource "google_cloud_scheduler_job" "job" {

  name        = var.job_name
  description = var.description

  region = var.region

  schedule  = var.schedule
  time_zone = var.time_zone

  http_target {

    http_method = var.http_method

    uri = var.uri

    oidc_token {
      service_account_email = var.service_account_email
    }

    body = base64encode(var.request_body)

    headers = {
      "Content-Type" = "application/json"
    }
  }
}