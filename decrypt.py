# decrypt.py

import argparse
from frodo_core import FrodoFileEncryption

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Decrypt a file using FrodoKEM')
    parser.add_argument('input_file', help='Input encrypted file')
    parser.add_argument('output_file', help='Output decrypted file')
    parser.add_argument('key_file', help='File containing the secret key')
    parser.add_argument('--variant', default='FrodoKEM-640-AES',
                      choices=['FrodoKEM-640-AES', 'FrodoKEM-976-AES', 'FrodoKEM-1344-AES'],
                      help='FrodoKEM variant to use')
    
    args = parser.parse_args()
    
    try:
        # Create encryption instance
        frodo_enc = FrodoFileEncryption(args.variant)
        
        # Read the secret key
        with open(args.key_file, 'rb') as f:
            sk = f.read()
        
        print(f"Decrypting {args.input_file}...")
        # Decrypt the file
        frodo_enc.decrypt_file(args.input_file, args.output_file, sk)
        
        print(f"Decryption successful!")
        print(f"Decrypted file saved to: {args.output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())