from pymata4 import pymata4
import time
from inspect import signature

CMD_LCD_DATA = 3
CMD_LCD_PRINT = 0
CMD_LCD_PUSH = 1
CMD_LCD_CLEAR = 2

CMD_MOTOR_DATA = 2
CMD_MOTOR_ON = 1
CMD_MOTOR_OFF = 2
CMD_MOTOR_INVERSE = 4
CMD_MOTOR_DIR = 5
CMD_MOTOR_SPEED = 6


class pyInterfaz(pymata4.Pymata4):

    def __init__(self, com_port=None):
        super().__init__(com_port=com_port, baud_rate=115200, arduino_wait=1)
        self._outputs = [self._Output(self, 0)]
        self._analogs = [self._Analog(self, 0)]
        self._digitals = [self._Digital(self, 14)]
        self._servos = [self._Servo(self, 9), self._Servo(self, 10)]
        self._lcd = self._LCD(self)

    def output(self, index):
        if index < 1: index = 1
        return self._outputs[index - 1]

    def analog(self, index):
        if index < 1: index = 1
        return self._analogs[index - 1]

    def digital(self, index):
        if index < 1: index = 1
        return self._digitals[index - 1]

    def servo(self, index):
        if index < 1: index = 1
        return self._servos[index - 1]

    def lcd(self):
        return self._lcd

    def print(self, str1, str2):
        if not self._lcd is None:
            if not self.lcd()._silenciado:
                self.lcd().clear()
                self.lcd().print(0, str1)
                self.lcd().print(1, str2)
                time.sleep(0.008)


    class _LCD:

        def __init__(self, interfaz):
            self._interfaz = interfaz
            self._silenciado = False

        def _strtosysex(self, str):
            buf = []
            for char in str:
                buf.append(ord(char) & 0x7F)
                buf.append(ord(char) >> 7 & 0x7F)
            return buf

        def push(self, str):
            data = [CMD_LCD_PUSH]
            data += self._strtosysex(str)
            self._interfaz._send_sysex(CMD_LCD_DATA, data)

        def print(self, row, str):
            data = [CMD_LCD_PRINT, row]
            data += self._strtosysex(str)
            self._interfaz._send_sysex(CMD_LCD_DATA, data)

        def clear(self):
            self._interfaz._send_sysex(CMD_LCD_DATA, [CMD_LCD_CLEAR])

        def silence(self):
            self._silenciado = True

        def on(self):
            self._silenciado = False

    class _Servo:
        def __init__(self, interfaz, index):
            self._interfaz = interfaz
            self.index = index
            self._interfaz.set_pin_mode_servo(self.index)

        def position(self, pos):
            self._interfaz.servo_write(self.index, pos)


    class _Output:
        def __init__(self, interfaz, index):
            self._interfaz = interfaz
            self.index = index

        def on(self):
            self._interfaz._send_sysex(CMD_MOTOR_DATA, [CMD_MOTOR_ON, self.index])
            self._interfaz.print("salida "+str(self.index + 1 ), "encendido")


        def off(self):
            self._interfaz._send_sysex(CMD_MOTOR_DATA, [CMD_MOTOR_OFF, self.index])
            self._interfaz.print("salida "+str(self.index + 1 ), "apagado")

        def inverse(self):
            self._interfaz._send_sysex(CMD_MOTOR_DATA, [CMD_MOTOR_INVERSE, self.index])
            self._interfaz.print("salida "+str(self.index + 1 ), "invertido")

        def direction(self, dir):
            if dir > 0:
                dir = 1
            else: dir = 0
            self._interfaz._send_sysex(CMD_MOTOR_DATA, [CMD_MOTOR_DIR, self.index, dir])
            self._interfaz.print("salida "+str(self.index + 1 ), "direccion "+str(dir))

        def speed(self, speed):
            if speed > 100: speed = 100
            if speed < 0: speed = 0
            self._interfaz._send_sysex(CMD_MOTOR_DATA, [CMD_MOTOR_SPEED, self.index, speed & 0x7F, speed >> 7 & 0x7F])
            self._interfaz.print("salida "+str(self.index + 1 ), "potencia "+str(speed))


    class __Sensor:
        def __init__(self):
            self.changeCallback = None
            pass

        def processCallback(self, callback):
            self.changeCallback = callback

        def _changecb(self, data):
            if not (self.changeCallback is None):
                sig = signature(self.changeCallback)
                params = len(sig.parameters)
                if params == 1:
                    self.changeCallback(data[2])
                elif params == 2:
                    self.changeCallback(data[2], data[3])


    class _Analog(__Sensor):
        def __init__(self, interfaz, index):
            self._interfaz = interfaz
            self.index = index
            super().__init__()

        def on(self, callback):
            self.processCallback(callback)
            self._interfaz.set_pin_mode_analog_input(self.index, self._changecb)
            self._interfaz.print("sensor "+str(self.index + 1 ), "reportando")

        def off(self):
            self._interfaz.disable_analog_reporting(self.index)

        def read(self):
            return self._interfaz.analog_read(self.index)[0]

        def set_sampling_interval(self, interval):
            self._interfaz.set_sampling_interval(interval)


    class _Digital(__Sensor):
        def __init__(self, interfaz, index):
            self._interfaz = interfaz
            self.index = index
            super().__init__()

        def on(self, callback):
            self.processCallback(callback)
            self._interfaz.set_pin_mode_digital_input_pullup(self.index, self._changecb)

        def off(self):
            self._interfaz.disable_digital_reporting(self.index)

        def read(self):
            return self._interfaz.digital_read(self.index)[0]



    def __shiftout(self, dataPin, clockPin, isBigEndian = False, value = None):
        if value is None:
            value = isBigEndian
            isBigEndian = True
        for i in range(0, 7):
            self.digital_write(clockPin, 0)
            if isBigEndian:
                self.digital_write(dataPin,  (value & (1 << (7 - i ))) | 0)
            else:
                self.digital_write(dataPin,  (value & (1 << i )) | 0)
            self.digital_write(clockPin, 1)




