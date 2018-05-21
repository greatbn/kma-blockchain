from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode, b64encode

def sign(data, private_key):
    """
    Sign a data and return signature 
    """
    private_key = RSA.importKey(private_key)
    signer = PKCS1_v1_5.new(private_key)
    digest = SHA256.new()
    digest.update(data)
    signature = signer.sign(digest)

    return signature.encode('hex')


def verify(data, signature, public_key):
    """
    Verify a signature
    return True of False
    """

    public_key = RSA.importKey(public_key)
    verifier = PKCS1_v1_5.new(public_key)
    digest = SHA256.new()
    digest.update(data)
    verified = verifier.verify(digest, signature.decode('hex'))
    if verified:
        return True
    return False


if __name__ == '__main__':
    private_key = open('../test/key/key.pem', 'r').read()
    public_key = open('../test/key/public.pem', 'r').read()
    data = '62d49a9b4d0c804f7de5578dc0df21f754a6b5c43e491271b9c267674189bd7f'
    print "Sign data"
    signature = sign(data, private_key)
    print "Signature ", signature
    print "Verify signature"
    print verify(data, signature, public_key)


    