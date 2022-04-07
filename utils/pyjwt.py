import jwt

headers = {
  "alg": "HS256",
  "typ": "JWT"
}

def set_jwt(salt,data,exp_time):
    payload = {
    "name": data,
    "exp": exp_time
    }

    token = jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers)
    return token

def assert_jwt(token,salt):
    try:
        info = jwt.decode(jwt=token,salt=salt,options={'verify_signature':False}, algorithms=['HS256'])
        return info
    except Exception as e:

        return 'token无效'



