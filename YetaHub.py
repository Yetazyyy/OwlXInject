
import base64
import zlib
import time
import sys
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256

def deobfuscate_string(s, key=0x42):
    return ''.join(chr(b ^ key) for b in base64.b64decode(s))

def aes_decrypt(enc_data, key):
    iv = enc_data[:16]
    ct = enc_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), 16)

def anti_debug():
    if sys.gettrace() is not None:
        print("Debugger terdeteksi! Program keluar.")
        sys.exit(1)
    suspicious_vars = ['PYTHONINSPECT', 'PYTHONDEBUG']
    for var in suspicious_vars:
        if os.getenv(var):
            print("Lingkungan mencurigakan terdeteksi! Program keluar.")
            sys.exit(1)

anti_debug()

encoded_obf = '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'

max_attempts = 3

for attempt in range(max_attempts):
    secret = input("Masukkan kunci rahasia untuk dekripsi: ").encode('utf-8')
    if len(secret) < 8:
        print("Kunci terlalu pendek, minimal 8 karakter.")
        continue

    try:
        encoded = deobfuscate_string(encoded_obf)
        data = base64.b64decode(encoded)
        salt = data[:16]
        encrypted = data[16:]

        key = PBKDF2(secret, salt, dkLen=16, count=100000, hmac_hash_module=SHA256)

        decompressed = zlib.decompress(aes_decrypt(encrypted, key))
        exec(decompressed.decode('utf-8'))
        break
    except Exception:
        print("Kunci salah atau data rusak.")
        if attempt < max_attempts - 1:
            print("Coba lagi...")
            time.sleep(2)
        else:
            print("Percobaan habis. Program keluar.")
            sys.exit(1)
