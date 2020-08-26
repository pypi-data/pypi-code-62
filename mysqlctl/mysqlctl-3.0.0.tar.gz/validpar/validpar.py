import validus


class CheckParams:
    error_list = []

    def __init__(self):
        pass

    def _check_params(self, params, rule, msg=None):
        func = getattr(validus, rule)
        if not func(params):
            if msg:
                self.error_list.append(msg)
            else:
                self.error_list.append(f"Failed {rule} verification")

    def check(self, args):
        for arg in args:
            if len(arg) == 2:
                self._check_params(arg[0], arg[1])
            elif len(arg) == 3:
                self._check_params(arg[0], arg[1], arg[2])

    def err_first_string(self):
        if len(self.error_list):
            return self.error_list[0]
        return []

    def err_strings(self):
        return self.error_list


# example
# ck = CheckParams()
# ck.check([
#     ['@a.com', 'isemail'],
#     ['asdfas', 'isphone', '手机号码错误'],
#     ['13.5', 'isfloat'],
#     ['28', 'isint'],
#     ['192.168.1.52', 'isip', '不是ip ']
# ])
#
#
# print(ck.err_first_string())
# print(ck.err_strings())

# 支持以下验证
"""
isascii()
isprintascii()
isnonempty()
isbase64()
isemail()
ishexadecimal()
isint()
isfloat()
ispositive()
isslug()
isuuid()
isuuid3()
isuuid4()
isuuid5()
isfullwidth()
ishalfwidth()
islatitude()
islongitude()
ismac()
ismd5()
issha1()
issha256()
issha512()
ismongoid()
isiso8601()
isbytelen()
isipv4()
isipv6()
isip()
isport()
isdns()
isssn()
issemver()
ismultibyte()
isfilepath()
isdatauri()
isjson()
istime()
isurl()
iscrcard()
isisin()
isiban()
ishexcolor()
isrgbcolor()
isphone()
isisbn()
isisbn10()
isisbn13()
isimei()
ismimetype()
isisrc()
"""