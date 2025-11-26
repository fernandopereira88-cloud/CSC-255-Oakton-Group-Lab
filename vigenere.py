"""
This module provide functions for Vigenère encryption.
Reference: https://www.youtube.com/watch?v=RCkGauRMs2A&t=115s

Functions:
    encrypt(pwd: str) -> str: encrypt given text and return the encrypted string
    decrypt(encrypted: str) -> str: decrypt the given encrypted text and return the original string
"""

# The set of characters allowed by our encryption algorithm.
# It includes letters, numbers, punctuation, and space (US keyboard).
ALPHABET = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789 !@#$%^&*()-=[]\\;',./`_+{}|:\"<>?~"
)
ALPHABET_SIZE = len(ALPHABET)

# Master key is a user's master password. As this program only assumes one user the master
# key is hard coded for now. Improvements could be made to allow for multiple users.
MASTER_KEY = "MyVerySecureVaultKey123"
MASTER_KEY_INDICES = [ALPHABET.index(c) for c in MASTER_KEY]
MASTER_KEY_LEN = len(MASTER_KEY_INDICES)


def encrypt(pwd: str) -> str:
    """Encrypt the given text using the Vigenère cipher with the given key.
    The Vigenère encryption formula: C_i = (P_i + K_i) mod N.
    Unsupported characters are left unchanged.

    Input: The original string to be encrypted.
    Output: The encrypted string.
    """
    encrypted = []

    for i, char in enumerate(pwd):
        try:
            p_idx = ALPHABET.index(char)
        except ValueError:
            encrypted.append(char)
            continue
        k_idx = MASTER_KEY_INDICES[i % MASTER_KEY_LEN]
        c_idx = (p_idx + k_idx) % ALPHABET_SIZE
        encrypted.append(ALPHABET[c_idx])

    return "".join(encrypted)


def decrypt(encrypted: str) -> str:
    """Decrypt the given encrypted text using the Vigenère cipher with the given key.
    The Vigenère decryption formula: P_i = (C_i - K_i) mod N.
    Unsupported characters are left unchanged.

    Input: The encrypted string to be decrypted.
    Returns: The decrypted string.
    """
    decrypted = []

    for i, char in enumerate(encrypted):
        try:
            c_index = ALPHABET.index(char)
        except ValueError:
            decrypted.append(char)
            continue
        k_index = MASTER_KEY_INDICES[i % MASTER_KEY_LEN]
        p_index = (c_index - k_index) % ALPHABET_SIZE
        decrypted.append(ALPHABET[p_index])

    return "".join(decrypted)


if __name__ == "__main__":
    password = "Oakton255FallSem!"

    encrypted = encrypt(password)
    decrypted = decrypt(encrypted)
    assert decrypted == password

    print(f"{password  = }")
    print(f"{encrypted = }")
    print(f"{decrypted = }")
