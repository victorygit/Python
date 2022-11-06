import gnupg
import os
from pprint import pprint

newhome = 'd:/tmp/.gnupg'

if os.path.exists(newhome) is True:
    print("The {0} directory already exists.".format(newhome))
else:
    print("Creating the {0} directory.".format(newhome))
    os.mkdir(newhome)
    os.chmod(newhome, 0o700)

gpg = gnupg.GPG(gnupghome=newhome)
key_data = open('d:/tmp/.gnupg/my_SECRET.asc').read()
import_result = gpg.import_keys(key_data)
#pprint(import_result.results)

gpg = gnupg.GPG(gnupghome='d:/tmp/.gnupg')
gpg.encoding= 'utf-8'
path = 'd:/tmp'
inputfile = '/message.txt'
encryptfile = '/message.pgp'
decryptfile = '/newmessage.txt'

with open(path+inputfile, 'rb') as f:
    status = gpg.encrypt_file(
        f, recipients=['yzy628@yahoo.com'],always_trust=True, output=path+encryptfile)

print ('ok: ', status.ok)
print ('status: ', status.status)
print ('stderr: ', status.stderr)

#decrypt:
gpg = gnupg.GPG(gnupghome=newhome)
#key_data = open('d:/tmp/.gnupg/my_public.asc').read()
#import_result = gpg.import_keys(key_data)
#pprint(import_result.results)

with open(path+encryptfile, 'rb') as f:
    #status = gpg.decrypt_file(f, passphrase='myphase1', output=path+decryptfile)
    status = gpg.decrypt_file(f, output=path+decryptfile)

print ('ok: ', status.ok)
print ('status: ', status.status)
print ('stderr: ', status.stderr)