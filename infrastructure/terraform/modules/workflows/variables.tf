variable "name" {
  type = string
}

variable "region" {
  type = string
}

variable "description" {
  type    = string
  default = ""
}

variable "service_account" {
  type = string
}

variable "source_contents" {
  type = string
}