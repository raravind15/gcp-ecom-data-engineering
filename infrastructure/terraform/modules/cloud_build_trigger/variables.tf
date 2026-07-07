variable "name" {
  type = string
}

variable "filename" {
  type = string
}

variable "github_owner" {
  type = string
}

variable "github_repo" {
  type = string
}

variable "branch" {
  type = string
}

variable "service_account" {
  type = string
}

variable "substitutions" {
  type = map(string)
}