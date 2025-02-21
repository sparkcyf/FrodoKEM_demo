# frodo_core.py

from frodokem import FrodoKEM
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

class FrodoFileEncryption:
    def __init__(self, variant="FrodoKEM-640-AES"):
        """Initialize with specified FrodoKEM variant"""
        self.frodo = FrodoKEM(variant)
        
    def _derive_fernet_key(self, shared_secret):
        """Derive a 32-byte Fernet key from the shared secret using SHAKE256"""
        shake = hashes.Hash(hashes.SHAKE256(32), backend=default_backend())
        shake.update(shared_secret)
        derived_key = shake.finalize()
        return base64.urlsafe_b64encode(derived_key)
        
    def encrypt_file(self, input_file, output_file):
        """
        Encrypt a file using FrodoKEM + Fernet(AES)
        Returns: (public key, secret key) tuple for later decryption
        """
        try:
            # Generate FrodoKEM keypair
            pk, sk = self.frodo.kem_keygen()
            
            # Encrypt the file with FrodoKEM+Fernet
            with open(input_file, 'rb') as f:
                plaintext = f.read()
                
            # Generate and encapsulate a shared secret
            ciphertext, shared_secret = self.frodo.kem_encaps(pk)
            
            # Derive a proper Fernet key from the shared secret
            fernet_key = self._derive_fernet_key(shared_secret)
            fernet = Fernet(fernet_key)
            
            # Encrypt the actual file content
            encrypted_data = fernet.encrypt(plaintext)
            
            # Write the encrypted data and FrodoKEM ciphertext
            with open(output_file, 'wb') as f:
                # First write the length of the KEM ciphertext
                f.write(len(ciphertext).to_bytes(4, byteorder='little'))
                # Then write the KEM ciphertext
                f.write(ciphertext)
                # Finally write the encrypted file content
                f.write(encrypted_data)
                
            return pk, sk
            
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")

    def decrypt_file(self, input_file, output_file, sk):
        """
        Decrypt a file using the provided secret key
        """
        try:
            # Read the encrypted file
            with open(input_file, 'rb') as f:
                # Read the length of KEM ciphertext
                kem_ct_len = int.from_bytes(f.read(4), byteorder='little')
                # Read the KEM ciphertext
                kem_ct = f.read(kem_ct_len)
                # Read the encrypted file content
                encrypted_data = f.read()
            
            # Decrypt the shared secret
            shared_secret = self.frodo.kem_decaps(sk, kem_ct)
            
            # Derive the same Fernet key
            fernet_key = self._derive_fernet_key(shared_secret)
            fernet = Fernet(fernet_key)
            
            # Decrypt the file content
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # Write the decrypted data
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
                
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")