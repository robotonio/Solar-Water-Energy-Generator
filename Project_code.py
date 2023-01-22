class Project:
    def __init__(self):
        # Values
        self.pump_speed = 0
        self.temp = 0
        self.bat_voltage = 3.92
        self.gen_voltage = 0
        self.charging_status = 'Charging' #'Not Charging'
        self.charge = 100
        self.fan = 0#1 if fan runs
        self.pump = 0#1 if pump runs
        # i2c init
        I2C_LCD1602.LcdInit(39)
        I2C_LCD1602.clear()
        I2C_LCD1602.clear()
        #init screen 
        I2C_LCD1602.show_string("Moving Minds", 2, 0)
        I2C_LCD1602.show_string("Project!", 4, 1)        
        #init pump and fan
        self.turn_off_fan()
        self.turn_off_pump()

        self.set_battery_voltage()
        self.set_charging_status()

    def get_temp(self):
        val = smarthome.read_temperature(TMP36Type.TMP36_TEMPERATURE_C, AnalogPin.P0)
        self.temp = val+10

    def set_motor_speed(self, speed=0): 
        self.pump_speed = 10*speed
        pins.analog_write_pin(AnalogPin.P0, self.pump_speed)

    def set_battery_voltage(self):
        self.bat_voltage = 12.6
            
    def set_charging_status(self):
        if self.gen_voltage > 0:
            self.charging_status = "Charging"
        else:
            self.charging_status = "Not Charging"

    def get_battery_voltage(self):  
        self.bat_voltage = 12.5
    
    def get_battery_percentage(self):
        val = self.bat_voltage
        return (val/12.6)*100

    def turn_off_fan(self):
        self.fan = 1
        pins.digital_write_pin(DigitalPin.P2, 1)

    def turn_on_fan(self):
        self.fan = 0
        pins.digital_write_pin(DigitalPin.P2, 0)

    def turn_off_pump(self):
        self.pump = 1
        self.pump_speed = 0
        pins.digital_write_pin(DigitalPin.P12, 1)

    def turn_on_pump(self):
        self.pump = 0
        self.pump_speed = 100
        pins.digital_write_pin(DigitalPin.P12, 0)

    def get_generator_voltage(self):  
        analog_input = pins.analog_read_pin(AnalogPin.P1)
        voltage = Math.map(analog_input, 0, 1023, 0, 10)
        self.gen_voltage = Math.round_with_precision(voltage, 2)
                
    def print_value(self, value):
        I2C_LCD1602.clear()
        I2C_LCD1602.show_number(value, 0, 0)
     
    def update_values(self, rep): 
        if rep == 1:
            I2C_LCD1602.clear()
            I2C_LCD1602.ShowString("Water side Temp:",0, 0)
            self.get_temp()
            I2C_LCD1602.ShowString(self.temp +'C', 6, 1)
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

SWEG = Project()
counter=1
threshold = 50
SWEG.turn_on_fan()

def on_button_pressed_a():
    global counter
    if counter < 0 or counter > 5:
            counter = 1
    else:
        counter = counter + 1

    SWEG.update_values(counter)
            
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    global counter
    if counter < 0 or counter > 5:
            counter = 1
    else:
        counter = counter - 1

    SWEG.update_values(counter)
            
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_forever():

    #SWEG.get_generator_voltage()
    SWEG.get_temp()
    if SWEG.temp < threshold:
        SWEG.turn_on_pump()
    else:
        SWEG.turn_off_pump()

basic.forever(on_forever)
