_a = input("请输入第一个数：")
_b = input("请输入第二个数：")
_c = input("请输入第三个数：")
_c = float(_c)
_a = float(_a)
_b = float(_b)
if _a > _b and _a > _c:
    print(_a)
elif _b > _c:
    print(_b)
else :
    print(_c)
