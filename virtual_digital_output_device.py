class VirtualDigitalOutputDevice:
    def __init__(self, pin):
        self.pin = pin
        self.is_active = False

    def on(self):
        self.is_active = True

    def toggle(self):
        self.is_active = not self.is_active

    def off(self):
        self.is_active = False
