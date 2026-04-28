from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'df6b3477d07b7f6ccc958eb4bc155585')

    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Swagger / OpenAPI
    OPENAPI_COMPONENTS = {
        "securitySchemes": {
            "SessionAuth": {
                "type": "apiKey",
                "in": "cookie",
                "name": "session"
            }
        }
    }

    OPENAPI_SECURITY = [{"SessionAuth": []}]