import hashlib

# List of given MD5 hashes
md5_hashes = [
    "04886164e5140175bafe599b7f1cacc8",
    "664f52463ef97bcd1729d6de1028e41e",
    "3e03cd0f3d335c6fb50122553f63ef78",
    "f2aeb18f5b3f08420eed9b548b6058c3",
    "32b9401a6d972f8c1a98de145629ea9d",
    "3a79238df0a92ab0afa44a85f914fc3b",
    "49c2a68b21b9982aa9fd64cf0fd79f72",
    "f8142c1304efb9b7e9a7f57363c2d286",
    "706457f6dd78729a8bed5bae1efaeb50",
    "bb0564aa5785045937a35a9fa3fbbc73",
    "4173a7bc22aee35c5fc48261b041d064",
    "198b8bf2cd30a7c7fed464cca1720a88",
    "3a7c8ecffeeadb164c31559f8f24a1e7",
    "288e60e318d9ad7d70d743a614442ffc",
    "87ab4cb29649807fdb716ac85cf560ea",
    "89f3ec1275407c9526a645602d56e799",
    "33539252b40b5c244b09aee8a57adbc9",
    "152899789a191d9e9150a1e3a5513b7f",
    "7cd48566f118a02f300cdfa75dee7863",
    "d798a55fca64118cea2df3c120f67569",
    "6ef5570cd43a3ec9f43c57f662201e55",
    "bf189d47c3175ada98af398669e3cac3",
    "743ac25389a0b430dd9f8e72b2ec9d7f",
    "270aabd5feaaf40185f2effa9fa2cd6e",
    "8b58850ee66bd2ab7dd2f5f850c855f8",
    "6fd00cbda10079b1d55283a88680d075",
    "612001dd92369a7750c763963bc327f0",
    "010f2cc580f74521c86215b7374eead6",
    "29860c67296d808bc6506175a8cbb422",
    "7b7f6891b6b6ab46fe2e85651db8205f",
    "45ffb41c4e458d08a8b08beeec2b4652",
    "d0e6bfb6a4e6531a0c71225f0a3d908d",
    "bd7efda0cb3c6d15dd896755003c635c",
    "5be8911ced448dbb6f0bd5a24cc36935",
    "1acbfea6a2dad66eb074b17459f8c5b6",
    "0f262d0003bd696550744fd43cd5b520",
    "8cac896f624576d825564bb30c7250eb",
    "8ef6d2e12a58d7ec521a56f25e624b80",
    "b4959370a4c484c10a1ecc53b1b56a7d",
    "38bdd7748a70529e9beb04b95c09195d",
    "8d4366f08c013f5c0c587b8508b48b15",
    "67566692ca644ddf9c1344415972fba8",
    "8fbf4152f89b7e309e89b9f7080c7230",
    "936f4db24a290032c954073b3913f444",
    "c44d8d6b03dcd4b6bf7cb53db4afdca6",
    "cb722d0b55805cd6feffc22a9f68177d",
    "724d494386f8ef9141da991926b14f9b",
    "67c7aef0d5d3e97ad2488babd2f4c749",
]

# Process each hash
results = {}
for md5_hash in md5_hashes:
    md5_with_newline = md5_hash + "\n"
    sha256_hash = hashlib.sha256(md5_with_newline.encode('utf-8')).hexdigest()
    results[md5_hash] = sha256_hash

# Display results
for md5, sha256 in results.items():
    print(f"MD5: {md5} -> SHA-256 with Newline: {sha256}")
