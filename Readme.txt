Pranjal Walia
IMT2019062

-- The project is a submission for ComputerArch. Assignment 1
-- An emulation of the IAS Instruction Set, implemented using python3.x

-- Project Core Structure:
    -- main.py
    -- input.txt, output.txt
    -- *.idea file(s)
    -- *.example file(s)

-- main.py => The main entry point to the program and contains the entire implementation.    
-- input.txt => main.py will open this file in run-time to fetch the machine code.
-- output.txt => the entire memory structure of the IAS computer is printed in this, i.e an array of 40 bit per field.
-- <filename>.idea and <filename>.example are analogoues of each other,
        -- <filename>.idea => contains the code that is to be emulated
        -- <filename>.example => contains the machine code that is going to be used to run main.py

REQUIREMENTS:
    -- Preferebly run on a linux distribution (ubuntu/fedora etc) as we will be using some terminal commands to pass in the machine code
    -- Installed version of python3.x 


RUNNING COMMANDS:
    -- Inside the Project Directory:
        -$ cat fileName.idea => appends to the terminal an overview of the instruction you are about to implement using the IAS. (---OPTIONAL---)
        -$ cat fileName.example > input.txt
        -$ python3 main.py

        Example 1: Implements a simple if/else program with some basic ALU operations.
            $ cat prog1.idea                     
            $ cat prog1.example > input.txt
            $ python3 main.py

        Example 2: Checks if a number is Odd or Even and performs corresponding ALU operations.
            $ cat prog3.idea                     
            $ cat prog3.example > input.txt
            $ python3 main.py

        -- Other example codes should also be executed in the above fashion.


Important Stuff to Remember !
    -- ! Make Sure that the contents of *.example files are not changed.
    -- ! It is preffered to use the cat command to copy the ".example" files into "input.txt",
            because any Additional Spaces in the end of file in input.txt after copying will cause the program to crash,
            or any change in the machine code that disrupts the HALT() instruction (at End of file) will cause an Infinite Loop.
    -- ! Make sure that the ".idea" and ".example" currently being tested have the same name.


Description:
    -- The project is broadly divided into two parts:
        ! main.py: 
            The main module where the IAS machine resides, all the relevant methods of the machine can be found here.
                class IAS:
                    -- fetch_cycle() 
                    -- execute_cycle()

                class MemoryOps:
                    -- contains the relevent memory operations such as initialise_memory, set_memory , get_final_memory

        ! mathStuff.py
            -- contains functions relevant for all the conversions of two's compliment binary strings to decimal and vice-versa,
                for the purpose of calculations and memory_addressing, 
                    this is implemented seperately as it is not relevant to the working procedure of the IAS machine.
            -- These are used throughout the entire program to encode and decode input/output values or addresses/data.

Implementation Details:
    -- Details about the execution are printed on the terminal as the program executes to follow along.
    -- Final memory will be visible in output.txt after successfull execution of the entire program.
    
    Assumptions and Overview of the Memory:
        -- Memory slot with 40 bit string of zeros is considered as empty.

        -- Since operations like Multiply and Divide use the MQ along with AC
            => I have slightly modified the STOR(M(x)) instruction to make it easier to visualise the demo.
            => The STOR(M(x) stores the AC at M(x) and also stores the MQ at M(x+2), this is done consiously to help with the demo and not a bug,
                I hope I will not be penalised for this :)

        -- Memory starts at index 0 and PC starts at 1, therefore the first row in memory is always empty.

        -- The memory is an array of 1000 strings(40 bit each), after execution, the final state of the memory shall be written into output.txt.

        -- Instructions are stored from index 1 in the memory onwards upto the 100th index(Assumed limit for the Demo).

        -- The Input data i.e the hardcoded variables are stored in the addresses starting from index 100 upto 103, these will be used in the ALU operations.

        -- The output of the program is stored as binary 40 bit (2's compliment) numbers at the location of 205 or 201
                        (This final output index can be found the corresponding .idea of the program you are executing)

        -- The Instruction "1111111111111111111111111111111111111111", is assumed as the HALT instruction, therefore the HALT shall take up an entire 40 bit row in memory.

        -- Although the multiply instruction stores the "Most significant 40 bits" in AC and remaining 40 in MQ,
                        this implementation does this instruction only if the output number in binary cannot be represented in 40 bits.

    class MemoryOps:
        -- init_memory() => this method initialises the memory as a 1000x40 grid.
        -- set_memory() => this method copies the (instructions specified in input.txt + the hardcoded variable data ) and feeds them starting from index 1 in memory.
        -- get_memory() => this method prints the final state of the memory after execution in output.txt

    class IAS:
        -- fetch_cycle():
            --A regular fetch cycle works exactly as specified in the flow-chart, listed below are some things specific to the implementation of this program:
                Things to note about this Implementation:
                    1. Current fetch_cycle implementation always fetches instructions from left to right in a memory slot.
                    2. If a "Stand Alone" instruction is found in memory, the instruction is stored in the right half (as specified in the flow-chart) and the left half stays empty (i.e zeros) the fetch cycle skips the empty instruction and picks up the right.
                    3. Special case:
                        Instruction of the form : [JUMP] , [SOME OPERATION]
                            -- Fetch cycle will not immediately jump on encountering the JUMP, first the Right instruction shall be copied in the IBR,
                                and only then will JUMP be executed first in the execute cycle.


        -- execute_cycle():
            -- A regular exectue cycle as specified in the flow-chart, after a single fetch_cycle; IR, MAR, MBR, IBR all are loaded with the necessary inputs.
            -- The execute_cycle starts by decoding the Instruction Opcode and the respective addresses as specified in the machine code.
            -- Prompts are also printed in the terminal at the execution of every instruction to help understand the functioining of the machine.
            -- The execute cycle consists of 17 implemented instructions out of the 21.

            Note on the divide and multiply instructions:
                Multiply and divide use the AC and MQ together so in case of these operations, 
                The output of both of these is written in the memory at adjacent positions.