terraform {
    cloud {
      organization = "signalroom"

        workspaces {
            name = "kafka-topic-record-picker-python-app"
        }
  }

  # Using the "pessimistic constraint operators" for all the Providers to ensure
  # that the provider version is compatible with the configuration.  Meaning
  # only patch-level updates are allowed but minor-level and major-level 
  # updates of the Providers are not allowed
  required_providers {
        confluent = {
            source  = "confluentinc/confluent"
            version = "~> 2.24.0"
        }
        aws = {
            source  = "hashicorp/aws"
            version = "~> 5.94.1"
        }
    }
}

locals {
  cloud                         = "AWS"
  secrets_insert                = "record_picker_python_app"
  confluent_secrets_path_prefix = "/confluent_cloud_resource/${local.secrets_insert}"
}

# Reference the Confluent Cloud
data "confluent_organization" "env" {}

# Create the Confluent Cloud Environment
resource "confluent_environment" "env" {
  display_name = "${local.secrets_insert}"

  stream_governance {
    package = "ESSENTIALS"
  }
}