terraform {
  backend "gcs" {
    bucket = "di-dev-aravind-tfstate"
    prefix = "terraform/dev"
  }
}