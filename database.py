import os
from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv


load_dotenv()

class ConnectToDatabase:
    def connect(app):
        try:
            connection = register_tortoise(
                    app,
                    db_url=os.getenv("DATABASE_URL"),
                    modules = {'models' : ['models']},
                    generate_schemas = True,
                    add_exception_handlers = True
                    )
            return connection
        except Exception as error:
            return {"error" : str(error)}
