def base62_encoder(deci):
  s = '012345689abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  hash_str = ''
  while deci > 0:
    hash_str= s[deci % 62] + hash_str
    deci //=62
  return hash_str
print base62_encoder(999999)
