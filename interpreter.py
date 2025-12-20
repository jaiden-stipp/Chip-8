# NOTE: THIS CLASS SHOULD ONLY ACCEPT VALID CHIP8 ASSEMBLY
# Takes in a Chip 8 Assembly file and outputs the opcodes
class Assembler:
    def __init__(self):
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
    def assemble(self, filename, outfilename="newFile.ch8"):
        bytecode = bytearray()
        try:  
            with open(filename, "r") as file:
               lines = file.readlines()
               for linenum, line in enumerate(lines, 1):
                   tokens = line.replace(",", " ").upper().split()
                   command = tokens[0]
                   arguments = tokens [1:] 
                   if command in self.instruction_set:
                       try:
                           opcode = self.instruction_set[command](arguments)
                           
                       except Exception as e:
                           print(f"Unkown instruction on line {linenum}")
                                   

            with open(outfilename, "wb") as outfile:
                outfile.write(bytecode)

                        
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        except IOError as e:
            print(f"An I/O error occurred: {e}")
    


        