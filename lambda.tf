data "archive_file" "lambda" {
  type        = "zip"
  source_file = "lambda/handler.py"
  output_path = "lambda_function_payload.zip"
}

resource "aws_lambda_layer_version" "ffmpeg" {
  filename   = "layer.zip"
  layer_name = "ffmpeg"

  compatible_runtimes = ["python3.9"]
}

resource "aws_sqs_queue" "create_frames" {
  name = "create-frames-queue"
  visibility_timeout_seconds = 600
}

resource "aws_sqs_queue" "update_frames" {
  name = "update-frames-queue"
  visibility_timeout_seconds = 600
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
  timeout = 600
  memory_size = 600

  environment {
    variables = {
      foo = "bar"
    }
  }
}

resource "aws_lambda_permission" "allow_sqs" {
  statement_id  = "AllowSQSTrigger"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.extractor.function_name
  principal     = "sqs.amazonaws.com"
  source_arn    = aws_sqs_queue.create_frames.arn
}


resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn  = aws_sqs_queue.create_frames.arn
  function_name     = aws_lambda_function.extractor.function_name
  enabled           = true
  batch_size        = 10 # Quantidade máxima de mensagens processadas por vez
}

