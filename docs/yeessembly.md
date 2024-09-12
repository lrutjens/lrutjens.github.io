###### Version 1.0

## Operator Codes

There are 8 possible operators, with the final one up to the CPU designer

1. Add
2. Subtract
3. Multiply
4. Divide
5. Move Pointer
6. Conditional
7. Write
8. ???

---

 - Add:
    
    [000][XX][X][XX][X] [XXXXXXXX XXXXXXXX] [XXXXXXXX XXXXXXXX]
    
    [Add Operator][Read RAM/ROM/Cache for num 1][Start at beginning or pointer][Read RAM/ROM/CACHE][Start at beginning or pointer] [Num 1 offset] [Num 2 offset]

 - Subtract:
    
    [001][XX][X][XX][X] [XXXXXXXX XXXXXXXX] [XXXXXXXX XXXXXXXX]
    
    [Subtract Operator][Read RAM/ROM/Cache for num 1][Start at beginning or pointer][Read RAM/ROM/CACHE][Start at beginning or pointer] [Num 1 offset] [Num 2 offset]

 - Multiply:
    
    [010][XX][X][XX][X] [XXXXXXXX XXXXXXXX] [XXXXXXXX XXXXXXXX]
    
    [Multiply Operator][Read RAM/ROM/Cache for num 1][Start at beginning or pointer][Read RAM/ROM/CACHE][Start at beginning or pointer] [Num 1 offset] [Num 2 offset]

 - Divide:
    
    [011][XX][X][XX][X] [XXXXXXXX XXXXXXXX] [XXXXXXXX XXXXXXXX]
    
    [Add Operator][Read RAM/ROM/Cache for num 1][Start at beginning or pointer][Read RAM/ROM/CACHE][Start at beginning or pointer] [Num 1 offset] [Num 2 offset]

 - Move Pointer:
    
    [100][XX][X][00] [XXXXXXXX XXXXXXXX]
    
    [Move Pointer Operator][RAM/ROM/Display][Beginning/Pointer][Empty] [Offset]

 - Conditional:
    
    [101][X][X][X][X][0] [XXXX][0000] [XXXXXXXX XXXXXXXX] [XXXXXXXX XXXXXXXX] [XXXXXXXX XXXXXXXX] [XXXXXXXX XXXXXXXX]
    
    [Conditional Operator][Read first from RAM/ROM][Read first from pointer or beginning][Read second from RAM/ROM][Read second from pointer or beginning]  [Type of Conditional]    [First comparison offset]  [Second comparison offset]  [Rom adress if true]  [Rom adress if false]

 - Write:
    
    [110][XX][X][X][X] [XXXXXXXX XXXXXXXX] [XXXXXXXX XXXXXXXX]
    
    [Write Operator][Read Cache/ROM/RAM][Read from beginning/pointer][Write to RAM/Graphics RAM][Write to beginning/pointer]    [Read offset]   [Write offset]

###### All operators write an output to the cache, solutions for arithmatic, and a 1 for anyting else

---

## Keywords

You can write in yeessembly and convert it to pinary with the yeessembler

Syntax is as follows:

 - BEG - Beginning of memory

 - PNT - Pointer location

 - 0xNum - Memory address

 - DIS - Display RAM

 - RAM - System RAM

 - ROM - Read only memory, where to program is stored

 - CACHE - 1 byte that stores output from operations

 - CLEAR - Always gives 0

 - ADD - Add

 - SUB - Subtract

 - MUL - Multiply

 - DIV - Divide

 - MV - Move pointer

 - IF - Conditional

 - ELSE - If above conditional is false

 - ENDIF - Ends the IF statement

 - VAR - Declares a variable

 - MV ROM PNT LNxline_number - Moves rom pointer to the starting byte of a line

 - WR - Writes to memory

---

## Exmaples

This code achieves nothing, it is simply a demo to show how to write yeessembly.

```

ADD RAM BEG 0x1 ROM PNT 0x0

SUB ROM PNT 0x2 ROM PNT 0x4

MUL ROM BEG 0x2 RAM BEG 0x2

DIV RAM PNT 0x1 ROM BEG 0x4

MV DIS BEG 0x4

MV ROM PNT LNx5 (moves pointer to the starting byte of line, only works for ROM)

IF RAM BEG 0x1 > ROM PNT

code here

ELSE

code here

ENDIF

WR CACHE > RAM BEG 0x3

WR RAM BEG 0x1 > RAM PNT 0x0

VAR SUPERCOOLNAME = 15

(this does:

WR ROM PNT 0x1 > RAM BEG ram_adress (eg 0x1 or 0x5 or whatever)

and sets the following byte to your value (eg 15)

)

WR CLEAR > SUPERCOOLNAME

(under the hood, it does this:

WR CLEAR > RAM BEG ram_adress

and clears the variable)

Could also be used like this:

ADD SUPERCOOLNAME MYAMAZINGVARIABLE

ADD RAM PNT 0x1 MYAMAZINGVARIABLE

```

