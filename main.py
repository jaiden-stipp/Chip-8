from cpu import Emulator
import time
import keyboard
chip8 = Emulator()
chip8.load_rom("67.ch8")


print(f"Program Counter: {hex(chip8.pc)}")
key_map = {
    '1': 0x1, '2': 0x2, '3': 0x3, '4': 0xC,
    'q': 0x4, 'w': 0x5, 'e': 0x6, 'r': 0xD,
    'a': 0x7, 's': 0x8, 'd': 0x9, 'f': 0xE,
    'z': 0xA, 'x': 0x0, 'c': 0xB, 'v': 0xF
}
last_timer_time = time.time()
try:
    while True:
        for key_char, key_value in key_map.items():
            if keyboard.is_pressed(key_char):
                chip8.keys[key_value] = 1
            else:
                chip8.keys[key_value] = 0
        chip8.cycle()
        current_time = time.time()
        if current_time - last_timer_time >= 1/60:
            chip8.update_timers()
            last_timer_time = current_time
        time.sleep(0.001)

except KeyboardInterrupt:
    print("\n Emulation stopped")