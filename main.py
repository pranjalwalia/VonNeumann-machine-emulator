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
                print('found a stand-alone at {}'.format(top))
            else:
                memory[top] = left+right
            top+=1;
        
        else:
            break

        #Hardcode demo
        memory[16] = "20"; memory[17] = "2"; memory[18] = "10"; memory[19] = "1"; memory[20] = "-1";

    f.close()


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
    set_memory()
    get_memory()

