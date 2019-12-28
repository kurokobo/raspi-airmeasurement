from glob import glob


def read():
    valuefile = open(glob("/sys/bus/w1/devices/28-*")[0] + "/w1_slave")
    text = valuefile.read()
    valuefile.close()

    line = text.split("\n")[1]
    rawdata = line.split(" ")[9]
    temperature = float(rawdata[2:])
    temperature = temperature / 1000

    return {"temperature": temperature}
