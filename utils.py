from passlib.context import CryptContext

# this function code helps with hashing the password that will be supplied at creation time
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

#this function helps to verify the password provided to be sure the hash value matches . and if matched, it is authenticated else its not
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
