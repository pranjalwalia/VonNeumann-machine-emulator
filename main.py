import sys,os
from mathStuff import *

PC = 1
MBR = ""
IR = ""
IBR = ""
MAR = ""
HALT = "1"*40
AC=0
MQ=0

class MemoryOps:
    def __init__(self):
        pass
    
    def init_memory(self):
        element = "0" * 40
        for i in range(1000):
            memory.append(element)
        return

    def set_memory(self):
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
                    print('Found a stand-alone at {}'.format(top))
                else:
                    memory[top] = left+right
                top+=1;
            
            else:
                break

            #! Hardcode Demo => if(a >= b)
            ''' Testing Variables '''
            memory[100] = "0000000000000000000000000000000000000010" #! 2
            memory[101] = "0000000000000000000000000000000000000011" #! 3
            memory[102] = "0000000000000000000000000000000000000101" #! 5
            memory[103] = "1111111111111111111111111111111111111111" #! -1

        f.close()

    def get_memory(self):
        outf = open('output.txt', 'w')
        for line in memory:
            outf.write(line + '\n')
        outf.close()



class IAS:
    def __init__(self):
        pass

    def execute(self):
        global PC; global IBR; global IR ; global MAR ; global MBR; global HALT; global AC; global MQ
        
        #?------------------------BEGIN DATA TRANSFER OPS------------------------------

        #!LOAD M(X)
        if(IR == "00000001"):
            AC = int(bintodec(str(memory[bintodec(MAR)])))
            print("Found the LOAD, LOAD to AC, at !! load: {}".format(int(bintodec(str(memory[bintodec(MAR)])))))

        #! LOAD MQ,MX
        if (IR == "00001001"):
            print('load to the MQ: ' , int(bintodec(str(memory[bintodec(MAR)]))) , 'from:' , int(bintodec(MAR)) )
            MQ = int(bintodec(str(memory[bintodec(MAR)])))

        #! LOAD from MQ
        if(IR=="00001010"):
            print("Load from MQ executed ! at " , int(bintodec(MAR)))
            AC = MQ

        #!STOR M(X)
        if(IR=="00100001"):
            memory[bintodec(MAR)] = num_to_bin(int(AC) , 40) + "  =>  "+ str(AC)
            memory[bintodec(MAR)+2] = num_to_bin(int(MQ) , 40) + "  =>  "+ str(MQ)
            print("Found the STOR , content at {}  => {}".format( bintodec(MAR), memory[bintodec(MAR)]))
            print("stored the MQ two memory slots after AC")

        #!LOAD -M(X)
        if(IR == "00000010"):
            AC = int(bintodec(str(memory[bintodec(MAR)]))); AC*=(-1)

        #!LOAD abs(M(X))
        if(IR == "00000011"):
            AC = abs(int(bintodec(str(memory[bintodec(MAR)]))))
        
        #!LOAD -abs(M(X))
        if(IR == "00000100"):
            AC = int(bintodec(str(memory[bintodec(MAR)]))); AC*=(-1)
        

        #?------------------------END DATA TRANSFER OPS------------------------------



        #? --------------------- BEGIN ARITHMETIC OPS ---------------------------
        #!ADD M(X)
        if(IR == "00000101"):
            AC+=int(bintodec(str(memory[bintodec(MAR)])))
            print("Found the ADD, add: {}".format(int(bintodec(str(memory[bintodec(MAR)])))))
        
        #! ADD abs(M(x))
        if(IR == "00000111"):
            AC+=abs(int(bintodec(str(memory[bintodec(MAR)]))))
            print("Found the abs ADD, add: {}".format(int(memory[bintodec(MAR)])))
        

        #!SUB M(X)
        if(IR=="00000110"):
            AC-=int(bintodec(str(memory[bintodec(MAR)])))
            print("found a subtract operation at {} !!, subtract: {}".format(PC , int(memory[bintodec(MAR)])))
        
        #! Sub |M(x)|
        if(IR=="00001000"):
            AC-=abs(int(bintodec(str(memory[bintodec(MAR)]))))
            print("found a subtract, sub_mod: {}".format(int(memory[bintodec(MAR)])))
        
        #! multiply(m(x)) => m(x)*MQ 
        if(IR == "00001011"):
            print("Found the Multiply ...AC = MQ*M(x).....MQ = {} and M(x)= {}".format(MQ , int(bintodec(str(memory[bintodec(MAR)])))))
            AC = MQ*int(bintodec(str(memory[bintodec(MAR)])))

            res = num_to_bin(AC , 80)
            if(res[:40]!="0000000000000000000000000000000000000000"):
                AC = res[:40]; MQ = res[40:]

        #! div(M(x))
        if(IR=="00001100"):
            if(int(memory[bintodec(MAR)]) == 0):
                AC = -1
                sys.exit("Found a Possible Zero Division Error....Aborting!")
            else:
                #! MQ = AC/int(memory[bintodec(MAR)])   => remember not to divide upto floats 
                MQ = int(AC/int(bintodec(str(memory[bintodec(MAR)]))))
                AC%=(int(bintodec(str(memory[bintodec(MAR)]))))
                print('AC:' , AC); print("MQ:", MQ)
                print("found a divide operation, divide: ".format(int(bintodec(str(memory[bintodec(MAR)])))))
            
        #! LSH
        if(IR == "00010100"):
            AC*=2

        #! RSH
        if(IR=="00010101"):
            AC/=2

        #? --------------------- END ARITHMETIC OPS ---------------------------



        #? --------------------- BEGIN BRANCHING OPS ---------------------------------

        #! Remember not to jump back to a smaller value of PC, it'll drive an infinite loop.

        #! JUMP M(X , 0:19)  => unconditional jump and take next from left...
        if(IR=="00001101"):
            print( 'found the UNCONDITIONAL JUMP Instruction => JUMPING !! MAR:', (MAR))
            x = bintodec(MAR)
            PC = x
        
        #! Conditional left JUMP(X , 0:19)
        if(IR=="00001111"):
            if(AC >= 0):
                print("Found the CONDITIONAL JUMP (jumping) !! MAR:" , MAR)
                x = bintodec(MAR)
                PC = x
            else:
                print("Not Jumping BRUHH!")

        #? --------------------- END BRANCHING OPS -----------------------------------
        print('AC:_' , AC)



    def fetch(self):
        global PC; global IBR; global IR ; global MAR ; global MBR; global HALT; global AC; global MQ
        #! HALT : 1111111111111111111111111111111111111111
        while(True):
            if(IBR==""):           # only left instruction remaining..
                MAR = str(PC)
                MBR = memory[int(MAR)]
                if(MBR==HALT):
                    print('found the HALT instruction at {}....exitting!'.format(PC))
                    #! sys.exit("Exitting after HALT Invoked...")   => this stops file IO
                    break
                left = MBR[:20]; right = MBR[20:]
                lopcode = left[:8]; ropcode = right[:8]
                laddress = left[8:]; raddress = right[8:]
                try:
                    # print(bintodec(laddress) , bintodec(raddress))
                    pass
                except:
                    print("Check the instructions and run again" , left , right)
                print()

                if(lopcode=="00000000" and ropcode != "00000000"):
                    print('Found a standalone Instruction at {}'.format(PC))
                    IR = ropcode; 
                    MAR = raddress
                    PC+=1
                    IAS.execute(self); print("Executing...")
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
                print('IBR:_ ' , IBR)
                print('Opcode:_' , IBR_opcode)
                print('Address:_' , IBR_addr)
                IBR = ""
                print()
                PC+=1
            IAS.execute(self); print("Executing...")



if __name__ == "__main__":
    memory = []
    memoryInstance = MemoryOps()
    machine = IAS()
    memoryInstance.init_memory()
    memoryInstance.set_memory()
    print()
    print()
    machine.fetch()
    memoryInstance.get_memory()
    print()
    print()
    print()
    print("Ending the Program, Check 'output.txt' for the Input Instructions, Data , Output")
    print()
    print("Locating the data in the output.txt can be a challenge because of 1000 lines,\nTherefore it is advisable to set numbering of lines if in vim")
    print()
    print('Note that the memory has zero based indexing! So if output is stored at 100, it will appear at line number 101 in output.txt')
    print("The same holds for anything written to Memory..")
    print('final content of AC:' , AC)
    print('final content of MQ:' , MQ)
