# SimpleCipher
A simple cipher.

## Install

```
python3 -m pip install simplecipher
```

## Usage

```python
from simplecipher import simplecipher as sc

cipher = sc.SimpleCipher()

message = 'Hello, World!'

encrypted_message = cipher.encrypt(message)

decrypted_message = cipher.decrypt(encrypted_message)
```