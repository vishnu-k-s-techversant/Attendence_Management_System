import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models import Users


load_dotenv()

oath2_scheme = OAuth2PasswordBearer(tokenUrl = 'token')

class GetUser:
    async def get_current_user(token: str = Depends(oath2_scheme)):
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms = ['HS256'])
            user = await Users.get(id = payload.get('id'))
        except Exception as error:
            return {"error" : str(error)}

        return await user    
