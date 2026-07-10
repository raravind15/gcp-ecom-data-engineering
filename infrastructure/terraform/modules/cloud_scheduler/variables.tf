variable "job_name" {
  type = string
}

variable "description" {
  type    = string
  default = ""
}

variable "region" {
  type = string
}

variable "schedule" {
  type = string
}

variable "time_zone" {
  type    = string
  default = "Asia/Kolkata"
}

variable "http_method" {
  type    = string
  default = "POST"
}

variable "uri" {
  type = string
}

variable "service_account_email" {
  type = string
}

variable "request_body" {
  type    = string
  default = ""
}