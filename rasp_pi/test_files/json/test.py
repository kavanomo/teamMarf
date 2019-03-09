import serverComms
from time import sleep

i2cComms.writeNumber(0)
sleep(1)

text = input("Command to send: ")
print(text)