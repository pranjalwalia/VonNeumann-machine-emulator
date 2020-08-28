# for i in range(10):
#     x,y = input().split()
#     x = int(x)
#     y = str(y)
#     print(type(x))
#     print(type(y))
# f = open('input.txt' , 'r')
# for i in f:
#     if(len(i)!=0):
#         x, y = i.split()
#         x = int(x)
#         y = str(y)
#         print(str(x) + " " + y)
#     else:
#         break
# f.close()
def binarytodecimal(n):
    return int(n,2)
print(binarytodecimal('000001100100'))
print(binarytodecimal('000001100101'))
print(binarytodecimal('000011001000'))