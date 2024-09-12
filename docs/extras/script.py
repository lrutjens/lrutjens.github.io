#pyright: reportUndefinedVariable=false
import re
from js import console, window

def dec2bin(dec, length, line):
    try:
        binary = bin(int(dec))[2:]
        if len(binary) > length:
            raise ValueError(f'Number too large at line {line + 1}')
        
        padded = binary.zfill(length)

        if int(dec) < 0:
            if padded[0] == "1":
                raise ValueError(f'Overflow when converting to negative number on line {line + 1}!\nPlease make the number non-negative or smaller')
            else:
                padded = "1" + padded[1:]

        groups = []
        if len(padded) % 8 != 0:
            first_group_len = len(padded) % 8
            groups.append(padded[:first_group_len])
            padded = padded[first_group_len:]

        for i in range(0, len(padded), 8):
            groups.append(padded[i:i+8])
        
        return ' '.join(groups)
    except:
        raise ValueError(f'An error occured while parsing line {line}!')
        
        

def list2dict(li):
    out_dict = {}
    for item in li:
        out_dict.update({item[0]: item[1:]})
    return out_dict

opcodes = {
    'ADD': '000',
    'SUB': '001',
    'MUL': '010',
    'DIV': '011',
    'MV': '100',
    'IF': '101',
    'WR': '110'
    # '???': '111'
}

codes = {
    "CACHE": "00",
    "ROM": "01",
    "RAM": "10",
    "DIS": "11"
}

arith_codes = {
    "ROM": "00",
    "RAM": "01",
    "CACHE": "10"
}

conditional_codes = {
    '>': '0000',
    '<': '0001',
    '>=': '0010',
    '<=': '0011',
    '==': '0100',
    '?': '0101',
    '??': '0110',
    '???': '0111'
}

variables = {}
line_nums = {}


raw_yeessembly = ''
preprocessed = ''
pinary = ''

def to_raw_yeessembly(text_input):
    conditional_stack = []
    global preprocessed
    global raw_yeessembly
    text = Element('text_area_input').value
    text = text.replace("\r\n", "\n")
    if text != '':
        line_num = 0
        current_conditional = -1
        tmp_cond = ''
        for line in text.splitlines(True):
            line_num += 1
            opcode = line.split(" ")[0]
            if opcode in ['IF', 'ELSE\n', 'ENDIF\n']:
                if opcode == 'IF':
                    current_conditional += 1
                    conditional_stack.append([line_num])
                elif opcode == 'ELSE\n':
                    conditional_stack[current_conditional].append(line_num)
                elif opcode == 'ENDIF\n':
                    conditional_stack[current_conditional].append(line_num)
                    current_conditional -= 1
            tmp_cond += line
        conditional_dict = list2dict(conditional_stack)
        for index, line in enumerate(tmp_cond.splitlines(True)):
            opcode = line.split(" ")
            if index + 1 in conditional_dict.keys():
                if len(conditional_dict[index + 1]) == 1:
                    line = line.strip('\n')
                    line += f' LNx{index + 2}\nLNx{conditional_dict[index + 1][0]}'
                else:
                    line = line.strip('\n')
                    line += f' LNx{index + 2}\nLNx{conditional_dict[index + 1][0]}'
            if 'ELSE' in line:
                for item in conditional_stack:
                    if len(item) > 2:
                        if item[1] == index + 1:
                            line = f'MV ROM BEG LNx{item[2] + 1}'
            if 'ENDIF' in line:
                for item in conditional_stack:
                    line = 'MV ROM PNT 0x1'


            preprocessed += (line + '\n')
            
        for line in preprocessed.splitlines(True):
            was_var_dec = False
            line = line.replace('\n\n', '\n')
            opcode = line.split(" ")[0]
            if 'VAR' in line and '=' in line:
                if line.split(" ")[1] not in variables.keys():
                    variables.update({line.split(" ")[1]: f'0x{len(variables.keys())}'})
                raw_yeessembly += (f'WR ROM PNT 0x1 > RAM BEG {variables[line.split(" ")[1]]}\n{dec2bin(line.split(" ")[3], 16, line_num)} {dec2bin(0, 24, line_num)}\n')
                was_var_dec = True
            elif "LNx" in line:
                for i in range(3):
                    file_input = text
                    bytes_passed = 0
                    lines_passed = 0
                    try:
                        file_line_num = int(re.search(r'LNx(\d+)', line).group(i+1))
                        if line in ['', ' ', '\n', '$', ' \n', '\n ']:
                            continue
                        for index, line2 in enumerate(file_input.splitlines()):
                            if line in ['', ' ', '\n', '$', ' \n', '\n '] or line[1] == 'x':
                                continue
                            lines_passed += 1
                            bytes_passed += 5
                            if line2.split(" ")[0] in ['IF', 'VAR']:
                                bytes_passed += 5
                            if line2[1] == "x" or line2[0] == '#':
                                bytes_passed -= 5
                            if lines_passed == file_line_num:
                                print(f'Found: {bytes_passed-5} - {lines_passed}')
                                if_byte_fix = False
                                if line2.split(' ')[0] == 'IF' and file_input.splitlines(True)[index]:
                                    bytes_passed -= 5
                                    if_byte_fix = True
                                line = line.replace(f'LNx{file_line_num}', f'0x{bytes_passed - 5}')
                                if if_byte_fix:
                                    bytes_passed += 5
                    except:
                        pass
                                
            if 'VAR' not in line:
                for i in range(len(variables.keys())):
                    if list(variables.keys())[i] in line and 'VAR' not in line:
                        line = line.replace(list(variables.keys())[i], f'RAM BEG {variables[list(variables.keys())[i]]}', 1)
                for i in range(len(variables.keys())):
                    if list(variables.keys())[i] in line and 'VAR' not in line:
                        line = line.replace(list(variables.keys())[i], f'RAM BEG {variables[list(variables.keys())[i]]}', 1)
                for i in range(len(variables.keys())):
                    if list(variables.keys())[i] in line and 'VAR' not in line:
                        line = line.replace(list(variables.keys())[i], f'RAM BEG {variables[list(variables.keys())[i]]}', 1)
                
            if not was_var_dec:
                raw_yeessembly += line
            line_num += 1

def to_pinary():
    global pinary
    global raw_yeessembly
    raw_yeessembly_input = raw_yeessembly.replace('\n\n', '\n')
    if len(raw_yeessembly_input) > 0:
        line_num = 0
        line_itr = 0
        for line in raw_yeessembly_input.splitlines(True):
            if line == '':
                break
            if line[0] !='#':
                opcode = line.split(" ")[0]
                line = line.replace('0x', '')
                match opcode:
                    case 'ADD' | 'SUB' | 'MUL' | 'DIV':
                        pinary += (f'{opcodes[opcode]}{arith_codes[line.split(" ")[1]]}{"0" if line.split(" ")[2] == "BEG" else "1"}{arith_codes[line.split(" ")[4]]}{"0" if line.split(" ")[5] == "BEG" else "1"} {dec2bin(line.split(" ")[3], 16, line_num)} {dec2bin(line.split(" ")[6], 16, line_num)}\n')
                    case 'MV':
                        pinary += (f'{opcodes[opcode]}{codes[line.split(" ")[1]]}{"0" if line.split(" ")[2] == "BEG" else "1"}00 {dec2bin(line.split(" ")[3], 16, line_num) if "LNx" not in line else line.split(" ")[3][:len(line.split(" ")[3])-1]} {dec2bin(0, 16, line_num)}\n')
                    case 'WR':
                        match line.split(" ")[1]:
                            case "CACHE" | "CLEAR":
                                pinary += (f'{opcodes[opcode]}{"10" if line.split(" ")[1] == "CACHE" else "11"}0{"0" if line.split(" ")[3] == "RAM" else "1"}{"0" if line.split(" ")[4] == "BEG" else "1"} {dec2bin(0, 16, line_num)} {dec2bin(line.split(" ")[5], 16, line_num)}\n')
                            case _:
                                pinary += (f'{opcodes[opcode]}{arith_codes[line.split(" ")[1]]}{"0" if line.split(" ")[2] == "BEG" else "1"}{"0" if line.split(" ")[5] == "RAM" else "1"}{"0" if line.split(" ")[2] == "BEG" else "1"} {dec2bin(line.split(" ")[3], 16, line_num)} {dec2bin(line.split(" ")[7], 16, line_num)}\n')
                    case "BREAK":
                        line_num -= 1
                    case _: 
                        pinary += (line + '\n')
                line_num += 1
                line_itr += 1

    if len(pinary) > 0:
        output_str = ''
        current_conditional = -1
        line_num = 0
        for index, line in enumerate(pinary.splitlines(True)):
            line_num += 1
            opcode = line.split(" ")[0]
            match opcode:
                case 'IF':
                    pyscript_newline_jank_fix = "\n"
                    newline = f'101{"0" if line.split(" ")[1] == "RAM" else "1"}{"0" if line.split(" ")[2] == "BEG" else "1"}{"0" if line.split(" ")[5] == "RAM" else "1"}{"0" if line.split(" ")[6] == "BEG" else "1"}0 {conditional_codes[line.split(" ")[4]]}0000 {dec2bin(line.split(" ")[3], 16, line_itr)} {str(dec2bin(line.split(" ")[7], 16, line_itr)).split(" ")[0] }\n{str(dec2bin(line.split(" ")[7], 16, line_itr)).split(" ")[1]} {dec2bin(line.split(" ")[8], 16, line_itr)} {dec2bin(pinary.splitlines(True)[index+2], 16, line_itr)}'
                    output_str += newline
                case _:
                    output_str += line
    return output_str

def assemble(*args, **kwargs):
    global raw_yeessembly
    global text_input
    global variables
    global line_nums
    global pinary
    global preprocessed
    raw_yeessembly_input = ''
    variables = {}
    line_nums = {}
    raw_yeessembly = ''
    preprocessed = ''
    pinary = ''

    try:
        text_output = Element("test-output")
        text_input = Element('text_area_input')
        print('Parsing...')
        to_raw_yeessembly(text_input)
        raw_yeessembly = raw_yeessembly.strip()
        raw_yeessembly_input = ''
        print('\n----\n')
        for line in raw_yeessembly.splitlines():
            if line != '' and line != '\n' and line != '$':
                print(line)
                raw_yeessembly_input += f'{line}\n'
        print('-------')
        output_string = to_pinary()
        print('Done!')
        #raw_yeessembly_input = text_input
        final_output = ''
        for line in output_string.splitlines(True):
            if len(line) > 4:
                final_output += line
        text_output.element.innerText = (final_output)
        raw_yeessembly_input = ''
        text_input = ''
        output_string = ''
        variables = {}
        line_nums = {}
        raw_yeessembly = ''
        preprocessed = ''
        pinary = ''
    except Exception as e:
        console.log(e)
        text_output.element.innerText = f"An error occured while parsing,\nPlease make sure everything is formatted correctly\n\n{e}"


def assemble_just_raw(*args, **kwargs):
    global raw_yeessembly
    global variables
    global line_nums
    global text_input
    global preprocessed
    global pinary
    raw_yeessembly_input = ''
    variables = {}
    line_nums = {}
    raw_yeessembly = ''
    preprocessed = ''
    pinary = ''
    try:
        text_output = Element("test-output")
        text_input = Element('text_area_input')
        print('Parsing...')
        to_raw_yeessembly(text_input)
        raw_yeessembly = raw_yeessembly.strip()
        raw_yeessembly_input = ''
        print('\n----\n')
        for line in raw_yeessembly.splitlines():
            if line != '' and line != '\n' and line != '$':
                print(line)
                raw_yeessembly_input += f'{line}\n'
        print('-------')
        print('Done!')
        text_output.element.innerText = (raw_yeessembly_input)
        raw_yeessembly_input = ''
        variables = {}
        line_nums = {}
        raw_yeessembly = ''
        preprocessed = ''
        pinary = ''
    except Exception as e:
        console.log(e)
        text_output.element.innerText = f"An error occured while parsing,\nPlease make sure everything is formatted correctly\n\n{e}"

Element("test-output").element.innerText = "Ready!!"
