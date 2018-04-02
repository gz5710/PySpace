# from abc import ABC, abstractmethod

# class AbsClass(ABC):

#     @abstractmethod
#     def do_sth(self):
#         print('Do something')
#         return 'Do something'
    
# class ImplClass(AbsClass):
#     def do_sth(self):
#         print('Do something in Impl')
#         return f'{super().do_sth()}-Do something in Impl'

# x = ImplClass()
# r = x.do_sth()
# print(r)

from decimal import Decimal

i = int(1)
s = str('str')
d = Decimal('27.23')

print(type(i).__name__)
print(type(s).__name__)
print(type(d).__name__)