import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


salt = b"abd05bwet0sdfsawetgajdlkasdnfljbwaesdf35guw="


def encrypted(bytes, password):
	passcode = password.encode('utf-8')
	kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
	key = base64.urlsafe_b64encode(kdf.derive(passcode)) # making password 32 bytes length

	token = Fernet(key).encrypt(bytes)
	return token
	
	
def decrypted(bytes, password):
	passcode = password.encode('utf-8')
	kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1) 
	key = base64.urlsafe_b64encode(kdf.derive(passcode)) # making password 32 bytes length

	token = Fernet(key).decrypt(bytes)
	return token