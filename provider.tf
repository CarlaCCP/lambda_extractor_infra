terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.52.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.4.3"
    }
  }
  required_version = ">= 1.1.0"
  #   cloud {
  #   organization = "teste-carla"

  #   workspaces {
  #     name = "novo-workspace"
  #   }
  # }
}

provider "aws" {
  region = "us-east-1"
}