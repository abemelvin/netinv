from django.utils import timezone

from .models import Device, Scan, Host, Interface

import docker
from netmiko.ssh_autodetect import SSHDetect
from netmiko.ssh_dispatcher import ConnectHandler
from ntc_templates.parse import parse_output
import time
import os
import json


"""
def execute_scan(scan_pk, scan_username, scan_password):
    client = docker.from_env()
    cwd = os.getcwd()
    devices_dir = cwd + '/history/' + str(scan_pk) + '/devices/'
    discoveries_dir = cwd + '/history/' + str(scan_pk) + '/discoveries/'

    volumes = {
        devices_dir: {'bind': '/tmp/devices', 'mode': 'rw'},
        discoveries_dir: {'bind': '/tmp/discoveries', 'mode': 'rw'},
    }

    devices = Device.objects.all()
    scan = Scan.objects.get(pk=scan_pk)
    dev_total = len(devices)
    dev_scanned = 0

    for i, device in enumerate(devices):
        scan.status = str(dev_scanned) + '/' + str(dev_total) + ' devices'
        scan.save()

        container = client.containers.run(
            'scanner',
            "'{}' '{}' '{}' '{}'".format(device.ip, scan.username, scan.password, device.device_type),
            volumes=volumes,
            detach=True,
        )

        result = container.wait(timeout=120)

        if result['StatusCode'] == 1:
            scan.finish_date = timezone.now()
            scan.status = 'Failed on ' + device.ip
            scan.save()
            return

        device.last_seen = timezone.now()
        dev_scanned += 1

        if not device.first_seen:
            device.first_seen = device.last_seen

        with open(devices_dir + device.ip.replace('.', '-') + '.json') as json_file:
            device_info = json.load(json_file)
            device.device_type = device_info['device_type']
            device.hostname = device_info['hostname']
            device.image = device_info['running_image']
            device.os_version = device_info['version']
            device.uptime = device_info['uptime']
            device.serial = device_info['serial'][0]
            device.mac = device_info['mac'][0].lower().replace(':', '.')
            device.hardware = device_info['hardware'][0]
            device.save()
        
    scan.finish_date = timezone.now()

    if dev_scanned == dev_total:
        scan.status = 'Completed'
    else:
        scan.status = 'Partial Failure'

    scan.username = scan.password = ''
    scan.save()
"""


def execute_scan(scan_pk):

    devices = Device.objects.all()
    scan = Scan.objects.get(pk=scan_pk)
    dev_total = len(devices)
    dev_scanned = 0

    for i, device in enumerate(devices):
        scan.status = str(dev_scanned) + '/' + str(dev_total) + ' devices'
        scan.save()
    
        remote_device = {
            'host': device.ip,
            'username': scan.username,
            'password': scan.password,
            'device_type': device.device_type,
        }

        try:
            if remote_device['device_type'] == 'autodetect':
                guesser = SSHDetect(**remote_device)
                remote_device['device_type'] = guesser.autodetect()

            connection = ConnectHandler(**remote_device)

            if remote_device['device_type'] == 'cisco_ios':

                device_info = parse_output(
                    platform=remote_device['device_type'],
                    command="show version",
                    data=connection.send_command("show version"),
                )[0]

                device.device_type = remote_device['device_type']
                device.hostname = device_info['hostname']
                device.image = device_info['running_image']
                device.os_version = device_info['version']
                device.uptime = device_info['uptime']
                device.serial = device_info['serial'][0]
                device.mac = device_info['mac'][0].lower().replace(':', '.')
                device.hardware = device_info['hardware'][0]
                device.last_seen = timezone.now()

                if not device.first_seen:
                    device.first_seen = device.last_seen

                device.save()

                interface_info = parse_output(
                    platform=remote_device['device_type'],
                    command="show ip int brief",
                    data=connection.send_command("show ip int brief"),
                )

                for item in interface_info:
                    if item['ipaddr'] != 'unassigned':
                        try:
                            host = Host.objects.get(pk=item['ipaddr'])
                            host.delete()
                        except Host.DoesNotExist:
                            pass
                        try:
                            interface = Interface.objects.get(pk=item['ipaddr'])
                            interface.name = item['intf']
                            interface.device = device
                        except Interface.DoesNotExist:
                            interface = Interface(ip=item['ipaddr'], name=item['intf'], device=device)
                        interface.save()

                arp_info = parse_output(
                    platform=remote_device['device_type'],
                    command="show ip arp",
                    data=connection.send_command("show ip arp"),
                )

                for item in arp_info:
                    try:
                        interface = Interface.objects.get(pk=item['address'])
                        interface.mac = item['mac']
                        interface.save()
                        try:
                            host = Host.objects.get(pk=item['address'])
                            host.delete()
                        except Host.DoesNotExist:
                            pass
                    except Interface.DoesNotExist:
                        try:
                            host = Host.objects.get(pk=item['address'])
                            host.mac = item['mac']
                            host.vlan = item['interface']
                            host.last_seen = timezone.now()
                            host.save()
                            host.access_interface.add(Interface.objects.get(device=device, name=item['interface']))
                            host.scans_found.add(scan)
                        except Host.DoesNotExist:
                            host = Host(ip=item['address'], mac=item['mac'], vlan=item['interface'])
                            host.first_seen = timezone.now()
                            host.last_seen = timezone.now()
                            host.save()
                            host.access_interface.add(Interface.objects.get(device=device, name=item['interface']))
                            host.scans_found.add(scan)

                dev_scanned += 1
        
        except:
            continue

    scan.finish_date = timezone.now()

    if dev_scanned == dev_total:
        scan.status = 'Completed'
    else:
        scan.status = 'Partial Failure'

    scan.username = scan.password = ''
    scan.save()