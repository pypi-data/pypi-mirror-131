# @Time    : 2018/5/4 14:58
# @Author  : Niyoufa
import numpy

def get_tmp_dir(filename, body):
    if isinstance(body, bytes):
        mode = "wb"
    else:
        mode = "w"
    tmp_dir = "/tmp/%s" % filename
    with open(tmp_dir, mode) as f:
        f.write(body)
    return tmp_dir

# JSON序列化对象
def strongdumps(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, dict) or isinstance(v, list):
                strongdumps(v)
            if isinstance(v, numpy.int) or isinstance(v, numpy.int8) or isinstance(v, numpy.int16)\
                    or isinstance(v, numpy.int32) or isinstance(v, numpy.int64):
                obj[k] = int(v)
            if isinstance(v, numpy.float) or isinstance(v, numpy.float16) \
                    or isinstance(v, numpy.float32) or isinstance(v, numpy.float64)\
                    or isinstance(v, numpy.float128):
                obj[k] = float(v)
            if isinstance(v, numpy.ndarray):
                obj[k] = list(v)
    elif isinstance(obj, list):
        i = 0
        for s in obj:
            if isinstance(s, dict) or isinstance(s, list):
                obj[i] = strongdumps(s)
            if isinstance(s, numpy.int) or isinstance(s, numpy.int8) or isinstance(s, numpy.int16)\
                    or isinstance(s, numpy.int32) or isinstance(s, numpy.int64):
                obj[i] = int(s)
            if isinstance(s, numpy.float) or isinstance(s, numpy.float16) \
                    or isinstance(s, numpy.float32) or isinstance(s, numpy.float64)\
                    or isinstance(s, numpy.float128):
                obj[i] = float(s)
            if isinstance(s, numpy.ndarray):
                obj[i] = list(s)

            i += 1
    return obj

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

def is_chinese_string(ustring):
    """判断一个字符串是否包含汉字"""
    flag = False
    res_map = map(is_chinese,ustring)
    for obj in res_map:
        if obj == True:
            flag = True
            break
    return flag