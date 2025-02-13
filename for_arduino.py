# '/dev/ttyUSB0'
import serial
from time import sleep

# Настройка подключения к Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)
sleep(2)  # Ждем пару секунд, чтобы плата успела инициализироваться


def send_command(command):
    ser.write(bytes(command + '\n', 'utf-8'))

while True:
    # command = input("Введите команду ('on' или 'off'): ")
    list = ["on", 'off']
    for i in range (len(list)):
        command = list[i]

        if command == 'off':
            print("Отпустить груз")
            send_command('H')
        elif command == 'on':
            print("Взять груз")
            send_command('L')
        else:
            print("Неизвестная команда")

        sleep(5)  # Небольшая пауза между командами


