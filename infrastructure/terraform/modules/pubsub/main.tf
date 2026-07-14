resource "google_pubsub_topic" "topic" {

  name = var.topic_name

}

resource "google_pubsub_subscription" "subscription" {

  name  = var.subscription_name

  topic = google_pubsub_topic.topic.id

  ack_deadline_seconds = 30

  push_config {

    push_endpoint = var.push_endpoint

    oidc_token {
      service_account_email = var.service_account_email
    }

  }

}