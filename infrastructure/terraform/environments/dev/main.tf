module "source_bucket" {

  source = "../../modules/storage_bucket"

  bucket_name = local.source_bucket_name

  location = var.region


}

module "landing_bucket" {

  source = "../../modules/storage_bucket"

  bucket_name = local.landing_bucket_name

  location = var.region

}

module "archive_bucket" {

  source = "../../modules/storage_bucket"

  bucket_name = local.archive_bucket_name

  location = var.region

  storage_class = "ARCHIVE"

}

module "error_bucket" {

  source = "../../modules/storage_bucket"

  bucket_name = local.error_bucket_name

  location = var.region


}

module "src_to_landing_sa" {

  source = "../../modules/service_account"

  account_id = "sa-src-to-landing-ingestion"

  display_name = "sa-src-to-landing-ingestion"

}

module "landing_to_bqraw_sa" {

  source = "../../modules/service_account"

  account_id = "sa-landing-to-bqraw"

  display_name = "sa-landing-to-bqraw"

}

module "git_trigger_sa" {

  source = "../../modules/service_account"

  account_id   = "sa-src-to-land-gcs-git-trg"
  display_name = "sa-src-to-land-gcs-git-trg"

}

##########################################
# IAM - Source to Landing
##########################################

module "src_to_land_logs_writer" {

  source = "../../modules/iam"

  project_id = var.project_id

  role = "roles/logging.logWriter"

  member = module.src_to_landing_sa.member

}

module "src_to_land_eventarc" {

  source = "../../modules/iam"

  project_id = var.project_id

  role = "roles/eventarc.eventReceiver"

  member = module.src_to_landing_sa.member

}

module "src_to_land_storage_admin" {

  source = "../../modules/iam"

  project_id = var.project_id

  role = "roles/storage.objectAdmin"

  member = module.src_to_landing_sa.member

}

##################################################
# IAM - Landing to BigQuery Raw
##################################################

module "landing_to_bq_logs_writer" {

  source = "../../modules/iam"

  project_id = var.project_id

  role = "roles/logging.logWriter"

  member = module.landing_to_bqraw_sa.member

}

module "landing_to_bq_storage_admin" {

  source = "../../modules/iam"

  project_id = var.project_id

  role = "roles/storage.objectAdmin"

  member = module.landing_to_bqraw_sa.member

}

module "landing_to_bq_data_editor" {

  source = "../../modules/iam"

  project_id = var.project_id

  role = "roles/bigquery.dataEditor"

  member = module.landing_to_bqraw_sa.member

}

module "landing_to_bq_job_user" {

  source = "../../modules/iam"

  project_id = var.project_id

  role = "roles/bigquery.jobUser"

  member = module.landing_to_bqraw_sa.member

}

module "landing_to_bq_firestore" {

  source = "../../modules/iam"

  project_id = var.project_id

  role = "roles/datastore.user"

  member = module.landing_to_bqraw_sa.member

}

module "landing_to_bq_eventarc" {

  source = "../../modules/iam"

  project_id = var.project_id

  role = "roles/eventarc.eventReceiver"

  member = module.landing_to_bqraw_sa.member

}

##################################################
# IAM - Cloud build trigger
##################################################

module "git_trigger_artifact_registry_editor" {

  source = "../../modules/iam"

  project_id = var.project_id

  role = "roles/artifactregistry.editor"

  member = module.git_trigger_sa.member

}

module "git_trigger_cloud_run_developer" {

  source = "../../modules/iam"

  project_id = var.project_id
  role       = "roles/run.developer"
  member     = module.git_trigger_sa.member

}

module "git_trigger_logs_writer" {

  source = "../../modules/iam"

  project_id = var.project_id
  role       = "roles/logging.logWriter"
  member     = module.git_trigger_sa.member

}

module "git_trigger_service_account_user" {

  source = "../../modules/iam"

  project_id = var.project_id
  role       = "roles/iam.serviceAccountUser"
  member     = module.git_trigger_sa.member

}

module "git_trigger_storage_object_viewer" {

  source = "../../modules/iam"

  project_id = var.project_id
  role       = "roles/storage.objectViewer"
  member     = module.git_trigger_sa.member

}

#Cloud run service

module "src_to_landing_cloud_run" {

  source = "../../modules/cloud_run"

  service_name = "src-to-landing-ingestion"
  location     = var.region

  image = local.src_to_land_image

  service_account = module.src_to_landing_sa.email

  environment_variables = {
    SOURCE_BUCKET  = local.source_bucket_name
    LANDING_BUCKET = local.landing_bucket_name
  }

}

module "landing_to_bqraw_cloud_run" {

  source = "../../modules/cloud_run"

  service_name = "landing-to-bqraw"
  location     = var.region

  image = local.landing_to_bq_image

  service_account = module.landing_to_bqraw_sa.email

  environment_variables = {
    LANDING_BUCKET = local.landing_bucket_name
    ARCHIVE_BUCKET = local.archive_bucket_name
    ERROR_BUCKET   = local.error_bucket_name
    RAW_DATASET    = "ds_raw"
    AUDIT_DATASET  = "ds_audit"
  }

}

#Eventarc triggers

module "src_to_landing_eventarc" {

  source = "../../modules/eventarc"

  name = "trg-src-to-landing"

  location = var.region

  bucket = local.source_bucket_name

  service_account = module.src_to_landing_sa.email

  cloud_run_service = module.src_to_landing_cloud_run.name

}

module "gcs_landing_to_bq_eventarc" {

  source = "../../modules/eventarc"

  name = "trg-landing-to-bqraw"

  location = var.region

  bucket = local.landing_bucket_name

  service_account = module.landing_to_bqraw_sa.email

  cloud_run_service = module.landing_to_bqraw_cloud_run.name

}

##################################################
# Artifact Registry
##################################################

module "artifact_registry" {

  source = "../../modules/artifact_registry"

  repository_id = "dataeng-images"

  location = var.region

  format = "DOCKER"

}

##################################################
# BigQuery Datasets
##################################################

module "ds_admin" {

  source = "../../modules/bigquery"

  dataset_id = "ds_admin"

  location = "asia-south1"

}

module "ds_audit" {

  source = "../../modules/bigquery"

  dataset_id = "ds_audit"

  location = "asia-south1"

}

module "ds_raw" {

  source = "../../modules/bigquery"

  dataset_id = "ds_raw"

  location = "asia-south1"

}

module "ds_trans" {

  source = "../../modules/bigquery"

  dataset_id = "ds_trans"

  location = "asia-south1"

}

module "ds_curated" {

  source = "../../modules/bigquery"

  dataset_id = "ds_curated"

  location = "asia-south1"

}

#cloud build trigger

module "git_src_to_land_trigger" {

  source = "../../modules/cloud_build_trigger"

  name = "trg-git-src-to-land-gcs"

  filename = "services/src_to_land_gcs/cloudbuild.yaml"

  github_owner = "raravind15"

  github_repo = "gcp-ecom-data-engineering"

  branch = "^main$"

  service_account = module.git_trigger_sa.name

  substitutions = {

    _AR_REPOSITORY = "dataeng-images"

    _ENV = var.environment

    _ENV_FILE = "deploy.env"

    _IMAGE_NAME = "src_to_land_gcs"

    _REGION = var.region

    _SERVICE_ACCOUNT = "sa-src-to-landing-ingestion"

    _SERVICE_NAME = "src-to-landing-ingestion"

    _SOURCE_DIR = "src_to_land_gcs"

  }

}

module "git_land_to_bq_trigger" {

  source = "../../modules/cloud_build_trigger"

  name = "trg-git-land-to-bq"

  filename = "services/gcs_land_to_bq/cloudbuild.yaml"

  github_owner = "raravind15"

  github_repo = "gcp-ecom-data-engineering"

  branch = "^main$"

  service_account = module.git_trigger_sa.name

  substitutions = {

    _AR_REPOSITORY = "dataeng-images"

    _ENV = var.environment

    _ENV_FILE = "gcs_land_to_bq.env"

    _IMAGE_NAME = "gcs_land_to_bq"

    _REGION = var.region

    _SERVICE_ACCOUNT = "sa-landing-to-bqraw"

    _SERVICE_NAME = "landing-to-bqraw"

    _SOURCE_DIR = "gcs_land_to_bq"

  }

}