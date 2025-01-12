variable "aws_access_key" {
  description = "The AWS access key"
  type        = string
  sensitive   = true
}

variable "aws_secret_key" {
  description = "The AWS secret key"
  type        = string
  sensitive   = true
}

variable "aws_session_token" {
  description = "The AWS session token"
  type        = string
  sensitive   = true
}