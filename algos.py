import hashlib
import hmac
import gtk
import urllib2
import time
import os
import base64
from Crypto.Cipher import AES # encryption library
from datetime import datetime, timedelta
import json

#=======================================================================================================
#                        ENCRYPTION
#=======================================================================================================

BLOCK_SIZE = 32

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = '~'

# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

#=======================================================================================================
#                        GET-HTTP
#=======================================================================================================


def get_https(url,API_KEY,API_SECRET,body=None):
  opener = urllib2.build_opener()
  nonce = int(time.time() * 1e6)
  message = str(nonce) + url + ('' if body is None else body)
  signature = hmac.new(API_SECRET, message, hashlib.sha256).hexdigest()
  opener.addheaders = [('ACCESS_KEY', API_KEY),
                       ('ACCESS_SIGNATURE', signature),
                       ('ACCESS_NONCE', nonce)]
  try:
    return opener.open(urllib2.Request(url, body))
  except urllib2.HTTPError as e:
    print e
    return e

def get_http(url):
	opener = urllib2.build_opener()
	try:
		return opener.open(urllib2.Request(url,''))
		print("Yay")
  	except urllib2.HTTPError as e:
    		print e
    		return e

#=======================================================================================================
#                        READ / WRITE
#=======================================================================================================

def decrypt_file(ff,passwd,hsh):
	# create a cipher object using the random secret
	cipher = AES.new(str(passwd))
	ff.seek(0)
	h,s=(ff.read()).split(' ')
	if(h!=hsh):
		print("Incorrect Passwd")
		return -1
	# decode the encoded string
	try:
		decoded = DecodeAES(cipher, s)
		#print 'Decrypted string: %s' % decoded
		return decoded
	except:
		print("Corrupt Config file Error")
		return -2
		
def encrypt_file(ff,passwd,s,hsh):
	# create a cipher object using the random secret
        cipher = AES.new(str(passwd))
        # encode a string
	encoded = hsh+" "+EncodeAES(cipher, s)
	ff.write(encoded);

#=======================================================================================================
#                        OPEN / CREATE FILE
#=======================================================================================================

def read_data(filename):
	if(os.path.isfile(filename)):
		f = open(filename,'r+')
		flag = -1
		count =0
		S=-1
		p=''
		while (S == -1 and count < 5):
			pwd = getText(p,'Enter Password: ') #raw_input("Enter passwd: ")
			pwd=pad(pwd)
			hsh=hashlib.sha256(pwd).hexdigest()
			S=decrypt_file(f,pwd,hsh)
			count = count + 1
			p='Incorrect Password'
			if(count ==5):
				#print("5 Failed attempts")
				raise NameError('Bad Password')
		f.close()
		if(S!=-2 and S!= -1):
			try:
				API_KEY,API_SECRET,p=S.split('\n',2)
			except:
				S=-2
				raise NameError('File has been Corrupted')
				#print("File is Corrupt")
	else:
		#create file
		pwd = getText('Create a new password','Password: ') #raw_input("Create passwd: ")
		pwd2 = getText('','Re-enter password') #raw_input("Re-enter passwd: ")
		while (pwd != pwd2):
			pwd = getText('Password mismatch, please try again','Password: ') # raw_input("Mismatched passwords.\nEnter: ")
			pwd2 = getText('','Re-enter password') #raw_input("Re-enter passwd: ")	
		pwd = pad(str(pwd)) #make it 32 chars long
		
		API_KEY = getText('',"Enter API Key: ") 
		API_SECRET = getText('',"Enter API Secret: ") 
		S='' #API_KEY+'\n'+API_SECRET+'\n'
		p=''
	return S,p,API_KEY,API_SECRET,pwd
#s = get_http('https://coinbase.com/api/v1/account/balance').read()

def begin_auth():
	filename=os.environ['HOME']+'/.test'
	S,p,API_KEY,API_SECRET,pwd = read_data(filename)
	#S=-1 #^these 3 have to go
	return S,p,API_KEY,API_SECRET,pwd

def end_auth(S,p,API_KEY,API_SECRET,pwd):
	if (S != -1 and S!= -2):
		filename=os.environ['HOME']+'/.test'
		#n=n+1;
		#p=raw_input("Add to file:")+"\n"+p # f.read()
		
		S=API_KEY+'\n'+API_SECRET+'\n'+p
		
		#print(S)
		f = open(filename,'w+')
		f.seek(0);
		encrypt_file(f,pwd,S,hashlib.sha256(pwd).hexdigest())
		f.truncate()

def update_mkt():
	XX =[]
	YY=[]
	try:
		data=get_http("http://coinbase.com/api/v1/prices/historical?page=1").read().split('\n')
		for i in range(len(data)):
			s1,s2=data[i].split(',')
			#print(s1,s2)
			XX.append(datetime.strptime(s1[:-6],"%Y-%m-%dT%H:%M:%S")-timedelta(hours=int(s1[-6:-3])))
			YY.append(float(s2))
			#print(str(XX[i])+" "+str(YY[i])+"\n")
		return XX,YY
	except:
		return XX, YY



#--------------------------------------------------------
#            DIALOG BOX
#--------------------------------------------------------
#http://ardoris.wordpress.com/2008/07/05/pygtk-text-entry-dialog/

def responseToDialog(entry, dialog, response):
    dialog.response(response)
def getText(top,bot):
    #base this on a message dialog
    dialog = gtk.MessageDialog(
        None,
        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        gtk.MESSAGE_QUESTION,
        gtk.BUTTONS_OK,
        None)
    dialog.set_markup(top)
    #create the text input field
    entry = gtk.Entry()
    #allow the user to press enter to do ok
    entry.connect("activate", responseToDialog, dialog, gtk.RESPONSE_OK)
    #create a horizontal box to pack the entry and a label
    hbox = gtk.HBox()
    hbox.pack_start(gtk.Label(bot), False, 5, 5)
    hbox.pack_end(entry)
    dialog.vbox.pack_end(hbox, True, True, 0)
    dialog.show_all()
    #go go go
    dialog.run()
    text = entry.get_text()
    dialog.destroy()
    return text

#a='oY3S2Qvwv2n0WWts'
#b='g1ePft6ZhzE54KQgDGqot23zXdbSu1LU'
#bod='qty=0.01'
#s=get_https('https://coinbase.com/api/v1/sells',a,b,bod)
#print(s.read())

