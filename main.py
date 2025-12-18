from cpu import Emulator, Display
import time
import keyboard
chip8 = Emulator()
chip8.load_rom("Space_Invaders.ch8")
display = Display()

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
        display.handle_events()

        for key_char, key_value in key_map.items():
            chip8.keys[key_value] = 1 if keyboard.is_pressed(key_char) else 0
        chip8.cycle()
        if chip8.drawFlag:
            display.draw(chip8.display)
            chip8.drawFlag = False
        current_time = time.time()
        if current_time - last_timer_time >= 1/60:
            chip8.update_timers()
            last_timer_time = current_time
        print(chip8.pc)
        time.sleep(1)

except KeyboardInterrupt:
    print("\n Emulation stopped")