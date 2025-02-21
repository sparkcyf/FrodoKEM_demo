#!/bin/bash
# FrodoKEM Encryption/Decryption Demo Script
# This script demonstrates the post-quantum FrodoKEM encryption and decryption process
# It encrypts a file, then decrypts it, and verifies the SHA-256 checksums match

# Colorful output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}==========================================================${NC}"
echo -e "${BLUE}         Post-Quantum FrodoKEM Encryption Demo            ${NC}"
echo -e "${BLUE}==========================================================${NC}"

# Check if a file was provided as argument
if [ "$#" -ne 1 ]; then
  echo -e "${RED}Error: Please provide a file to encrypt/decrypt${NC}"
  echo "Usage: $0 <file_to_encrypt>"
  exit 1
fi

INPUT_FILE="$1"
ENCRYPTED_FILE="${INPUT_FILE}.enc"
DECRYPTED_FILE="${INPUT_FILE}.dec"
KEY_FILE="frodo_key.hex"

# Check if the input file exists
if [ ! -f "$INPUT_FILE" ]; then
  echo -e "${RED}Error: Input file '$INPUT_FILE' does not exist!${NC}"
  exit 1
fi

# Check if python3 and required scripts are available
if ! command -v python3 &> /dev/null; then
  echo -e "${RED}Error: Python 3 is not installed or not in PATH${NC}"
  exit 1
fi

if [ ! -f "encrypt.py" ] || [ ! -f "decrypt.py" ]; then
  echo -e "${RED}Error: encrypt.py or decrypt.py not found in current directory${NC}"
  exit 1
fi

# Calculate original file SHA-256
echo -e "\n${YELLOW}Step 1: Calculating SHA-256 of original file...${NC}"
ORIGINAL_SHA=$(sha256sum "$INPUT_FILE" | awk '{print $1}')
echo -e "Original file: ${GREEN}$INPUT_FILE${NC}"
echo -e "SHA-256: ${GREEN}$ORIGINAL_SHA${NC}"

# Encrypt the file
echo -e "\n${YELLOW}Step 2: Encrypting file using FrodoKEM...${NC}"
python3 encrypt.py "$INPUT_FILE" "$ENCRYPTED_FILE" "$KEY_FILE"
if [ $? -ne 0 ]; then
  echo -e "${RED}Error: Encryption failed!${NC}"
  exit 1
fi

# Show encrypted file info
ENCRYPTED_SIZE=$(stat -c%s "$ENCRYPTED_FILE" 2>/dev/null || stat -f%z "$ENCRYPTED_FILE")
echo -e "Encrypted file size: ${GREEN}$ENCRYPTED_SIZE bytes${NC}"

# Decrypt the file
echo -e "\n${YELLOW}Step 3: Decrypting file using FrodoKEM...${NC}"
python3 decrypt.py "$ENCRYPTED_FILE" "$DECRYPTED_FILE" "$KEY_FILE"
if [ $? -ne 0 ]; then
  echo -e "${RED}Error: Decryption failed!${NC}"
  exit 1
fi

# Calculate decrypted file SHA-256
echo -e "\n${YELLOW}Step 4: Calculating SHA-256 of decrypted file...${NC}"
DECRYPTED_SHA=$(sha256sum "$DECRYPTED_FILE" | awk '{print $1}')
echo -e "Decrypted file: ${GREEN}$DECRYPTED_FILE${NC}"
echo -e "SHA-256: ${GREEN}$DECRYPTED_SHA${NC}"

# Verify the checksums match
echo -e "\n${YELLOW}Step 5: Verifying integrity...${NC}"
if [ "$ORIGINAL_SHA" = "$DECRYPTED_SHA" ]; then
  echo -e "${GREEN}SUCCESS: Checksums match! The file was encrypted and decrypted correctly.${NC}"
  echo -e "Original:  $ORIGINAL_SHA"
  echo -e "Decrypted: $DECRYPTED_SHA"
else
  echo -e "${RED}ERROR: Checksums do not match! The decryption process failed.${NC}"
  echo -e "Original:  $ORIGINAL_SHA"
  echo -e "Decrypted: $DECRYPTED_SHA"
  exit 1
fi

echo -e "\n${BLUE}==========================================================${NC}"
echo -e "${GREEN}Post-Quantum Encryption Demo Completed Successfully!${NC}"
echo -e "${BLUE}==========================================================${NC}"

exit 0