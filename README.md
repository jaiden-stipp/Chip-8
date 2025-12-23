![Project Screenshot](/img/Screenshot_9.png)

What is Chip-8?
---------------
Chip-8 is an interpreted programming language, originally used on 8-bit microcomputers in the mid-1970s like the COSMAC VIP and TELMAC 1800. 

Chip 8 CPU Specifications:
----------------------------
- 4096 bytes of adressable memory
- Sixteen 8-bit registers (v0-vF) (vF register commonly used for storing carry values)
- 16-bit index register
- 64 byte stack
- 8-bit stack pointer
- 8-bit delay timer
- 8-bit sound timer
- 64x32 bit frame buffer (display)
- Frame buffer is a (x,y) adressable array that tells the display whether a pixel is on or off.
- 16-bit program counter


Chip-8 Op Codes / Instruction Set
----------------
0nnn - Jumps to routine at nnn (not implemented because modern interpreter)

00E0 / CLS - Clear display

00EE / RET - Returns from routine. Sets program counter to address at the top of the stack and then subtracts 1

1nnn - Jumps to location nnn. Also sets program counter to nnn

2nnn - Calls routine at nnn. Interpreter icrements the stack pointer and sets current stack pointer on top of stack

3xkk - Skip next instruction if Vx = kk. Compares register Vx to kk and if are equal, increment pc by 2

4xkk - Skip next instruction if Vx != kk. Compares register Vx to kk and if they are not equal, increments pc by 2

5xy0 - Skip next instruction if Vx = Vy. Compares Vx to Vy and if equal increment pc by 2

6xkk - Set Vx to kk

7xkk - Set Vx = Vx + kk

8xy0 - Stores value of Vy into Vx

8xy1 - Set *Vx* to Vx OR Vy

8xy2 - Set *Vx* to Vx AND Vy

8xy3 - Set *Vx* to Vx XOR Vy  

8xy4 - Set *Vx* to Vx + Vy. Set VF to carry

8xy5 - Set *Vx* to Vx - Vy. Vf = NOT borrow

8xy6 - Set *Vx* to Vx shifted one bit to the right. Vf = 1 if the LSB is one before shift

8xy7 - Set *Vx* to Vy - Vx. Vf = NOT borrow

8xyE - Set *Vx* to Vx shifted one bit to the left. Vf = 1 if the MSB is one before the shift

9xy0 - Skip one instruction if Vx != Vy

Annn - Set I (index register) to nnn

Bnnn - Jump/Set pc to location nnn + V0

Cxkk - Set Vx = random byte & kk

Dxyn - Display n-byte sprite starting at I (index register) at (Vx, Vy). Vf = collision

### Keyboard instructions
Ex9E - Skips next instruction if key with value of Vx is pressed

ExA1 - Skips next instruction if key with value of Vx is not pressed

### Timer, Sound, & Memory Instructions
Fx07 - Set Vx = delay timer value

Fx0A - Wait for a key press, store the value of the key in Vx. (Blocking operation, all execution stops until key press)

Fx15 - Set delay timer = Vx

Fx18 - Set sound timer = Vx

Fx1E - Set I = I + Vx

Fx29 - Set I = location of sprite for digit Vx

Fx33 - Store BCD representation of Vx in memory locations I, I+1, and I+2

Fx55 - Store registers V0 through Vx in memory starting at location I

Fx65 - Read registers V0 through Vx from memory starting at location I


-- Project by Jaiden Stipp created with Cowgod's Chip-8 Technical Reference
-- Special thanks to the github repos that provided the test ROM files to run 
