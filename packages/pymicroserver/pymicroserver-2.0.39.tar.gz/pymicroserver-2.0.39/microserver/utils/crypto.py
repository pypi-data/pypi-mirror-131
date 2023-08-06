# @Time    : 2018/4/2 下午8:43
# @Author  : Niyoufa
import random
import hashlib
import time
import base64
import re

# Use the system PRNG if possible
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    import warnings
    warnings.warn('A secure pseudo-random number generator is not available '
                  'on your system. Falling back to Mersenne Twister.')
    using_sysrandom = False

def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """
    Return a securely generated random string.
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    if not using_sysrandom:
        # This is ugly, and a hack, but it makes things better than
        # the alternative of predictability. This re-seeds the PRNG
        # using a value that is hard for an attacker to predict, every
        # time a random string is required. This may change the
        # properties of the chosen random sequence slightly, but this
        # is better than absolute predictability.
        random.seed(
            hashlib.sha256(
                ('%s%s%s' % (random.getstate(), time.time(), "")).encode()
            ).digest()
        )
    return ''.join(random.choice(allowed_chars) for i in range(length))


def get_random_secret_key():
    """
    返回长度为50的随机字符串，作为文件的SECRET_KEY
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(50, chars)

def md5(mingwen):
    """MD5"""
    m = hashlib.md5()
    mdr_str = mingwen.encode()
    m.update(mdr_str)
    ciphertext = m.hexdigest()
    return ciphertext

def base64encrypt(content):
    """base64加密"""
    b_content = content.encode("utf-8")
    b_base64_content = base64.encodebytes(b_content)
    base64_content = b_base64_content.decode("utf-8")
    return base64_content

def base64decrypt(content):
    """base64解密"""
    b_base64_content = content.encode("utf-8")
    b_content = base64.decodebytes(b_base64_content)
    origin_text = b_content.decode("utf-8")
    return origin_text

def remove_punctuation(text, punctuation='，！？：;。“”‘’、,!?:;."\"\'`',extend_str=""):
    """去除文本标点符号"""
    punctuation = punctuation + extend_str
    text = re.sub(r'[{}]+'.format(punctuation), '', text)
    return text.strip()

def random_str(randomlength=8):
    """随机生成指定长度字符串"""
    from random import Random
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

def sha1(mingwen):
    sha1 = hashlib.sha1()
    sha1.update(mingwen.encode())
    miwen = sha1.hexdigest()
    return miwen