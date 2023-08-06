import sys


class SimpleCipher:
    CHAR_SET_ODD = ['0', 'o', 'O', '8']
    CHAR_SET_EVEN = ['l', 'L', 'i', 'I']
    MIN_SUPPORTED_ORD = 32
    MAX_SUPPORTED_ORD = 126
    MODULO_LENGTH = min(len(CHAR_SET_EVEN), len(CHAR_SET_ODD))
    DEFAULT_REPLACEMENT = ''
    SEPARATOR = ' '

    def __init__(self):
        pass

    @staticmethod
    def get_ordinals(message: str) -> []:
        return [ord(char) for char in message]

    def is_supported(self, ordinal: int) -> bool:
        return ordinal >= self.MIN_SUPPORTED_ORD and ordinal <= self.MAX_SUPPORTED_ORD

    def are_supported(self, ordinals: []) -> bool:
        return all([self.is_supported(ordinal) for ordinal in ordinals])

    def get_sanitized_replacement_ordinals(self, replacement: str) -> []:
        replacement_ordinals = SimpleCipher.get_ordinals(replacement)
        if self.are_supported(replacement_ordinals):
            return replacement_ordinals
        else:
            return []

    def get_sanitized_ordinals(self, message: str, replacement: str = DEFAULT_REPLACEMENT) -> []:
        replacement_ordinals = self.get_sanitized_replacement_ordinals(replacement)
        message_ordinals = SimpleCipher.get_ordinals(message)
        sanitized_ordinals = []
        for ordinal in message_ordinals:
            if self.is_supported(ordinal):
                sanitized_ordinals.append(ordinal)
            else:
                sanitized_ordinals.extend(replacement_ordinals)
        return sanitized_ordinals

    def encrypt(self, message: str, replacement: str = '') -> str:
        ordinals = SimpleCipher.get_ordinals(message)
        sanitized_ordinals = self.get_sanitized_ordinals(message, replacement=replacement)
        encrypted_message = []
        last_used_char = ''
        for ordinal in sanitized_ordinals:
            ordinal -= SimpleCipher.MIN_SUPPORTED_ORD
            if ordinal % 2:
                char_set = SimpleCipher.CHAR_SET_ODD
                ordinal = (ordinal - 1) // 2
            else:
                char_set = SimpleCipher.CHAR_SET_EVEN
                ordinal //= 2
            modulo = ordinal % SimpleCipher.MODULO_LENGTH
            quotient = ordinal // SimpleCipher.MODULO_LENGTH
            encrypted_char = char_set[modulo]
            if encrypted_char == last_used_char:
                encrypted_message.append(SimpleCipher.SEPARATOR)
            last_used_char = encrypted_char
            encrypted_message.append(encrypted_char * quotient)
        return ''.join(encrypted_message)        

    def get_decryption_parts(self, message: str) -> []:
        message_length = len(message)
        char = message[0]
        message = message.lstrip(char)
        nr_removed_chars = message_length - len(message)
        result = [(char, nr_removed_chars)]
        if not message:
            return result
        return result + self.get_decryption_parts(message)

    def decrypt(self, message: str) -> str:
        parts = self.get_decryption_parts(message)
        decrypted_message = []
        for part in parts:
            if part[0] in SimpleCipher.CHAR_SET_ODD:
                char_set = SimpleCipher.CHAR_SET_ODD
                even = False
            elif part[0] in SimpleCipher.CHAR_SET_EVEN:
                char_set = SimpleCipher.CHAR_SET_EVEN
                even = True
            else:
                continue
            index = char_set.index(part[0])
            ordinal = index + part[1] * SimpleCipher.MODULO_LENGTH
            ordinal *= 2
            if not even:
                ordinal += 1
            ordinal += SimpleCipher.MIN_SUPPORTED_ORD
            decrypted_message.append(chr(ordinal))
        return ''.join(decrypted_message)


class CaesarCipher:
    def __init__(self):
        pass

    @staticmethod
    def encrypt_char(char: str, offset: int = 1) -> str:
        new_ord = ord(char) + offset
        if new_ord > sys.maxunicode:
            new_ord = new_ord % (sys.maxunicode + 1)
        return chr(new_ord)

    @staticmethod
    def encrypt(message: str, offset: int = 1) -> str:
        encrypted_message = []
        for char in message:
            encrypted_char = CaesarCipher.encrypt_char(char, offset=offset)
            encrypted_message.append(encrypted_char)
        return ''.join(encrypted_message)

    @staticmethod
    def decrypt_char(char: str, offset: int = 1) -> str:
        new_ord = ord(char) - offset
        if new_ord < 0:
            new_ord += sys.maxunicode + 1
        return chr(new_ord)

    @staticmethod
    def decrypt(message: str, offset: int = 1) -> str:
        decrypted_message = []
        for char in message:
            decrypted_char = CaesarCipher.decrypt_char(char, offset=offset)
            decrypted_message.append(decrypted_char)
        return ''.join(decrypted_message)


class VigenereCipher:
    VERY_SECRET_KEY = 'cf9acc0a41370810012c03d8a00fbefb'

    def __init__(self):
        pass

    @staticmethod
    def crypt(message: str, encrypt: bool = True, key: str = VERY_SECRET_KEY) -> str:
        crypted_message = []
        key_length = len(key)
        for index in range(len(message)):
            key_ordinal = ord(key[index % key_length])
            if encrypt:
                crypted_char = CaesarCipher.encrypt_char(message[index], offset=key_ordinal)
            else:
                crypted_char = CaesarCipher.decrypt_char(message[index], offset=key_ordinal)
            crypted_message.append(crypted_char)
        return ''.join(crypted_message)

    @staticmethod
    def encrypt(message: str, key: str = VERY_SECRET_KEY) -> str:
        return VigenereCipher.crypt(message, encrypt=True, key=key)

    @staticmethod
    def decrypt(message: str, key: str = VERY_SECRET_KEY) -> str:
        return VigenereCipher.crypt(message, encrypt=False, key=key)
            
