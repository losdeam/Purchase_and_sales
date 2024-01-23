import bcrypt

def hash_password(plaintext_password):
    # 生成盐并对密码进行哈希
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), salt)
    return hashed_password

def verify_password(hashed_password,plaintext_password ):
    # print(plaintext_password, hashed_password)
    # 验证密码是否匹配
    return bcrypt.checkpw(plaintext_password.encode('utf-8'), hashed_password)
