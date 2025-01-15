import json
import boto3
import os
import subprocess
import shutil

s3 = boto3.client('s3')
sqs = boto3.client('sqs')

FFMPEG_PATH = '/opt/layer/bin/ffmpeg'
os.environ['PATH'] = FFMPEG_PATH + ':' + os.environ['PATH']

def lambda_handler(event, context):
    # TODO implement
    print(event)
    print(context)
    print("Iniciando processamento")

    ##variaveis do evento
    filename = event.get("uploadFilename")
    id = event.get("id")

  
    bucket_name = 'storage-image-extractor'
    s3_file_key = f'{id}/{filename}'

    local_input_file = '/tmp/teste_video.mov'
    local_output_file = '/tmp/frames'

    if not os.path.exists(local_output_file):
        os.makedirs(local_output_file)

    zip_file_path = '/tmp/compactado'

    if not os.path.exists(zip_file_path):
        os.makedirs(zip_file_path)

    #Variaveis sqs
    queue_url = 'update-frames-queue'
    message_body = {"s3-file-key": s3_file_key}


    # Processo completo
    download_file_from_s3(bucket_name, s3_file_key, local_input_file)  # Passo 1: Baixar arquivo
    process_video(local_input_file, local_output_file)  # Passo 2: Processar com FFmpeg
    zip_file(local_output_file, zip_file_path)  # Passo 3: Compactar em ZIP
    upload_file_to_s3(bucket_name, zip_file_path, "123/imagens.zip")  # Passo 4: Enviar para o S3
    send_message_to_sqs(queue_url, json.dumps(message_body))  # Passo 5: Enviar mensagem para a fila SQS

    # Limpar arquivos temporários
    # os.remove(local_input_file)
    # os.remove(local_output_file)
    # os.remove(zip_file_path)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def download_file_from_s3(bucket_name, s3_file_key, local_input_file):
    s3.download_file(bucket_name, s3_file_key, local_input_file)
    print(f"Arquivo {s3_file_key} baixado para {local_input_file}")

def process_video(imput_file, output_file):
    print(FFMPEG_PATH)
    command = f"{FFMPEG_PATH} -i {imput_file} -vf fps=1 {output_file}/frame-%03d.png"
    subprocess.run(command, shell=True)
    print(f"Vídeo processado e salvo em {output_file}")

def zip_file(output_file, zip_file_path):
    shutil.make_archive(f"{zip_file_path}/arquivo_convertido", 'zip', output_file)
    print(f"Arquivo zipado e salvo em {zip_file_path}")

def upload_file_to_s3(bucket_name, zip_file_path, s3_file_key):
    s3.upload_file(f"{zip_file_path}/arquivo_convertido.zip", bucket_name, s3_file_key)
    print(f"Arquivo {zip_file_path} enviado para {s3_file_key}")

def send_message_to_sqs(queue_url, message_body):
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )
    print(f"Mensagem enviada para a fila SQS: {response['MessageId']}")


# input
# s3_dir
# s3_filename

# Output
# s3_file_key