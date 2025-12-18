# NOTE: THIS CLASS SHOULD ONLY ACCEPT VALID CHIP8 ASSEMBLY
class Assembler:
    def __init__(self):
        pass
    def assemble(self, filename, outfilename="newFile.ch8"):
        try:
            bytecode = bytearray()
            with open(filename, "r") as file:
                for line in file:
                    code = line.split()
                    match code[0]:
                        case "CLS":
                            bytecode += (0x00E0).to_bytes(2, "big")
                        case "RET":
                            bytecode += (0x00EE).to_bytes(2, "big")
                        case "JP":
                            if len(code) == 2:
                                addr = int(code[1], 16)
                                opcode = 0x1000 | addr
                            elif len(code) == 3:
                                addr = int(code[2], 16)
                                opcode = 0xB000 | addr
                            bytecode += opcode.to_bytes(2, "big")
                        case "CALL":
                            addr = int(code[1], 16)
                            opcode = 0x2000 | addr
                            bytecode += opcode.to_bytes(2, "big")
                        case "SE":
                            if code[2][0] == "V":
                                x = int(code[1][1], 16) << 8
                                y = int(code[2][1], 16) << 4
                                opcode = 0x5000 | x | y
                                bytecode += opcode.to_bytes(2, "big")
                            else: 
                                x = int(code[1][1], 16) << 8
                                nn = int(code[2], 16)
                                opcode = 0x3000 | x | nn
                                bytecode += opcode.to_bytes(2, "big")
                         
                        

            with open(outfilename, "wb") as outfile:
                outfile.write(bytecode)

                        
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        except IOError as e:
            print(f"An I/O error occurred: {e}")


        