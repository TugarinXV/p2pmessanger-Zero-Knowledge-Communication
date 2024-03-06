from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes



# Share securely aes_key and hmac_key with the receiver
# encrypted.bin can be sent over an unsecure channel

def generate_key():
    aes_key = get_random_bytes(16)
    return aes_key

def encrypt_message(aes_key,message):
    data = message.encode()
    #aes_key = generate_key()

    cipher = AES.new(aes_key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)

    return nonce,tag,ciphertext


def decrypt_message(key,nonce,ciphertext,tag):
    cipher = AES.new(key, AES.MODE_EAX,nonce=nonce)
    try:
        plaintext = cipher.decrypt(ciphertext)
        cipher.verify(tag)
        
        return plaintext

    except Exception as e:
        return "ошибочка"
        

key = b"hh" * 8
key2 = b"rr" * 8
nonce,tag,ciphertext = encrypt_message(key,"1234")

print(decrypt_message(key2,nonce,ciphertext,tag))

