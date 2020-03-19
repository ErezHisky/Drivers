import time
from Drivers.RUDAT_USB import *


class DigAtt64:
    def __init__(self):
        self.U1 = USBDAT()
        sn = self.read_sn()

    def read_sn(self):
        s1 = self.U1.ReadSN()
        return s1

    def read_model(self):
        s1 = self.U1.Send_SCPI(":MN?")
        return s1

    def set_attenuation(self, atten=12.5):
        s1 = self.U1.Send_SCPI(f":SETATT:{atten}")
        return s1

    def get_att(self):
        s1 = self.U1.Send_SCPI(":ATT?")
        return s1


if __name__ == "__main__":
    myAtt = DigAtt64()
    print(myAtt.read_sn())
    print(myAtt.get_att())
    print(myAtt.read_model())
    myAtt.set_attenuation(30.25)
    print(myAtt.get_att())
    print('Done')

