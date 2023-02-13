import jwt
import os
from dotenv import load_dotenv
from fastapi import Depends
from authentication import Authentication
from models import Users


load_dotenv()

class Token:
    async def token_generator(username: str, password: str):
        try:
            user = await Authentication.authenticate_user(username, password)

            if not user:
                return {"error" : "Invalid username or password"}

            token_data = {
                "id" : user.id,
                "username" : user.username
            }

            token = jwt.encode(token_data, os.getenv('SECRET_KEY'))
            return token
        except Exception as error:
            return {"error" : str(error)}

    async def verify_token(token: str):
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms = ['HS256'])
            user = await Users.get(id = payload.get('id'))
        except Exception as error:
            return {"error" : str(error)}

        return user
