#-------------------------------------------------------------------------------
import jwt
#-------------------------------------------------------------------------------
#-- Local imports --
#
#-- Firebit imports --
#
#-------------------------------------------------------------------------------
class JWT_Lib(object):
    #...........................................................................
    """ Class: Json Web Token Libraries using PyJWT. https://pyjwt.readthedocs.io/en/latest/."""
    #...........................................................................
    def m_encode(self,json,secret,algorithm='HS256'):
        try:
            encoded_jwt = jwt.encode(json,secret,algorithm)
            return encoded_jwt
        except Exception as e:
            raise ValueError(e)
    #...........................................................................
    def m_decode(self,encoded_jwt,secret,algorithms=['HS256']):
        try:
            decoded_jwt = jwt.decode(encoded_jwt,secret,algorithms)
            return decoded_jwt
        except jwt.InvalidSignatureError:
            print('Invalid signature')
            return False
        except jwt.ExpiredSignatureError:
            print('Signature has expired')
            return False
        except Exception as e:
            raise ValueError(e)
    #...........................................................................
    def m_decode_json(self,encoded_jwt,secret,algorithms=['HS256']):
        try:
            decoded_jwt = jwt.decode(encoded_jwt,secret,algorithms,options={"verify_exp":False})
            return decoded_jwt
        except jwt.InvalidSignatureError:
            print('Invalid signature')
            return False
        except jwt.ExpiredSignatureError:
            print('Signature has expired')
            return False
        except Exception as e:
            raise ValueError(e)
    #...........................................................................
#-------------------------------------------------------------------------------