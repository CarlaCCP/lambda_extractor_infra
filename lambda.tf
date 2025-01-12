data "archive_file" "lambda" {
  type        = "zip"
  source_file = "lambda/handler.py"
  output_path = "lambda_function_payload.zip"
}

resource "aws_lambda_layer_version" "ffmpeg" {
  filename   = "python.zip"
  layer_name = "ffmpeg"

  compatible_runtimes = ["python3.9"]
}

resource "aws_lambda_function" "extractor" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "lambda_function_payload.zip"
  function_name = "extractor"
  role          = "arn:aws:iam::339712924021:role/LabRole"
  handler       = "handler.lambda_handler"
  layers        = [aws_lambda_layer_version.ffmpeg.arn] 

  source_code_hash = data.archive_file.lambda.output_base64sha256

  runtime = "python3.9"

  environment {
    variables = {
      foo = "bar"
    }
  }
}

