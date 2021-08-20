from gpiozero import DigitalOutputDevice
from signal import pause

if __name__ == '__main__':
    out = DigitalOutputDevice(17)
    out.blink()

    pause()
