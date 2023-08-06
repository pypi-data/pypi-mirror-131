# SimpleCipher
A simple cipher.

## Install

```
python3 -m pip install simplecipher
```

## Dependencies

In terms of dependencies, there are no dependencies.

## Usage

Supported ciphers:
* Caesar cipher
* Vigenere cipher
* Custom cipher

Example:

```python
from simplecipher import simplecipher as sc

message = 'Hello, World!'

offset = 10
encrypted_message = sc.CaesarCipher.encrypt(message, offset=offset)
decrypted_message = sc.CaesarCipher.decrypt(encrypted_message, offset=offset)

key = 'vigenere_key'
encrypted_message = sc.VigenereCipher.encrypt(message, key=key)
decrypted_message = sc.VigenereCipher.decrypt(encrypted_message, key=key)

cipher = sc.SimpleCipher()
replacement = '?' # replacement for unsupported characters
encrypted_message = cipher.encrypt(message, replacement=replacement)
decrypted_message = cipher.decrypt(encrypted_message)
```