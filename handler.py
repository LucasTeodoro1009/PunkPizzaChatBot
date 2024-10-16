import json
import boto3
import hashlib
import os
from dotenv import load_dotenv
from datetime import datetime

# Carregando variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializando os serviços da AWS
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
polly = boto3.client('polly')  # Inicializando o Polly
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])  # Variável do .env
bucket_name = os.environ["BUCKET_NAME"] # Variável do .env

def tts(event, context):
    try:
        # Processar o corpo da requisição
        body = json.loads(event['body'])
        phrase = body.get('phrase')

        if not phrase:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Phrase is required."})
            }

        print(f"Received phrase: {phrase}")

        # Gerar um hash único para a frase
        unique_id = hashlib.md5(phrase.encode()).hexdigest()

        # Verificar se o áudio já foi gerado anteriormente no DynamoDB
        response = table.get_item(Key={'dynamoapikey': unique_id})
        if 'Item' in response:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    'received_phrase': phrase,
                    'url_to_audio': response['Item']['audio_url'],
                    'created_audio': response['Item']['created_at'],
                    'unique_id': unique_id
                })
            }

        # Gerar o áudio com o Amazon Polly
        polly_response = polly.synthesize_speech(
            Text=phrase,
            OutputFormat='mp3',
            VoiceId='Joanna'  # Você pode trocar para outra voz se preferir
        )

        # Armazenar o arquivo MP3 no S3
        s3_key = f"{unique_id}.mp3"
        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=polly_response['AudioStream'].read())
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"

        # Salvar a referência no DynamoDB
        created_at = datetime.utcnow().isoformat()
        table.put_item(
            Item={
                'dynamoapikey': unique_id,
                'phrase': phrase,
                'audio_url': s3_url,
                'created_at': created_at
            }
        )

        # Retornar a resposta da API
        return {
            "statusCode": 200,
            "body": json.dumps({
                'received_phrase': phrase,
                'url_to_audio': s3_url,
                'created_audio': created_at,
                'unique_id': unique_id
            })
        }

    except Exception as e:
        # Logar o erro e retornar um erro 500 com a mensagem de exceção
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }