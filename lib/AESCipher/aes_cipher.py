# https://gitlab.com/Microeinstein/panopto-sync/-/blob/master/aes_cipher.py

import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher:
    _rnd = Random.new()

    def __init__(self, key: str or bytes):
        if isinstance(key, str):
            key = key.encode()
        self.key = hashlib.sha256(key).digest()

    def encrypt(self, raw: bytes) -> bytes:
        raw = self._pad(raw)
        check = hashlib.sha256(raw).digest()
        iv = AESCipher._rnd.read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        data = cipher.encrypt(raw)
        return base64.b64encode(check + iv + data)

    def decrypt(self, enc: bytes) -> bytes:
        enc = base64.b64decode(enc)
        check = enc[:32]
        iv = enc[32:32 + AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        dec = cipher.decrypt(enc[32 + AES.block_size:])
        if check != hashlib.sha256(dec).digest():
            raise ValueError("Invalid key")
        return self._unpad(dec)

    def encrypt_text(self, text: str) -> str:
        return self.encrypt(text.encode()).decode()

    def decrypt_text(self, enc: str) -> str:
        return self.decrypt(enc.encode()).decode()

    @staticmethod
    def _pad(s: bytes) -> bytes:
        data: int = AES.block_size - len(s) % AES.block_size
        return s + data * bytes([data])

    @staticmethod
    def _unpad(s: bytes) -> bytes:
        return s[: -ord(s[len(s) - 1:])]
