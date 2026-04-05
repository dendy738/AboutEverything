from .some import cryptor

def encryptor(p):
    return cryptor.encrypt(p.encode()).decode()

def decryptor(p):
    return cryptor.decrypt(p.encode()).decode()

def get_encrypted(p):
    return encryptor(p)

def password_compare(p, encrypted):
    decrypted = decryptor(encrypted)
    return p == decrypted


