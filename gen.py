#!/home/ssms27/bin/myenv/bin/python3
import yaml
from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader

#GLOBAL VARIABLES
username = 'cisco'
password = 'cisco'
file_location = '/home/ssms27/bin/prj1/'
spt_yml = file_location + 'spt-devices.yml'
dev_j2 = 'device_configs.j2'

''' This section is for reading/rendering YAML files '''
with open(spt_yml) as data:
    yaml_data = data.read()
    yaml_dict = yaml.load(yaml_data, Loader=yaml.FullLoader)

''' This section is for reading/rendering JINJA2 '''
file_loader = FileSystemLoader(file_location)
env = Environment(loader=file_loader)
template = env.get_template(dev_j2)
output = template.render()


''' This section is for connecting to and interacting with Devices '''
for k in yaml_dict.keys():
    ip = yaml_dict[k]['monitor_port_ip']
    port = yaml_dict[k]['monitor_port_port']
    device_type = yaml_dict[k]['device_type']
    try:
        print('Connecting to: ', ip, port, ' with username and password', username, password)
        dev = ConnectHandler(ip=ip, username=username, password=password, port=port, device_type=device_type)
        dev.send_config_set(output)
        # x = dev.send_command('show version')
        # print(x)
    except:
        print('exception occurred')
        pass


