# '/dev/ttyUSB0'

import serial
from time import sleep

# Настройка подключения к Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)
sleep(2)  # Ждем пару секунд, чтобы плата успела инициализироваться


def send_command(command):
    ser.write(bytes(command + '\n', 'utf-8'))


while True:
    command = input("Введите команду ('on' или 'off'): ")

    if command == 'on':
        print("Включаем светодиод")
        send_command('H')
    elif command == 'off':
        print("Выключаем светодиод")
        send_command('L')
    else:
        print("Неизвестная команда")

    sleep(1)  # Небольшая пауза между командами

send_command(on)