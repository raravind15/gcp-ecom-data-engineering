variable "service_name" {
  type = string
}

variable "location" {
  type = string
}

variable "image" {
  type = string
}

variable "service_account" {
  type = string
}

variable "environment_variables" {
  type = map(string)
}

variable "cpu" {
  type = string
  default = "1000m"
}

variable "memory" {
  type = string
  default = "512Mi"
}

variable "timeout" {
  type = number
  default = 300
}

variable "max_scale" {
  type = number
  default = 3
}

variable "allow_unauthenticated" {
  type    = bool
  default = false
}