import os
import boto3
import json


class Settings:

    if os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        client = boto3.client("secretsmanager")
        response = client.get_secret_value(SecretId=os.environ.get("SECRET_NAME"))
        config = json.loads(response["SecretString"])

    else:
        from dotenv import load_dotenv, find_dotenv

        load_dotenv(find_dotenv())
        config = {
            key: os.getenv(key)
            for key in ["DB_USER", "DB_PASS", "DB_HOST", "DB_NAME", "DB_PORT"]
        }

    DB_USER = config.get("DB_USER")
    DB_PASS = config.get("DB_PASS")
    DB_HOST = config.get("DB_HOST")
    DB_PORT = config.get("DB_PORT")
    DB_NAME = config.get("DB_NAME")
    DATABASE_URL = f"postgresql+psycopg2://{config.get('DB_USER')}:{config.get('DB_PASS')}@{config.get('DB_HOST')}:{config.get('DB_PORT')}/{config.get('DB_NAME')}"
