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
file = '/message.txt'
unencrypted_string = 'Who are you? How did you get in my house?'
encrypted_data = gpg.encrypt(unencrypted_string, 'yzy628@yahoo.com',always_trust=True)
#print (encrypted_data.ok)
#print (encrypted_data.status)
#print (encrypted_data.stderr)
print (encrypted_data.data)
encrypted_string = str(encrypted_data)
decrypted_data = gpg.decrypt(encrypted_string, passphrase='myphase1')
#print (decrypted_data.ok)
#print (decrypted_data.status)
#print (decrypted_data.stderr)
print (decrypted_data.data)