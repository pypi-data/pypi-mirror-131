# @Time    : 2018/3/29 上午12:01
# @Author  : Niyoufa

def print_testcase(func):

    def wrapper(self):
        print("{testcase_name} {sub_testcase_name}".format(
            testcase_name = self.__class__.__name__,
            sub_testcase_name = func.__name__
        ))
        func(self)

    return wrapper