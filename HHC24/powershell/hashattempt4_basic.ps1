import hashlib

md5_value = "5f8dd236f862f4507835b0e418907ffc"
sha256_of_md5 = hashlib.sha256(md5_value.encode()).hexdigest()
print(sha256_of_md5.upper())