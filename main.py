import sys,os

PC = 0
MBR = ""
IR = ""
IBR = ""
MAR = ""
HALT = ""
AC=0
MQ=0

def make_halt():
    global HALT;
    for i in range(20):
        HALT+="1"
    for i in range(20):
        HALT+="1"

def bintodec(n):
    return int(n,2)


def init_memory():
    element = "0" * 40
    for i in range(1001):
        memory.append(element)
    return


def set_memory():
    f = open('input.txt', 'r'); 
    top=1;
    for line in f:
        if len(line)!=0:
            left, right = line.split(); left = str(left); right = str(right)

            lopcode = left[:8]; ropcode = right[:8]
            laddress = left[8:]; raddress = right[8:]

            # check for stand-alone instruction, if lop gets some assigned opcode and rop remains initial value => stand-alone => store in the right
            if(lopcode != '00000000' and ropcode == '00000000'):
                memory[top]=right+left
                # print('found a stand-alone at {}'.format(top))
            else:
                memory[top] = left+right
            top+=1;
        
        else:
            break
        #Hardcode demo
        memory[16] = "20"; memory[17] = "2"; memory[18] = "10"; memory[19] = "1"; memory[20] = "-1";
        memory[100] = "2"; memory[101] = "3" ; memory[200]="0"

    f.close()

'''
LOAD M(x) Add M(x)
Stor M(x) Add M(x)
JUMP (x,left) Sub M(x)
Halt()
'''



def execute():
    global PC; global IBR; global IR ; global MAR ; global MBR; global HALT; global AC; global MQ
    
    #?------------------------BEGIN DATA TRANSFER OPS------------------------------
    #!LOAD M(X)
    if(IR == "00000001"):
        AC = int(memory[bintodec(MAR)])
        print("Found the LOAD Instruction at {} !! load: {}".format(PC , int(memory[bintodec(MAR)])))

    #! LOAD MQ,MX
    elif("00001001"):
        MQ = int(memory[bintodec(MAR)])
        
    #! LOAD MQ
    elif(IR=="00001010"):
        AC = MQ


    #!STOR M(X)
    elif(IR=="00100001"):
        memory[bintodec(MAR)] = str(AC)
        print("Found the STOR at {}!! content at {}  => {}".format( PC, bintodec(MAR), memory[bintodec(MAR)]))

    #!LOAD -M(X)
    if(IR == "00000010"):
        AC = int(memory[bintodec(MAR)]); AC*=(-1)

    #!LOAD abs_M(X)
    if(IR == "00000011"):
        AC = abs(int(memory[bintodec(MAR)]))
    
    #!LOAD -abs_M(X)
    if(IR == "00000100"):
        AC = abs(int(memory[bintodec(MAR)])); AC*=(-1)
    

    #?------------------------END DATA TRANSFER OPS------------------------------



    #? --------------------- BEGIN ARITHMETIC OPERATIONS ---------------------------
    #!ADD M(X)
    elif(IR == "00000101"):
        AC+=int(memory[bintodec(MAR)])
        print("Found the ADD Instruction at {} !! add: {}".format(PC , int(memory[bintodec(MAR)])))
    
    #! ADD abs(M(x))
    elif(IR == "00000111"):
        AC+=abs(int(memory[bintodec(MAR)]))
        print("Found the abs ADD Instruction at {} !! add: {}".format(PC , int(memory[bintodec(MAR)])))
    

    #!SUB M(X)
    elif(IR=="00000110"):
        AC-=int(memory[bintodec(MAR)])
        print("found a subtract operation at {} !!, subtract: {}".format(PC , int(memory[bintodec(MAR)])))
    
    #! Sub |M(x)|
    elif(IR=="00001000"):
        AC-=abs(int(memory[bintodec(MAR)]))
        print("found a subtract operation at {} !!, subtract: {}".format(PC , int(memory[bintodec(MAR)])))
    
    #! div(M(x))
    elif(IR=="00001100"):
        MQ = AC/int(memory[bintodec(MAR)])
        AC%=(int(memory[bintodec(MAR)]))
        print("found a subtract operation at {} !!, subtract: {}".format(PC , int(memory[bintodec(MAR)])))
    
    #! LSH
    elif(IR == "00010100"):
        AC*=2

    #! RSH
    elif(IR=="00010101"):
        AC/=2

    #? --------------------- END ARITHMETIC OPERATIONS ---------------------------



    #TODO:  UNDER_DEVELOPMENT_Branching
    #! Remember not to jump back to a smaller value, it'll drive an infinite loop.

    #? --------------------- BEGIN BRANCHING OPS ---------------------------------

    #! JUMP M(X , 0:19)  => unconditional jump and take next from left...
    elif(IR=="00001101"):
        print( 'found the JUMP Instruction!! MAR:', (MAR))
        x = bintodec(MAR)
        PC = x-1
        print("x : " , x)
        # pass
        # PC = int(memory(bintodec(MAR)))
    #? --------------------- END BRANCHING OPS -----------------------------------
    
    print('AC:_' , AC)



def fetch():
    global PC; global IBR; global IR ; global MAR ; global MBR; global HALT; global AC; global MQ
    # print(PC); print(HALT);       # HALT : 1111111111111111111111111111111111111111
    while(True):
        if(IBR==""):           # only left instruction remaining..
            MAR = str(PC)
            MBR = memory[int(MAR)]
            # print(MAR)
            print("PC:_" , PC)
            # print(MBR)
            if(MBR==HALT):
                print('found the halt instruction at {}'.format(PC))
                sys.exit("Exitting after HALT Invoked...")
                break
            left = MBR[:20]; right = MBR[20:]
            lopcode = left[:8]; ropcode = right[:8]
            laddress = left[8:]; raddress = right[8:]
            print('-- first --')
            try:
                print(bintodec(laddress) , bintodec(raddress))
            except:
                print("We fucked up!!" , left , right)
            print()

            if(lopcode=="00000000" and ropcode != "00000000"):
                print('found a standalone at {}'.format(PC))
                IR = ropcode; 
                MAR = raddress
                PC+=1
                execute()
                # PC+=1 
                continue
            else:
                IBR = right
                IR = lopcode; 
                MAR = laddress
            print("IBR:_" , IBR)
            print()
        
        else:
            IBR_opcode = IBR[:8]
            IBR_addr = IBR[8:]
            IR = IBR_opcode
            MAR = IBR_addr
            print('-- second --')
            print('IBR:_' , IBR)
            print('opcode:_' , IBR_opcode)
            print('adrr:_' , IBR_addr)
            IBR = ""
            print(bintodec(laddress) , bintodec(raddress))
            print()
            PC+=1
        execute()


def get_memory():
    outf = open('out.txt', 'w')
    for line in memory:
        # if(len(line) < 20):
        #     print(int(line))
        outf.write(line + '\n')
    outf.close()
    return


if __name__ == "__main__":
    memory = []
    init_memory()
    make_halt()
    set_memory()
    print()
    print()
    fetch()
    get_memory()

