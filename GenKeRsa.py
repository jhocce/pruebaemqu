import json
from Crypto.PublicKey import RSA
key = RSA.generate(2048)

secret_code = "123456789jhocce"

private_key = key.export_key()

public_key = key.publickey().export_key()

# with open('apps/system/secury.json', 'w') as f:
#     # d= json.loads(f.read())
#     d={}
#     d['private_key']=  str(private_key)
#     d['public_key']=str(public_key)
#     json.dump(d, f)


with open("apps/system/private_back.pem", "wb") as f:
    f.write(private_key)


public_key = key.publickey().export_key()


with open("apps/system/public_back.pem", "wb") as f:
    f.write(public_key)