###### Version 2.1

# Yeessembly

## Components

### 1. RAM (Random Access Memory)
- **Purpose:** Temporary storage for data that can be read from and written to during program execution.
- **Addressing:** Uses single linear address.
    - Addresses are 4 bits each, providing 16 total addresses.
    - In practice, each address can be split into a y and an x component to make selecting easier, as long as the RAM is equal length on both sides.
- **Data:** Each location in RAM stores 4 bits.

---

### 2. ROM (Read-Only Memory)
- **Purpose:** Permanent storage for program instructions and data.
- **Addressing:** ROM uses the same memory address system as the RAM.
- **Data:** ROM is read-only and cannot be written to during execution.

---

### 3. Stack
- **Purpose:** A stack-based data structure used to store intermediate values for logic operations and control flow.
- **Structure:** The stack is an array of 4 bits.
- **Behavior:**
    - **Push Operation:** Adds a new value to the **bottom** of the stack, shifting all other values **up** by one position.
    - **Pop Operation:** Removes the value from the **bottom** of the stack, shifting all other values **down** by one position.
- **Limits:** The maximum size of the stack is not explicitly defined but must be managed by the program to prevent overflow.

---

### 4. Logic
- **Purpose:** The Logic component performs computations and manipulates the stack, memory, and program flow.
- **Instructions:** There are 8 logic operations, each represented by a 4-bit opcode.

#### Instruction Set

| **Instruction**       | **Opcode** | **Description**                                                                 |
|------------------------|------------|-------------------------------------------------------------------------------|
| **Add**               | `1000`     | Adds the bottom two values in the stack. Pushes the result to the bottom.      |
| **Subtract**          | `1001`     | Subtracts the second value in the stack from the first. Pushes the result.     |
| **IF**                | `1010`     | If the bottom value is greater than the second, move RAM pointer to 3rd value. |
| **Move RAM Pointer**  | `1011`     | Moves the RAM pointer to the address at the bottom of the stack.               |
| **Move ROM Pointer**  | `1100`     | Moves the ROM pointer to the address at the bottom of the stack.               |
| **Pop Stack**         | `1101`     | Removes the bottom value from the stack.                                       |
| **Read**              | `1110`     | Reads the value at the RAM pointer and pushes it to the stack.                 |
| **Write**             | `1111`     | Writes the bottom value in the stack to the RAM pointer location.              |

- **Number Values:** Any 4-bit value **starting with `0`** is treated as a literal number and are pushed directly onto the stack. As a workaround, you can push a second number to the stack and add them to utilize the full 4 bits

---

## Instruction Details

### 1. Add
- **Opcode:** `1000`
- **Behavior:**
    - Pops the bottom two values from the stack.
    - Adds them together.
    - Pushes the result to the **bottom** of the stack.

``` text title="Example"
Stack Before: [0101 (5), 0011 (3), ...]
Stack After: [0100 (8), ...]
```

---

### 2. Subtract
- **Opcode:** `1001`
- **Behavior:**
    - Pops the bottom two values from the stack.
    - Subtracts the second value from the first.
    - Pushes the result to the **bottom** of the stack.
    - **Note:** This instruction does not support negative numbers. Results are clamped at 0.

```text title="Example"
Stack Before: [0101 (5), 0011 (3), ...]
Stack After: [0010 (2), ...]
```

---

### 3. IF
- **Opcode:** `1010`
- **Behavior:**
    - Compares the bottom two values in the stack:
        - **If** the first value > second value, move the RAM pointer to the address specified by the **3rd value** in the stack.
    - Leaves all values on the stack intact.

``` text title="Example"
Stack Before: [0111 (7), 0101 (5), 1011 (11), ...]
Condition: 7 > 5 → True
RAM Pointer: Moves to 1011 (11)
```

---

### 4. Move RAM Pointer
- **Opcode:** `1011`
- **Behavior:**
    - Stack remains unchanged
    - Moves RAM pointer to first address in stack

```text title="Example"
Stack Before: [0111 (7), ...]
RAM Pointer: Moves to 0111 → 7
```

---

### 5. Move ROM Pointer
- **Opcode:** `1100`
- **Behavior:**
    - Identical to **Move RAM Pointer**, but moves the **ROM pointer**.

---

### 6. Pop Stack
- **Opcode:** `1101`
- **Behavior:**
    - Removes the bottom value from the stack.
    - Shifts all other values **down** by one position.

```text title="Example"
Stack Before: [0101 (5), 0011 (3), 0010 (2), ...]
Stack After: [0011 (3), 0010 (2), ...]
```

---

### 7. Read
- **Opcode:** `1110`
- **Behavior:**
    - Reads the value at the **current RAM pointer**.
    - Pushes the value to the **bottom** of the stack.

```text title="Example"
RAM at (2, 3): 0111 (7)
Stack Before: [...]
Stack After: [0111 (7), ...]
```

---

### 8. Write
- **Opcode:** `1111`
- **Behavior:**
    - Pops the bottom value from the stack.
    - Writes the value to the **current RAM pointer** location.

```text title="Example"
Stack Before: [1001 (9), ...]
RAM Pointer: 11
RAM After: 11 → 1001 (9)
```

---

## Memory and Stack Operations Summary

| **Operation**        | **Behavior**                                                        |
|-----------------------|---------------------------------------------------------------------|
| **Push**             | Adds value to the bottom of the stack (shifts others up).           |
| **Pop**              | Removes value from the bottom of the stack (shifts others down).    |
| **RAM Pointer Move** | Sets the RAM pointer using a 4-bit x and y address.                 |
| **Read**             | Reads value at RAM pointer and pushes it to the stack.             |
| **Write**            | Writes bottom stack value to the RAM pointer location.             |

---

## Example Program: Add Two Numbers
This example program adds two numbers stored in RAM at locations `0` and `1` and stores the result at `2`.

### Steps:
1. Move RAM pointer to `0` and read the value.
2. Move RAM pointer to `1` and read the value.
3. Perform **Add**.
4. Move RAM pointer to `2` and **Write** the result.

### Instructions:
```text title="Instructions"
1011    ; Move RAM pointer to 0
0000    ; Address: 0
1110    ; Read value into stack

1011    ; Move RAM pointer to 1
0001    ; Address: 1
1110    ; Read value into stack

1000    ; Add the two values

1011    ; Move RAM pointer to 2
0010    ; Address: 2
1111    ; Write result to RAM
```
