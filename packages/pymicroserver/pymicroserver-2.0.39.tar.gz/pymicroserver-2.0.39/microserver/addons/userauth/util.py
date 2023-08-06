# @Time    : 2018/6/15 15:30
# @Author  : Niyoufa
import re, sys, six
from importlib import import_module
from microserver.utils.crypto import get_random_string
from microserver.conf import settings

UNUSABLE_PASSWORD_PREFIX = '!'  # This will never be a valid encoded hash
UNUSABLE_PASSWORD_SUFFIX_LENGTH = 40  # number of random chars to add after UNUSABLE_PASSWORD_PREFIX


def check_mobile(mobile):
    phoneprefix = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '150', '151', '152', '153',
                   '156', '158', '159', '170', '183', '182', '185', '186', '188', '189']
    if len(mobile) != 11:
        raise Exception("手机号必须是11位数字！")
    else:
        if mobile.isdigit():# 检测输入的号码是否全部是数字。
            if mobile[:3] not in phoneprefix:# 检测前缀是否是正确。
                raise Exception("手机号无效！")
        else:
            raise Exception("手机号必须是数字！")

def check_email(email):
    if len(email) < 5:
        raise Exception("邮箱长度错误")
    elif re.match("[a-zA-Z0-9]+\@+[a-zA-Z0-9\-]+\.+[a-zA-Z]", email) == None:
        raise Exception("邮箱格式错误")

def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        msg = "%s doesn't look like a module path" % dotted_path
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        msg = 'Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])


def get_hashers():
    hashers = []
    for hasher_path in settings.USERAUTH["PASSWORD_HASHERS"]:
        hasher_cls = import_string(hasher_path)
        hasher = hasher_cls()
        if not getattr(hasher, 'algorithm'):
            raise Exception("hasher doesn't specify an "
                                       "algorithm name: %s" % hasher_path)
        hashers.append(hasher)
    return hashers

def get_hashers_by_algorithm():
    return {hasher.algorithm: hasher for hasher in get_hashers()}

def get_hasher(algorithm='default'):
    """
    Returns an instance of a loaded password hasher.

    If algorithm is 'default', the default hasher will be returned.
    This function will also lazy import hashers specified in your
    settings file if needed.
    """
    if hasattr(algorithm, 'algorithm'):
        return algorithm

    elif algorithm == 'default':
        return get_hashers()[0]

    else:
        hashers = get_hashers_by_algorithm()
        try:
            return hashers[algorithm]
        except KeyError:
            raise ValueError("Unknown password hashing algorithm '%s'. "
                             "Did you specify it in the PASSWORD_HASHERS "
                             "setting?" % algorithm)

def make_password(password, salt=None, hasher='default'):
    """
    Turn a plain-text password into a hash for database storage

    Same as encode() but generates a new random salt.
    If password is None then a concatenation of
    UNUSABLE_PASSWORD_PREFIX and a random string will be returned
    which disallows logins. Additional random string reduces chances
    of gaining access to staff or superuser accounts.
    See ticket #20079 for more info.
    """
    if password is None:
        return UNUSABLE_PASSWORD_PREFIX + get_random_string(UNUSABLE_PASSWORD_SUFFIX_LENGTH)
    hasher = get_hasher(hasher)

    if not salt:
        salt = hasher.salt()

    return hasher.encode(password, salt)