import RPi.GPIO as GPIO
import time
import Adafruit_DHT

dht11 = 4#DHT11
trig = 22#Trig датчика HC-SR04
echo = 27#Echo датчика HC-SR04
ph = 18#photoresistor

GPIO.setmode(GPIO.BCM)

GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.setup(ph, GPIO.IN)
GPIO.interruptMode(echo, 'both')
GPIO.setup(ph, GPIO.IN, pull_up_down=GPIO.PUD_UP)

humidity, temperature = Adafruit_DHT.read_retry('11', str(dht11))#читаем т и в

if humidity is not None and temperature is not None:#значения корректны
    print('Temp = ' + temperature + '*C ||| Humidity = ' + humidity + '%')
else:
    humidity = 50
    temperature = 25
    print('Failed to get reading. Try again!')


GPIO.output(trig, GPIO.LOW)
time.sleep(0.5)
GPIO.output(trig, GPIO.HIGH)
time.sleep(1/1000000.0)
GPIO.output(trig, GPIO.LOW)

t = GPIO.pulseInHigh(echo)#длительность сигнала
v = 331.5+0.6*temperature#скорость звука
d = t*v*50#пройденное расстояние

l = GPIO.input(ph)

print('Distance = ' + d + 'cm')
print('Light = ' + l)
 
try:
    while True:
        if GPIO.input(ph) == 0:
            while (GPIO.input(ph) == 0):
                time.sleep(0.1)
            print('Wait a minute')
            time.sleep(60)
            print('Monitoring again')
 
finally:
    print('Cleaning up GPIO')
    GPIO.cleanup()

GPIO.cleanup()
#sudo python3 'имя программы'.py
