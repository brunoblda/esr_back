import hmac
import hashlib
import base64
import json 
import datetime
from re import I
from secrets import token_hex

secret_key = token_hex(16)

timeStarted = datetime.datetime.now()

def create_jwt(payload):

  global timeStarted
  global secret_key

  payload["exp"] = (datetime.datetime.now() + datetime.timedelta(hours=2)).timestamp()

  if (timeStarted + datetime.timedelta(hours=4)).timestamp() < datetime.datetime.now().timestamp():
    secret_key = token_hex(16)
    timeStarted = datetime.datetime.now()

  payload = json.dumps(payload).encode()
  header = json.dumps({
      'typ': 'JWT',
      'alg': 'HS256'
  }).encode()
  b64_header = base64.urlsafe_b64encode(header).decode()
  b64_payload = base64.urlsafe_b64encode(payload).decode()
  signature = hmac.new(
      key=secret_key.encode(),
      msg=f'{b64_header}.{b64_payload}'.encode(),
      digestmod=hashlib.sha256
  ).digest()
  jwt = f'{b64_header}.{b64_payload}.{base64.urlsafe_b64encode(signature).decode()}'
  return jwt

def verify_and_decode_jwt(jwt):
  global timeStarted
  global secret_key

  if (timeStarted + datetime.timedelta(hours=4)).timestamp() < datetime.datetime.now().timestamp():
    secret_key = token_hex(16)
    timeStarted = datetime.datetime.now()

  b64_header, b64_payload, b64_signature = jwt.split('.')
  b64_signature_checker = base64.urlsafe_b64encode(
      hmac.new(
          key=secret_key.encode(),
          msg=f'{b64_header}.{b64_payload}'.encode(),
          digestmod=hashlib.sha256
      ).digest()
  ).decode()

  # payload extraido antes para checar o campo 'exp'
  payload = json.loads(base64.urlsafe_b64decode(b64_payload))
  unix_time_now = datetime.datetime.now().timestamp()

  if payload.get('exp') and payload['exp'] < unix_time_now:
    return ('Token expirado')

  if b64_signature_checker != b64_signature:
    return ('Assinatura inválida')
  
  return payload    

def authentication(jwt):
  global timeStarted
  global secret_key

  if (timeStarted + datetime.timedelta(hours=4)).timestamp() < datetime.datetime.now().timestamp():
    secret_key = token_hex(16)
    timeStarted = datetime.datetime.now()

  try:
    b64_header, b64_payload, b64_signature = jwt.split('.')
    b64_signature_checker = base64.urlsafe_b64encode(
        hmac.new(
            key=secret_key.encode(),
            msg=f'{b64_header}.{b64_payload}'.encode(),
            digestmod=hashlib.sha256
        ).digest()
    ).decode()

    # payload extraido antes para checar o campo 'exp'
    payload = json.loads(base64.urlsafe_b64decode(b64_payload))
    unix_time_now = datetime.datetime.now().timestamp()

    if payload.get('exp') and payload['exp'] < unix_time_now:
      return False

    if b64_signature_checker != b64_signature:
      return False
    
    return True    
  except:
    return False


if __name__ == '__main__':
  payload = {
      'userId': '55395427-265a-4166-ac93-da6879edb57a',
      'exp': (datetime.datetime.now() + datetime.timedelta(hours=2)).timestamp(),
  }
  jwt_created = create_jwt(payload)
  decoded_jwt = verify_and_decode_jwt(jwt_created)
