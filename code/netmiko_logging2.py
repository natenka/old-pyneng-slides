import logging
from netmiko.cisco.cisco_ios import CiscoIosBase

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("netmiko")
#logging.getLogger("paramiko").setLevel(logging.WARNING)


device_params = {
    'device_type': 'cisco_ios',
    'ip': '192.168.100.1',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco'
}


class MyNetmiko(CiscoIosBase):
    def say_hello(self):
        print('Hello from', self.ip)


r1 = MyNetmiko(**device_params)
print(r1.send_command('sh ip int br'))
r1.say_hello()

