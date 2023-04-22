from passlib.context import CryptContext



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def Hash(password:str):
     return pwd_context.hash(password)

def Verify(password:str, hash:str):
     return pwd_context.verify(password, hash)