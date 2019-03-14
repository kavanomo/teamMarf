# Pressure

# Based heavily on the BMP085 library provided by Adafruit found at
# https://github.com/adafruit/Adafruit_Python_BMP/blob/master/Adafruit_BMP/BMP085.py  
# also includes 'get height'

from __future__ import division
import logging
import time

#Registers and stuff;

BMP280_I2CADDR           = 0x76 # Can be set to 0x77 through wiring
BMP280_CHIPID            = 0x58

BMP280_REGISTER_DIG_T1              = 0x88
BMP280_REGISTER_DIG_T2              = 0x8A
BMP280_REGISTER_DIG_T3              = 0x8C

BMP280_REGISTER_DIG_P1              = 0x8E
BMP280_REGISTER_DIG_P2              = 0x90
BMP280_REGISTER_DIG_P3              = 0x92
BMP280_REGISTER_DIG_P4              = 0x94
BMP280_REGISTER_DIG_P5              = 0x96
BMP280_REGISTER_DIG_P6              = 0x98
BMP280_REGISTER_DIG_P7              = 0x9A
BMP280_REGISTER_DIG_P8              = 0x9C
BMP280_REGISTER_DIG_P9              = 0x9E

BMP280_REGISTER_CHIPID             = 0xD0
BMP280_REGISTER_VERSION            = 0xD1
BMP280_REGISTER_SOFTRESET          = 0xE0

BMP280_REGISTER_CAL26              = 0xE1  #R calibration stored in 0xE1-0xF0

BMP280_REGISTER_CONTROL            = 0xF4
BMP280_REGISTER_CONFIG             = 0xF5
BMP280_REGISTER_PRESSUREDATA       = 0xF7
BMP280_REGISTER_TEMPDATA           = 0xFA


class BMP280(object):
    def __init__(self, address=BMP280_I2CADDR, i2c=None, **kwargs):
        # Create I2C device.
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._device = i2c.get_i2c_device(address, **kwargs)
        #initialize t_fine
        self.t_fine = 0 
        #default value for atmospheric pressure
        self.p_neutral = 98000
        # Load calibration values.
        self._load_calibration()
        self._device.write8(BMP280_REGISTER_CONTROL, 0x3F)

    def _load_calibration(self):
        self.cal_dig_T1 = self._device.readU16LE(BMP280_REGISTER_DIG_T1)
        self.cal_dig_T2 = self._device.readS16LE(BMP280_REGISTER_DIG_T2)
        self.cal_dig_T3 = self._device.readS16LE(BMP280_REGISTER_DIG_T3)

        self.cal_dig_P1 = self._device.readU16LE(BMP280_REGISTER_DIG_P1)
        self.cal_dig_P2 = self._device.readS16LE(BMP280_REGISTER_DIG_P2)
        self.cal_dig_P3 = self._device.readS16LE(BMP280_REGISTER_DIG_P3)
        self.cal_dig_P4 = self._device.readS16LE(BMP280_REGISTER_DIG_P4)
        self.cal_dig_P5 = self._device.readS16LE(BMP280_REGISTER_DIG_P5)
        self.cal_dig_P6 = self._device.readS16LE(BMP280_REGISTER_DIG_P6)
        self.cal_dig_P7 = self._device.readS16LE(BMP280_REGISTER_DIG_P7)
        self.cal_dig_P8 = self._device.readS16LE(BMP280_REGISTER_DIG_P8)
        self.cal_dig_P9 = self._device.readS16LE(BMP280_REGISTER_DIG_P9)

    def _read24(self,register):
        '''read 3 bytes of data from the requested register'''
        bytes = self._device.readList(register,3)
        return ((bytes[0] << 16) + (bytes[1] << 8) + bytes[2])
    
    def read_raw_temp(self):
        '''read raw temperature data'''
        return self._read24(BMP280_REGISTER_TEMPDATA)
        
    def read_raw_pressure(self):
        '''read raw pressure data '''
        return self._read24(BMP280_REGISTER_PRESSUREDATA)

    def read_temperature(self):
        '''read temperature in celcius'''
        UT = self.read_raw_temp()/16
        
        #X1 = (((((UT>>3)-self.cal_dig_T1)*(self.cal_dig_T2))>>11
        #X2 = (((((UT>>4)-self.cal_dig_T1)*((UT>>4)-self.cal_dig_T1))
        #     >> 12) * self.cal_dig_T3) >> 14
                  
        #B5 = X1+X2
        #temp = (B5*5+128) >> 8;
        #return temp/100 
        
        
        var1 = (UT / 16384.0 - self.cal_dig_T1 / 1024.0) * self.cal_dig_T2
#   print "var1 " + str(var1)
        var2 = ((UT / 131072.0 - self.cal_dig_T1 / 8192.0) * (
            UT / 131072.0 - self.cal_dig_T1 / 8192.0)) * self.cal_dig_T3
#   print "var2 " + str(var2)
        #print("t_fine: ", self.t_fine)
        self.t_fine = int(var1 + var2)
#   print "tfine " + str(self.t_fine)
        temperature = self.t_fine / 5120.0
        return temperature
        
            
    def read_pressure(self):
        '''read pressure in Pa'''
        UP = self.read_raw_pressure()/16
        
        var1 = float(self.t_fine) / 2.0 - 64000.0
 #       print "var1 " + str(var1)
        var2 = var1 * var1 * self.cal_dig_P6 / 32768.0
 #       print "var2 " + str(var2)
        var2 = var2 + var1 * self.cal_dig_P5 * 2.0
 #       print "var2 " + str(var2)
        var2 = var2 / 4.0 + self.cal_dig_P4 * 65536.0
 #       print "var2 " + str(var2)
        var1 = (self.cal_dig_P3 * var1 * var1 / 524288.0 +
                self.cal_dig_P2 * var1) / 524288.0
 #       print "var1 " + str(var1)
        var1 = (1.0 + var1 / 32768.0) * self.cal_dig_P1
 #       print "var1 " + str(var1)
        if var1 == 0:
            return 0
        p = 1048576.0 - UP
 #       print "p " + str(p)
        p = ((p - var2 / 4096.0) * 6250.0) / var1
 #       print "p " + str(p)
        var1 = self.cal_dig_P9 * p * p / 2147483648.0
 #       print "var1 " + str(var1)
        var2 = p * self.cal_dig_P8 / 32768.0
 #       print "var2 " + str(var2)
        p = p + (var1 + var2 + self.cal_dig_P7) / 16.0
        return p
        
    def confirm_chipid(self):
        '''check if the chip id is what it's supposed to be'''
        return BMP280_CHIPID == self._device.readU8(BMP280_REGISTER_CHIPID)
        
    def set_neutral_pressure(self, p):
        '''change the neutral pressure used for depth calculations'''
        self.p_neutral = p

    def read_neutral_pressure(self):
        self.p_neutral = self.read_pressure()
        
    def read_depth(self):
        '''return the depth below surface based on neutral pressure,
        in metres'''
        pressure = self.read_pressure()
        #calculation: h = P/(rho * g)
        depth = (pressure - self.p_neutral) / (998 * 9.82)
        return depth
        
    def set_filter(self):
        curr = self._device.readU8(BMP280_REGISTER_CONFIG)
        curr = curr & 0xF7 # 111 1 0111
        self._device.write8(BMP280_REGISTER_CONFIG,curr)
        
  
def pressure():
  return BMP280.read_temperature()
''' 
if __name__ == "__main__":
    #import sys for testing
    import sys
    print("Checking for your BMP280...")
    BMP280 = BMP280()
    if ( BMP280.confirm_chipid() == False ):
        print("BMP280 not found! Check your wiring!")
        print("Press any key to exit")
        #wait for key press
        input()
        sys.exit()
    
    print ("Press Enter to display more values" +
          "\n or any other key to break")

    inp = ''
    while (inp == ''):
        
        print("Temperature: " + str(BMP280.read_temperature()) + " C")
        print("Pressure: " + str(BMP280.read_pressure()) + " Pa")
        inp = input()
'''