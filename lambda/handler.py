import json
import boto3
import os
import zipfile
import ffmpeg

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # TODO implement
    print(event)
    print(context)
    print("Iniciando processamento")

  
    bucket_name = 'storage-image-extractor'
    s3_file_key = '123/teste_video.mov'

    local_input_file = '/tmp/teste_video.mov'
    local_output_file = '/tmp'
    zip_file_path = '/tmp/arquivo_convertido.zip'

    # Processo completo
    download_file_from_s3(bucket_name, s3_file_key, local_input_file)  # Passo 1: Baixar arquivo
    process_video(local_input_file, local_output_file)  # Passo 2: Processar com FFmpeg
    zip_file(local_output_file, zip_file_path)  # Passo 3: Compactar em ZIP
    upload_file_to_s3(bucket_name, zip_file_path, "123/imagens.zip")  # Passo 4: Enviar para o S3

    # Limpar arquivos temporários
    os.remove(local_input_file)
    # os.remove(local_output_file)
    os.remove(zip_file_path)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def download_file_from_s3(bucket_name, s3_file_key, local_input_file):
    s3.download_file(bucket_name, s3_file_key, local_input_file)
    print(f"Arquivo {s3_file_key} baixado para {local_input_file}")

def process_video(imput_file, output_file):
    ffmpeg.input(imput_file).output(f'{output_file}%04d.png', vf=f'fps={1}').run()
    print(f"Vídeo processado e salvo em {output_file}")

def zip_file(output_file, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(output_file, os.path.basename(output_file))
    print(f"Arquivo zipado e salvo em {zip_file_path}")

def upload_file_to_s3(bucket_name, zip_file_path, s3_file_key):
    s3.upload_file(zip_file_path, bucket_name, s3_file_key)
    print(f"Arquivo {zip_file_path} enviado para {s3_file_key}")
