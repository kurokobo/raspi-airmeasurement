# Use Raspberry Pi as air measurement device

This repository includes files for:

* Measure air condition using some sensors connected to Raspberry Pi
    * **CO2 Concentration** using **MH-Z19B**
    * **Temperature** using **BME280** or **DS18B20**
    * **Humidity** using **BME280**
    * **Air Pressure** using **BME280**
* Publish these values to MQTT broker


## Use MH-Z19B

MH-Z19B can measure CO2 concentration.


### Layout

| Sensor Side | Raspberry Pi Side |
|-|-|
| GND | GND |
| Vin | 5 V |
| TXD | RXD (8) |
| RXD | TXD (10) |


### Raspberry Pi configuration

MH-Z19B use UART. You have to enable Serial port and disable Shell over Serial.

```sh
$ sudo raspi-config nonint do_serial 2
```


## Use BME280

BME280 can measure temperature, humidity, and air pressure.


### Layout

| Sensor Side | Raspberry Pi Side |
|-|-|
| GND | GND |
| VCC | 3.3 V |
| SCL | `GPIO3` (5) |
| SDA | `GPIO2` (3) |


### Raspberry Pi configuration

BME280 use I2C. You have to enable this feature.

```sh
$ sudo raspi-config nonint do_i2c 0
```

You can check connectivity by `i2cdetect` command. If you can see `0c76` as follows, it's connected correctly.

```sh
$ sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- 76 --            
```

## Use DS18B20

DS18B20 can measure temperature.


### Layout

| Sensor Side | Raspberry Pi Side |
|-|-|
| GND | GND |
| Vin | 3.3 V |
| Signal | `GPIO4` (7) |


### Raspberry Pi configuration

DS18B20 use interface called "One-Wire". You have to enable this feature.

```sh
$ sudo raspi-config nonint do_onewire 0
$ sudo reboot
```

The first One-Wire bus has to be connected `GPIO4` (7).

If you want to use a pin other than `GPIO4`, append strings `,gpiopin=4` to the end of of `dtoverlay=w1-gpio` and reboot.

```sh
$ sudo vi /boot/config.txt
$ grep dtoverlay=w1-gpio /boot/config.txt
dtoverlay=w1-gpio,gpiopin=4
$ sudo reboot
```

And then load some modules.

```sh
$ sudo modprobe w1-gpio
$ sudo modprobe w1-therm
```

Then you can see the directory start with `28-` in `/sys/bus/w1/devices` directory. 

The file `w1_slave` in this directory includes current temperature.

```sh
pi@raspberrypi:~ $ cat /sys/bus/w1/devices/28-01186d8e8fff/w1_slave 
7a 01 4b 46 7f ff 0c 10 ec : crc=ec YES
7a 01 4b 46 7f ff 0c 10 ec t=23625
```

In this example, the value `t=23625` means 23.625 degrees Celsius.

