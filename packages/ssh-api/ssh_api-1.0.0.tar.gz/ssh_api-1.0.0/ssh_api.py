import os
import time
import urllib.request

intell_ip = urllib.request.urlopen('http://ident.me').read().decode('utf8')

symb = ('@')
sym = ('\n')
host = input('Host ip: ')
user = input('\nLogin as: ')

all_info = f'--------------------------\nhost: { host }\nuser: { user }\n\n--------------------------'

print( all_info )

my_file = open("ssh.log", "w+")
my_file.write('<INFO :: DATA>\n\nhost-ip="' + host + '"''\nusername="' + user + '"''\n\nYour_Own_IP="' + intell_ip + '"''\n\n<FILE :: INFO>''\n\nTYPE="ssh-logger"\nFORMAT=".log"\nevent.manager="settings./sh"\n')
my_file.close()

os.system('ssh ' + user + symb + host)
