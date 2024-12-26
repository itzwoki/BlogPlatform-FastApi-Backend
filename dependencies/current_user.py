from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from sqlalchemy.orm import Session

from db.models.user import User
from db.db_setup import get_db
from userRoutes.utils.loginutil import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
        token : str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    
    try:
        print(f"Received token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid Credentials.")
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token.")
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not Found.")
    
    return user
