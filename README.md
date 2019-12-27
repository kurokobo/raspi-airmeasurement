# Thermohygrometer for Raspberry Pi

## Layout

### Thermistor (DS18B20)

| Sensor | RasPi |
|-|-|
| - | GND |
| + | 3.3 V |
| S | 7 |

The DS18B20 use interface called "One-Wire". The first One-Wire bus has to be connected `GPIO4` (7).

First of all you have to modify configuration file of Raspibian and reboot.

```sh
$ sudo echo "dtoverlay=w1-gpio" >> /boot/config.txt
$ sudo reboot
```

If you want to use a pin other than `GPIO4`, you can specify pin number as follows:

```sh
$ sudo echo "dtoverlay=w1-gpio,gpiopin=4" >> /boot/config.txt
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

The value `t=23625` means 23.625 degrees Celsius.


