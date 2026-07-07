terraform {
  backend "gcs" {
    bucket = "di-prod-aravind-tfstate"
    prefix = "terraform/prod"
  }
}