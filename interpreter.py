# NOTE: THIS CLASS SHOULD ONLY ACCEPT VALID CHIP8 ASSEMBLY
# Takes in a Chip 8 Assembly file and outputs the opcodes
class Assembler:
    def __init__(self) -> None:
        self.instruction_set = {
            "CLS": self.handle_cls,
            "RET": self.handle_ret,
            "JP": self.handle_jp,
            "CALL": self.handle_call,
            "SE": self.handle_se,
            "SNE": self.handle_sne,
            "LD": self.handle_ld,
            "ADD": self.handle_add,
            "OR": self.handle_or,
            "AND": self.handle_and,
            "XOR": self.handle_xor,
            "SUB": self.handle_sub,
            "SHR": self.handle_shr,
            "SUBN": self.handle_subn,
            "SHL": self.handle_shl,
            "RND": self.handle_rnd,
            "DRW": self.handle_drw,
            "SKP": self.handle_skp,
            "SKNP": self.handle_sknp
        }

    # Packs an integer into 2 bytes 
    def pack(self, val) -> bytearray:
        return val.to_bytes(2, "big")
    
    # Seperates the register from the number
    def seperate_reg(self, token) -> int:
        if not token.startswith('V'):
            raise ValueError("Expected register format")
        return int(token[1:], 16)
    
    # Parses any base into an integer
    def val(self, token) -> int:
        return int(token, 0)
    
    def set_x(self, token) -> int:
        if token[0] == 'V':
            token = self.seperate_reg(token)
        return token << 8
    
    def set_y(self, token) -> int:
        if token[0] == 'V':
            token = self.seperate_reg(token)
        return token << 4
        

    def assemble(self, filename, outfilename="newFile.ch8") -> None:
        bytecode = bytearray()
        try:  
            with open(filename, "r") as file:
               lines = file.readlines()
               for linenum, line in enumerate(lines, 1):
                   tokens = line.replace(",", " ").upper().split()
                   command = tokens[0]
                   print(command)
                   arguments = tokens [1:]
                   print(arguments)
                   if command in self.instruction_set:
                       try:
                           opcode = self.instruction_set[command](arguments)
                           bytecode += opcode
                       except Exception as e:
                           print(f"Unknown instruction on line {linenum} as {e}")
                           
                                   

            with open(outfilename, "wb") as outfile:
                outfile.write(bytecode)

                        
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        except IOError as e:
            print(f"An I/O error occurred: {e}")
    

    def nibble_addr(self, prefix, addr) -> int:
        if isinstance(addr, int):
            return prefix | (addr & 0x0FFF)
        return prefix | (self.val(addr) & 0x0FFF)
    
    def nibble_byte(self, prefix, byte) -> int:
        return prefix | (byte & 0xFF)

    def handle_cls(self, args) -> bytearray:
        return self.pack(0x00E0)
    
    def handle_ret(self, args) -> bytearray:
        return self.pack(0x00EE)
    
    def handle_jp(self, args) -> bytearray:
        match args:
            case ["V0", addr]:
                 return self.pack(self.nibble_addr(0xB000, addr))
            case [addr]:
                 return self.pack(self.nibble_addr(0x1000, addr))
    
    def handle_call(self, args) -> bytearray:
        addr = self.val(args[0])
        return self.pack(self.nibble_addr(0x2000, addr))

    def handle_se(self, args) -> bytearray:
        x = self.set_x(args[0])
        if args[1][0] == "V":
            y = self.set_y(args[1])
            return self.pack(0x5000 | x | y)
        kk = self.val(args[1])
        return self.pack(0x3000 | x | kk)

    def handle_sne(self, args) -> bytearray:
        x = self.set_x(args[0])
        if args[1][0] == "V":
            y = self.set_y(args[1])
            return self.pack(0x9000 | x | y)
        kk = self.val(args[1])
        return self.pack(0x4000 | x | kk)
    
    def handle_ld(self, args) -> bytearray:
         match args:
             case ["I", addr]:
                 return self.pack(self.nibble_addr(0xA000, addr))
             case ["DT", vx]:
                 x = self.set_x(vx)
                 return self.pack(0xF015 | x)
             case ["ST", vx]:
                 x = self.set_x(vx)
                 return self.pack(0xF018 | x)
             case ["F", vx]:
                 x = self.set_x(vx)
                 return self.pack(0xF029 | x)
             case ["B", vx]:
                 x = self.set_x(vx)
                 return self.pack(0xF033 | x)
             case ["[I]", vx]:
                 x = self.set_x(vx)
                 return self.pack(0xF055 | x)
             case [vx, "DT"]:
                 x = self.set_x(vx)
                 return self.pack(0xF007 | x)
             case [vx, "K"]:
                 x = self.set_x(vx)
                 return self.pack(0xF00A | x)
             case [vx, "[I]"]:
                 x = self.set_x(vx)
                 return self.pack(0xF065 | x)
             case [vx, vy] if vx.startswith('V') and vy.startswith('V'):
                x = self.set_x(vx)
                y = self.set_y(vy)
                return self.pack(0x8000 | x | y)
             case [vx, byte] if vx.startswith('V'):
                 x = self.set_x(vx)
                 kk = (self.val(byte) & 0xFF)
                 return self.pack(0x6000 | x | kk)
             case _:
                raise ValueError(f"Invalid LD instruction arguments: {args}")

    def handle_add(self, args) -> bytearray:
        x = self.set_x(args[0])
        if args[1].startswith('V'):
            y = self.set_y(args[1])
            return self.pack(0x8004 | x | y)
        kk = self.val(args[1])
        return self.pack(self.nibble_byte(0x7000, kk) | x)
        

    def handle_or(self, args) -> bytearray:
        x = self.set_x(args[0])
        y = self.set_y(args[1])
        return self.pack(0x8001 | x | y)

    
    def handle_and(self, args) -> bytearray:
        x = self.set_x(args[0])
        y = self.set_y(args[1])
        return self.pack(0x8002 | x | y)
    
    def handle_xor(self, args) -> bytearray:
        x = self.set_x(args[0])
        y = self.set_y(args[1])
        return self.pack(0x8003 | x | y)

    def handle_sub(self, args) -> bytearray:
        x = self.set_x(args[0])
        y = self.set_y(args[1])
        return self.pack(0x8005 | x | y)

    def handle_shr(self, args) -> bytearray:
        x = self.set_x(args[0])
        y = self.set_y(args[1])
        return self.pack(0x8006 | x | y)

    def handle_subn(self, args) -> bytearray:
        x = self.set_x(args[0])
        y = self.set_y(args[1])
        return self.pack(0x8007 | x | y)

    def handle_shl(self, args) -> bytearray:
        x = self.set_x(args[0])
        y = self.set_y(args[1])
        return self.pack(0x800E | x | y)

    def handle_rnd(self, args) -> bytearray:
        x = self.set_x(args[0])
        kk = self.val(args[1])
        return self.pack(self.nibble_byte(0xC000, kk) | x)

    def handle_drw(self, args) -> bytearray:
        x = self.set_x(args[0])
        y = self.set_y(args[1])
        n = self.val(args[2])
        return self.pack(0xD000 | x | y | (n & 0xF))


    def handle_skp(self, args) -> bytearray:
        x = self.set_x(args[0])
        return self.pack(0xE09E | x) 

    def handle_sknp(self, args) -> bytearray:
        x = self.set_x(args[0])
        return self.pack(0xE0A1 | x)