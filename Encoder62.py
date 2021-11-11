def base62_encode(deci):
  s='012345689abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  hash_str = ''
  while deci > 0:
    hash_str= s[deci % 62] + hash_str
    deci //= 62
  return hash_str
print(base62_encode(999999))