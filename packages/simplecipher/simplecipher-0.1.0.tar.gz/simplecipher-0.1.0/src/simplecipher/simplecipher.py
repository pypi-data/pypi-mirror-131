
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
        replacement_ordinals = Cipher.get_ordinals(replacement)
        if self.are_supported(replacement_ordinals):
            return replacement_ordinals
        else:
            return []

    def get_sanitized_ordinals(self, message: str, replacement: str = DEFAULT_REPLACEMENT) -> []:
        replacement_ordinals = self.get_sanitized_replacement_ordinals(replacement)
        message_ordinals = Cipher.get_ordinals(message)
        sanitized_ordinals = []
        for ordinal in message_ordinals:
            if self.is_supported(ordinal):
                sanitized_ordinals.append(ordinal)
            else:
                sanitized_ordinals.extend(replacement_ordinals)
        return sanitized_ordinals

    def encrypt(self, message: str, replacement: str = '') -> str:
        ordinals = Cipher.get_ordinals(message)
        sanitized_ordinals = self.get_sanitized_ordinals(message, replacement=replacement)
        encrypted_message = []
        last_used_char = ''
        for ordinal in sanitized_ordinals:
            ordinal -= Cipher.MIN_SUPPORTED_ORD
            if ordinal % 2:
                char_set = Cipher.CHAR_SET_ODD
                ordinal = (ordinal - 1) // 2
            else:
                char_set = Cipher.CHAR_SET_EVEN
                ordinal //= 2
            modulo = ordinal % Cipher.MODULO_LENGTH
            quotient = ordinal // Cipher.MODULO_LENGTH
            encrypted_char = char_set[modulo]
            if encrypted_char == last_used_char:
                encrypted_message.append(Cipher.SEPARATOR)
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
            if part[0] in Cipher.CHAR_SET_ODD:
                char_set = Cipher.CHAR_SET_ODD
                even = False
            elif part[0] in Cipher.CHAR_SET_EVEN:
                char_set = Cipher.CHAR_SET_EVEN
                even = True
            else:
                continue
            index = char_set.index(part[0])
            ordinal = index + part[1] * Cipher.MODULO_LENGTH
            ordinal *= 2
            if not even:
                ordinal += 1
            ordinal += Cipher.MIN_SUPPORTED_ORD
            decrypted_message.append(chr(ordinal))
        return ''.join(decrypted_message)

