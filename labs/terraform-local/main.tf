terraform {
  required_version = ">= 1.5.0"

  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

variable "message" {
  description = "Text written to the generated lab manifest."
  type        = string
  default     = "hello from a local-only Terraform lab"

  validation {
    condition     = length(trimspace(var.message)) > 0
    error_message = "message must not be empty."
  }
}

resource "random_pet" "environment" {
  length = 2
}

resource "local_file" "lab_manifest" {
  filename = "${path.module}/generated/${random_pet.environment.id}.txt"
  content = jsonencode({
    environment = random_pet.environment.id
    message     = var.message
    managed_by  = "terraform"
  })
}

resource "terraform_data" "audit" {
  triggers_replace = {
    manifest_hash = local_file.lab_manifest.content_sha256
  }

  provisioner "local-exec" {
    command = "echo Applied manifest ${self.triggers_replace.manifest_hash}"
  }
}

output "manifest_path" {
  description = "Path of the generated local file."
  value       = local_file.lab_manifest.filename
}

output "environment_name" {
  description = "Stable random name retained in state until replaced."
  value       = random_pet.environment.id
}
