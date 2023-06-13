from datetime import datetime, timedelta
from jose import jwt
from src.auth.schemas import JWTData
from src.auth.config import auth_config

def generate_fake_access_token(user_id: int, is_admin: bool) -> str:
    now = datetime.utcnow()
    expires_at = now + timedelta(minutes=auth_config.JWT_EXP)

    jwt_data = JWTData(
        user_id=user_id,
        exp=expires_at,
        is_admin=is_admin
    )
    token = jwt.encode(jwt_data.dict(), auth_config.JWT_SECRET, algorithm=auth_config.JWT_ALG)
    return token