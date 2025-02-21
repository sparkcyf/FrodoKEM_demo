# encrypt.py

import argparse
from frodo_core import FrodoFileEncryption

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Encrypt a file using FrodoKEM')
    parser.add_argument('input_file', help='Input file to encrypt')
    parser.add_argument('output_file', help='Output encrypted file')
    parser.add_argument('key_file', help='File to save the secret key')
    parser.add_argument('--variant', default='FrodoKEM-640-AES',
                      choices=['FrodoKEM-640-AES', 'FrodoKEM-976-AES', 'FrodoKEM-1344-AES'],
                      help='FrodoKEM variant to use')
    
    args = parser.parse_args()
    
    try:
        # Create encryption instance
        frodo_enc = FrodoFileEncryption(args.variant)
        
        print(f"Encrypting {args.input_file}...")
        # Encrypt the file
        pk, sk = frodo_enc.encrypt_file(args.input_file, args.output_file)
        
        # Save the secret key
        with open(args.key_file, 'wb') as f:
            f.write(sk)
            
        print(f"Encryption successful!")
        print(f"Encrypted file saved to: {args.output_file}")
        print(f"Secret key saved to: {args.key_file}")
        print("\nWARNING: Keep the secret key safe and secure. You will need it to decrypt the file.")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())