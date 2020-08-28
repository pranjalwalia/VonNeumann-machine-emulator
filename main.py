import sys,os

PC = 1
MBR = ""
IR = ""
IBR = ""
MAR = ""
HALT = ""
AC=0

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



def execute():
    pass



def fetch():
    global PC; global IBR; global IR ; global MAR ; global MBR; global HALT; global AC
    # print(PC); print(HALT);       # HALT : 1111111111111111111111111111111111111111
    while(True):
        if(IBR==""):           # only left instruction remaining..
            MAR = str(PC)
            MBR = memory[int(MAR)]
            # print(MAR)
            # print(PC)
            # print(MBR)
            if(MBR==HALT):
                print('found the halt instruction at {}'.format(PC))
                break
            left = MBR[:20]; right = MBR[20:]
            lopcode = left[:8]; ropcode = right[:8]
            laddress = left[8:]; raddress = right[8:]
            print(bintodec(laddress) , bintodec(raddress))
            print('-- first --')
            print()

            if(lopcode=="00000000" and ropcode != "00000000"):
                print('found a standalone at {}'.format(PC))
                IR = ropcode; MAR = raddress
                execute()
                PC+=1; continue
            else:
                IBR = right
                IR = lopcode; MAR = laddress
        
        else:
            IR = lopcode
            MAR = laddress
            IBR = ""
            print(bintodec(laddress) , bintodec(raddress))
            print('-- second --')
            print()
            PC+=1

        execute()

    '''
    while(True):
        if(IBR==""):
            MAR = str(PC)
            MBR = memory[int(MAR)]
    '''


def get_memory():
    outf = open('out.txt', 'w')
    for line in memory:
        if(len(line) < 20):
            print(int(line))
        outf.write(line + '\n')
    outf.close()
    return


if __name__ == "__main__":
    memory = []
    init_memory()
    make_halt()
    # print(HALT)
    set_memory()
    '''
    for i in range(10):
        if(memory[i]==HALT):
            print("found the halt" ,memory[i])
        else:
            print(memory[i])
    '''
    get_memory()
    print()
    print()
    fetch()
