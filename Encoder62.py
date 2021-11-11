#This is a 62 bit encoder that creats a 8 character random number has that can be used as a short URL
#Base62 encoder allows us to use the combination of characters and numbers which contains A-Z, a-z, 0–9 total( 26 + 26 + 10 = 62)
#So for 8 character short Url we can serve upto 62^8 URL (pow(62,8)
print(pow(62,8))
#
#Decoder
def base62_encode(deci):
  s='012345689abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  hash_str = ''
  while deci > 0:
    hash_str= s[deci % 62] + hash_str
    deci //= 62
  return hash_str
#Example hash printed below
print(base62_encode(99999999999999))
