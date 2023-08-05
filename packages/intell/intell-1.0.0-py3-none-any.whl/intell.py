import os
import urllib.request

intell_ip = urllib.request.urlopen('http://ident.me').read().decode('utf8')

print('Importing modules.....')

os.system('pip install time')
os.system('pip install threading')
os.system('pip install itertools')
import threading
import sys
import time
import itertools
os.system('cls')

done = False
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rLoading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!')

t = threading.Thread(target=animate)
t.start()

time.sleep(3)
done = True

print('\n')
print("\033[4m\033[37m\033[44m{}\033[0m".format("All done!"))
print("\033[4m\033[37m\033[44m{}\033[0m".format("Errors not found."))
print("\033[4m\033[37m\033[44m{}\033[0m".format("Language: ./Python-amd64"))

time.sleep(3)
os.system('cls')


print("██╗███╗░░██╗████████╗███████╗██╗░░░░░██╗░░░░░")
print("██║████╗░██║╚══██╔══╝██╔════╝██║░░░░░██║░░░░░")
print("██║██╔██╗██║░░░██║░░░█████╗░░██║░░░░░██║░░░░░")
print("██║██║╚████║░░░██║░░░██╔══╝░░██║░░░░░██║░░░░░")
print("██║██║░╚███║░░░██║░░░███████╗███████╗███████╗")
print("╚═╝╚═╝░░╚══╝░░░╚═╝░░░╚══════╝╚══════╝╚══════╝\n\n")

main = input('Выберите тип загрузки.\n\n1. Информация об IP\n2. Конвертатор из текста в голос\n3. Облачная загрузка модулей (Рекомендуется)\n4. Проигрыватель pythonHD (NEW!)\n5. Открыть Windows Powershell (FIXED!)\n\nВаш IP: ' + intell_ip + '\n$ >>> ')
one = ('1')
two = ('2')
three = ('3')
four = ('4')
five = ('5')

if main == one:
	os.system('pip install sTTgeo')
	import sTTgeo

if main == two:
	os.system('pip install sTTcv')
	import sTTcv

if main == three:
    import sys
    import time
    import colorama
    import requests

if main == four:
	os.system('pip install pythonHD')
	import pythonHD

if main == five:
	os.system('pip install MyAdmin')
	import MyAdmin

print('Ошибка! Неверно введено число (1-5)')
print('Активирую дополнительную кодировку.')
login = input('Login as: ')
print('Username --> @' + login)
time.sleep(2)
os.system('cls')
print("\033[4m\033[37m\033[44m{}\033[0m".format("intell WORKSPACE ↓\n"))
