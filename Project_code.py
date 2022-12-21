#programmed using python microbit makecode 
class Project:
    def __init__(self):
        # pins
        IN1_PIN = pins.P1
        IN2_PIN = pins.P2
        ENA_PIN = pins.P0
        TEMP_PIN = pins.P8
        # Values
        self.pump_speed = 0
        self.temp = 0
        self.bat_voltage = 0
        self.gen_voltage = 0
        self.charging_status = 'Not Charging'
        self.charge = 100
        # i2c init
        I2C_LCD1602.LcdInit(39)
        I2C_LCD1602.clear()
        #DHT11 init
        dht11_dht22.select_temp_type(tempType.CELSIUS)
        dht11_dht22.query_data(DHTtype.DHT11, DigitalPin.P8, True, False, True)
        #set H bridge rotation  
        pins.digital_write_pin(DigitalPin.P1, 0)
        pins.digital_write_pin(DigitalPin.P2, 1)
        pins.analog_write_pin(AnalogPin.P0, 0)
    
    def get_temp(self):
        self.temp = dht11_dht22.read_data(dataType.TEMPERATURE)
    
    def set_motor_speed(self, speed=0): 
        self.pump_speed = 10*speed
        pins.analog_write_pin(AnalogPin.P0, self.pump_speed)
     
    
    def get_battery_voltage(self):  
        self.bat_voltage = 3.89
     
    
    def get_generator_voltage(self):  
        self.gen_voltage = 10.2
     
    
    def update_values(self, rep): 
        if rep == 1:
            I2C_LCD1602.clear()
            I2C_LCD1602.ShowString("Water Temp:",0, 0)
            self.get_temp()
            I2C_LCD1602.ShowString(self.temp +'C', 5, 1)
        if rep == 2:
            I2C_LCD1602.clear()
            I2C_LCD1602.ShowString("Motor Speed:",0, 0)
            I2C_LCD1602.ShowString(self.pump_speed +'%', 6, 1)
        if rep == 3:
            I2C_LCD1602.clear()
            I2C_LCD1602.ShowString("Generator Volts:",0, 0)
            self.get_generator_voltage()
            I2C_LCD1602.ShowString(self.gen_voltage +'V', 5, 1)
        if rep == 4:
            I2C_LCD1602.clear()
            I2C_LCD1602.ShowString("Battery: Charged:",0, 0)
            self.get_battery_voltage()
            I2C_LCD1602.ShowString(self.bat_voltage +'V     '+ self.charge+ "%", 1, 1)
        if rep == 5:
            I2C_LCD1602.clear()
            I2C_LCD1602.ShowString("Battery Status:",0, 0)
            if self.charging_status == 'Not Charging':
                I2C_LCD1602.ShowString(self.charging_status, 2, 1)
            else:
                I2C_LCD1602.ShowString(self.charging_status, 4, 1) 

    def update_screen(self):
        SWEG. update_values(1)
        basic.pause(2000)
        SWEG. update_values(2)
        basic.pause(2000)
        SWEG. update_values(3)
        basic.pause(2000)
        SWEG. update_values(4)
        basic.pause(2000)
        SWEG. update_values(5)
        basic.pause(2000)


SWEG = Project()
def on_forever():
    SWEG.update_screen()

basic.forever(on_forever)
