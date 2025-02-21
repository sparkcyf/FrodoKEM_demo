# FrodoKEM File Encryption Demo

A simple demonstration of post-quantum encryption using FrodoKEM for file encryption and decryption.

## Overview

This tool demonstrates how to use the FrodoKEM post-quantum key encapsulation mechanism to securely encrypt and decrypt files. The implementation is based on the Python reference implementation from [Microsoft's PQCrypto-LWEKE](https://github.com/microsoft/PQCrypto-LWEKE/tree/master/FrodoKEM/python3) project.

## Requirements

Install dependencies:
```bash
pip install bitstring cryptography
```

## Quick Start

To try the demo, simply run:

```bash
chmod +x demo.sh
./demo.sh <your_file>
```

## Manual Usage

### Encrypting a file

```bash
python encrypt.py <input_file> <output_encrypted_file> <key_file>
```

Example:
```bash
python encrypt.py deepsme_frodokem_encryption_demo.tar.gz deepsme_frodokem_encryption_demo.tar.gz.enc key.hex
```

### Decrypting a file

```bash
python decrypt.py <input_encrypted_file> <output_decrypted_file> <key_file>
```

Example:
```bash
python decrypt.py deepsme_frodokem_encryption_demo.tar.gz.enc deepsme_frodokem_encryption_demo.tar.gz.dec key.hex
```

### Selecting FrodoKEM variant

You can choose between different FrodoKEM variants for different security levels:

```bash
python encrypt.py --variant FrodoKEM-976-AES deepsme_frodokem_encryption_demo.tar.gz deepsme_frodokem_encryption_demo.tar.gz.enc key.hex
```

Available variants:
- `FrodoKEM-640-AES` (default) - NIST Level 1 security
- `FrodoKEM-976-AES` - NIST Level 3 security 
- `FrodoKEM-1344-AES` - NIST Level 5 security

## Credits

Based on the Python3 reference implementation of FrodoKEM from the [Microsoft PQCrypto-LWEKE](https://github.com/microsoft/PQCrypto-LWEKE) project, which is released under the MIT License.

## License

This demo code is provided under the MIT License.