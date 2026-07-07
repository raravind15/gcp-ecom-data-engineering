resource "google_storage_bucket" "bucket" {

  name = var.bucket_name

  location = var.location

  uniform_bucket_level_access = true

  storage_class = var.storage_class

}