from models import Users
from hashing import Hash


class Authentication:
    async def authenticate_user(username: str, password: str):
        try:
            user = await Users.get(username = username)

            if user and Hash.verify_password(password, user.password):
                return user
        except:
            return False
