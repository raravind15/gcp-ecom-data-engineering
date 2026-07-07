resource "google_eventarc_trigger" "trigger" {

  name     = var.name
  location = var.location

  matching_criteria {
    attribute = "type"
    value     = "google.cloud.storage.object.v1.finalized"
  }

  matching_criteria {
    attribute = "bucket"
    value     = var.bucket
  }

  destination {
    cloud_run_service {
      service = var.cloud_run_service
      region  = var.location
    }
  }

  service_account = var.service_account
}