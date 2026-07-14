locals {

  source_bucket_name = "aravind-de-${var.environment}-aravind-source-${var.region}"

  landing_bucket_name = "aravind-de-${var.environment}-landing-${var.region}"

  archive_bucket_name = "aravind-de-${var.environment}-archive-${var.region}"

  error_bucket_name = "aravind-de-${var.environment}-error-${var.region}"

  artifact_repository = "dataeng-images"

  src_to_land_image = "${var.region}-docker.pkg.dev/${var.project_id}/${local.artifact_repository}/src_to_land_gcs:${var.image_tag}"

  landing_to_bq_image = "${var.region}-docker.pkg.dev/${var.project_id}/${local.artifact_repository}/gcs_land_to_bq:${var.image_tag}"

  platform_jobs_image = "${var.region}-docker.pkg.dev/${var.project_id}/${local.artifact_repository}/platform_jobs:${var.image_tag}"

  event_consumer_image = "${var.region}-docker.pkg.dev/${var.project_id}/${local.artifact_repository}/event_consumer:${var.image_tag}"

}

locals {

  common_labels = {
    environment = var.environment
    managed_by  = "terraform"
    project     = "gcp-ecom-data-engineering"
  }

}