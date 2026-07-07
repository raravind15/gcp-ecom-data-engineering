variable "project_id" {

  description = "Google Cloud Project ID"

  type = string

}

variable "region" {

  description = "Deployment Region"

  type = string

}

variable "environment" {
  type = string
}

variable "image_tag" {
  description = "Docker image tag"
  type        = string
}