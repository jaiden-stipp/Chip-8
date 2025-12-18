import random
#import pygame
FONT_SET = [
    0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
    0x20, 0x60, 0x20, 0x20, 0x70, # 1
    0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
    0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
    0x90, 0x90, 0xF0, 0x10, 0x10, # 4
    0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
    0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
    0xF0, 0x10, 0x20, 0x40, 0x40, # 7
    0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
    0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
    0xF0, 0x90, 0xF0, 0x90, 0x90, # A
    0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
    0xF0, 0x80, 0x80, 0x80, 0xF0, # C
    0xE0, 0x90, 0x90, 0x90, 0xE0, # D
    0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
    0xF0, 0x80, 0xF0, 0x80, 0x80  # F
]
class Emulator:
    def __init__(self):
        # RAM
        self.memory = [0] * 4096
        # Display
        self.display = [0] * 2048
        # Registers
        self.V = [0] * 16
        # Index Register
        self.I = 0
        # Program counter
        self.pc = 0x200
        # Stack
        self.stack = []
        # Keyboard
        self.keys = [0] * 16
        # Timers
        self.delayTimer = 0
        self.soundTimer = 0

        # Load Font set into memory
        for i in range(len(FONT_SET)):
            self.memory[i] = FONT_SET[i]
    def load_rom(self, filename):
        try:
            # Opens ch8 file as a binary and loads into self.memory
            with open(filename, 'rb') as f:
                rom_data = f.read()
            for index, byte in enumerate(rom_data):
                self.memory[512 + index] = byte

            print(f"ROM loaded. Size: {len(rom_data)} bytes")
        except FileNotFoundError:
            print(f"Couldn't find file {filename}")
    def print_screen(self):
        print("-" * 66)
        for y in range(32):
            line = "|"

            for x in range(64):
                index = x + (y * 64)
                if self.display[index]:
                    line += "█"
                else:
                    line += " "
            line += "|"
            print(line)
        print("-" * 66)
    def update_timers(self):
        if self.delayTimer > 0:
            self.delayTimer -= 1
        if self.soundTimer > 0:
            self.soundTimer -= 1
    def cycle(self):
        # Glues together the opcode from the current byte at pc and the next byte
        opcode = (self.memory[self.pc] << 8) | self.memory[self.pc+1]
        # Takes the 4 bits from wherever the F's are that are & with the opcode
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        n = opcode & 0x000F
        nn = opcode & 0x00FF
        nnn = opcode & 0x0FFF
        self.pc += 2
        # Takes the first hex digit that decides the kind of instruction. View README to understand what the instruction types do
        instruction_type = opcode & 0xF000
        if instruction_type == 0x0000:
            if opcode == 0x00E0:
                self.display = [0] * (64 * 32)
                print("CLS")
            if opcode == 0X00EE:
                self.stack.pop()
                print("RET")
        elif instruction_type == 0x1000:
            self.pc = nnn
            print(f"JP {hex(nnn)}")
        elif instruction_type == 0x2000:
            
            self.stack.append(self.pc)
            self.pc = nnn
            print(f"CALL {hex(nnn)}")
        elif instruction_type == 0x3000:
            if self.V[x] == nn:
                self.pc += 2
            print(f"SE Vx, {hex(nn)}")
        elif instruction_type == 0x4000:
            if self.V[x] != nn:
                self.pc += 2
            print(f"SNE Vx, {hex(nn)}")
        elif instruction_type == 0x5000:
            if self.V[x] == self.V[y]:
                self.pc += 2
            print(f"SE Vx, Vy")
        elif instruction_type == 0x6000:
            self.V[x] = nn
            print(f"LD Vx, {hex(nn)}")
        elif instruction_type == 0x7000:
            self.V[x] = (self.V[x] + nn) & 0xFF
            print(f"ADD Vx, {hex(nn)}")
        elif instruction_type == 0x8000:
            match n:
                case 0x0000:
                    self.V[x] = self.V[y]
                    print("LD Vx, Vy")
                case 0x0001:
                    self.V[x] = self.V[x] | self.V[y]
                    print("OR Vx, Vy")
                case 0x0002:
                    self.V[x] = self.V[x] & self.V[y]
                    print("AND Vx, Vy")
                case 0x0003:
                    self.V[x] = self.V[x] ^ self.V[y]
                    print("XOR Vx, Vy")
                case 0x0004:
                    sum_val = self.V[x] + self.V[y]
                    self.V[0xF] = 1 if sum_val > 255 else 0
                    self.V[x] = sum_val & 0xFF
                    print("ADD Vx, Vy")
                case 0x0005:
                    borrow = 1 if self.V[x]  >= self.V[y] else 0
                    self.V[x] = (self.V[x] - self.V[y]) & 0xFF
                    self.V[0xF] = borrow
                    print("SUB Vx, Vy")
                case 0x0006:
                    self.V[0xF] = 1 if (self.V[x] & 0x01) == 0x01 else 0
                    self.V[x] = self.V[x] >> 1
                    print("SHR Vx")
                case 0x0007:
                    borrow = 1 if self.V[y]  >= self.V[x] else 0
                    self.V[x] = (self.V[y] - self.V[x]) & 0xFF
                    self.V[0xF] = borrow
                    print("SUBN Vx, Vy")
                case 0x000E:
                    self.V[0xF] = 1 if (self.V[x] & 0x80) == 0x80 else 0
                    self.V[x] = (self.V[x] << 1) & 0xFF
                    print("SHL Vx")
        elif instruction_type == 0x9000:
            if self.V[x] != self.V[y]:
                self.pc += 2
            print("SNE Vx, Vy")
        elif instruction_type == 0xA000:
            self.I = nnn
            print(f"LD I, {hex(nnn)}")
        elif instruction_type == 0xB000:
            self.pc = nnn + self.V[0]
            print(f"JP V0, {hex(nnn)}")
        elif instruction_type == 0xC000:
            self.V[x] = random.randint(0, 255) & nn
            print(f"RND Vx, {hex(nn)}")
        # DRAW instruction -- Important
        elif instruction_type == 0xD000:
            x_coord = self.V[x]  % 64
            y_coord = self.V[y] % 32
            height = n
            self.V[0xF] = 0
            for row in range(height):
                sprite_byte = self.memory[self.I + row]

                for col in range(8): 
                    # Scans through the bits in the sprite byte
                    sprite_pixel = sprite_byte & (0x80 >> col)
                    if sprite_pixel != 0:
                        if (x_coord + col) < 64 and (y_coord + row) < 32:
                            pixel_index = (x_coord + col) + ((y_coord + row) * 64)
                            # Handling collisions
                            if self.display[pixel_index] == 1:
                                self.V[0xF] = 1

                            self.display[pixel_index] ^= 1
            self.print_screen()


            print(f"DRW Vx, Vy, {hex(n)}")
        # Keyboard checks
        elif instruction_type == 0xE000:
            match nn:
                case 0x9E:
                    if self.keys[self.V[x]] == 1:
                        self.pc += 2
                    print("SKP Vx")
                case 0xA1:
                    if self.keys[self.V[x]] == 0:
                        self.pc += 2
                    print("SKNP Vx")
        # Timer and Memory Instructions
        elif instruction_type == 0xF000:
            match nn:
                case 0x07:
                    self.V[x] = self.delayTimer
                    print("LD Vx, DT")
                case 0x0A:
                    pressed = False
                    for i in range(16):
                        if self.keys[i] == 1:
                            self.V[x] = i
                            pressed = True
                    if not pressed:
                        self.pc -= 2
                    print("LD Vx, K")
                case 0x15:
                    self.delayTimer = self.V[x]
                    print("LD DT, Vx")
                case 0x18:
                    self.soundTimer = self.V[x]
                    print("LD ST, Vx")
                case 0x1E:
                    self.I = self.I + self.V[x]
                case 0x29:
                    self.I = self.V[x] * 5
                    print("LD F, Vx")
                case 0x33:
                    value = self.V[x]
                    self.memory[self.I] = value // 100
                    self.memory[self.I + 1] = (value // 10) % 10
                    self.memory[self.I + 2] = value % 10
                    print("LD B, Vx")
                case 0x55:
                    for i in range(x+1):
                        self.memory[self.I + i] = self.V[i]
                    print("LD [I], Vx")
                case 0x65:
                    for i in range(x+1):
                        self.V[i] = self.memory[self.I + i]
                    print("LD Vx, [I]")

        else:
            print("Unkown Opcode")




        
        
        
