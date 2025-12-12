from pwdlib import PasswordHash
password_hash = PasswordHash.recommended()

def hash(password:str):
    return password_hash.hash(password)
         
def orm_to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

def verify(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)