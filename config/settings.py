import os

from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')

UPLOADS_DIR = os.getenv('UPLOADS_DIR')

VECTOR_DB_PATH = os.getenv('./index')

EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL')

LLM_MODEL = os.getenv('LLM_MODEL', '')
