import requests
import auth_layer.jwt_class as jwt_class

def login_auth(login_dict):

  url_login = 'https://redmine.iphan.gov.br/redmine/issues.json' 

  if not login_dict.get("jwt_token"):

    jwt_token = False

    login = login_dict.get("usuario")
    senha = login_dict.get("senha")
    response = requests.get(url_login, auth=(login, senha))

    if response.status_code == 200:
      jwt_token = jwt_class.create_jwt(login_dict)

    full_response = [ response.status_code, jwt_token ]

  else:

    payload = jwt_class.verify_and_decode_jwt(login_dict)

    if type(payload) is dict:
      
      login = payload.get("usuario")
      senha = payload.get("senha")
      response = requests.get(url_login, auth=(login, senha))

      if response.status_code == 200:
        full_response = [ response.status_code, jwt_token ]
      else:
        jwt_token = False
        full_response = [ response.status_code, jwt_token ]
  
  return full_response 


  
