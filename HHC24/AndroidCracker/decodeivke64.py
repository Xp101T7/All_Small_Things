from base64 import b64decode
from Crypto.Cipher import AES

def decrypt_base64_strings(base64_strings, key, iv):
    """
    Decrypt a list of Base64 strings using AES/GCM.
    
    Args:
        base64_strings (list): List of Base64-encoded ciphertexts.
        key (bytes): AES key (binary).
        iv (bytes): AES initialization vector (binary).
        
    Returns:
        list: Decrypted plaintext strings.
    """
    decrypted_strings = []
    
    for base64_string in base64_strings:
        try:
            # Decode the Base64-encoded ciphertext
            ciphertext = b64decode(base64_string)
            
            # Create AES cipher in GCM mode
            cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
            
            # Decrypt the ciphertext
            plaintext = cipher.decrypt_and_verify(ciphertext[:-16], ciphertext[-16:])
            
            # Decode plaintext to string
            decrypted_strings.append(plaintext.decode('utf-8'))
        
        except Exception as e:
            print(f"Failed to decrypt: {base64_string}")
            print(f"Error: {e}")
            decrypted_strings.append(None)
    
    return decrypted_strings

# Example usage:
if __name__ == "__main__":
    # Replace with your Base64-encoded AES key and IV
    base64_key = "rmDJ1wJ7ZtKy3lkLs6X9bZ2Jvpt6jL6YWiDsXtgjkXw="
    base64_iv = "Q2hlY2tNYXRlcml4"
    
    # Decode key and IV
    key = b64decode(base64_key)
    iv = b64decode(base64_iv)
    
    # List of Base64-encoded strings to decrypt
    base64_strings = [
  "KGfb0vd4u/4EWMN0bp035hRjjpMiL4NQurjgHIQHNaRaDnIYbKQ9JusGaa1aAkGEVV8="
    ]
    
    # Decrypt the strings
    decrypted = decrypt_base64_strings(base64_strings, key, iv)
    for i, plaintext in enumerate(decrypted):
        print(f"Decrypted string {i+1}: {plaintext}")
