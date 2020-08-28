from collections import OrderedDict

#
# class Row:
#     def __init__(self, data):
#         self.data = data
#         self.keys = list(data.keys())
#
#     def __iter__(self):
#         print("-")
#         return iter(self.keys)
#
#
# class Basic:
#     def __init__(self):
#         self.__prot = "prot"
#
#     def printin(self):
#         print(self.__prot)
#
#
# class Sub(Basic):
#     def change(self):
#         super().__prot = "abc"
#
#
# if __name__ == "__main__":
#     b = Sub()
#     b.change()
#     b.printin()


class Change:
    def __init__(self):
        self.value = [1, 2, 3]

    def gen(self, pos):
        if len(self.value) < 6:
            print("appending")
            self.value.append(5)
        yield pos

    def __iter__(self):
        return iter([iter(self.gen(p)) for p in self.value])


def y_so(value):
    yield value


class T:
    def __repr__(self):
        return "repr"

    # def __str__(self):
    #     return "str"


if __name__ == "__main__":
    # print(next(y_so("test")))
    t = T()
    print(t)
