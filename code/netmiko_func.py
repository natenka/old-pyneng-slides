import logging
from netmiko import ConnectHandler


logger = logging.getLogger('superscript.netfunc')
#logger = logging.getLogger('netfunc')

device_params = {
     'device_type': 'cisco_ios',
     'ip': '192.168.100.1',
     'username': 'cisco',
     'password': 'cisco',
     'secret': 'cisco'}


def send_show_command(device, command):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        output = ssh.send_command(command)
        logger.debug('Вывод команды:\n{}'.format(output))
    return output

if __name__ == '__main__':
    send_show_command(device_params, 'sh ip int br')

