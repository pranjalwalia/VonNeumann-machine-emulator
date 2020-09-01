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

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

# binary_string = '1111' # or whatever... no '0b' prefix
binary_string1 = "000001100100"
binary_string2 = "000001100101"
binary_string3 = "000011001000"
binary_string4 = "1111111111111111111111111111111111111111"

'''
print(twos_comp(binarytodecimal(binary_string1) , len(binary_string1)))
print(binarytodecimal(binary_string1))
print(twos_comp(binarytodecimal(binary_string2) , len(binary_string2)))
print(binarytodecimal(binary_string2))
print(twos_comp(binarytodecimal(binary_string3) , len(binary_string3)))
print(binarytodecimal(binary_string3))
print(twos_comp(binarytodecimal(binary_string4) , len(binary_string4)))
'''

# print(binarytodecimal('000001100100'))
# print(binarytodecimal('000001100101'))
# print(binarytodecimal('000011001000'))


'''  
0000000000000000000000000000000000000010  #! => 2
0000000000000000000000000000000000000011 #! 3
0000000000000000000000000000000000000101 #! 5
'''

def num_to_bin(num, wordsize):
    if num < 0:
        num = 2**wordsize+num
    base = bin(num)[2:]
    padding_size = wordsize - len(base)
    return '0' * padding_size + base

print(num_to_bin(-1 , 40))
print(num_to_bin(-2 , 40))
print(num_to_bin(-3 , 40))
print(num_to_bin(3 , 40))



