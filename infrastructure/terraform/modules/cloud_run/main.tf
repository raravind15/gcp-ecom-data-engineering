resource "google_cloud_run_v2_service" "service" {

  name     = var.service_name
  location = var.location

  template {

    service_account = var.service_account

    timeout = "${var.timeout}s"

    scaling {
      max_instance_count = var.max_scale
    }

    containers {

      image = var.image

      resources {
        limits = {
          cpu    = var.cpu
          memory = var.memory
        }
      }

      dynamic "env" {
        for_each = var.environment_variables

        content {
          name  = env.key
          value = env.value
        }
      }
    }
  }

  lifecycle {
    ignore_changes = [
      client,
      client_version
    ]
  }
}