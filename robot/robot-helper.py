#!/usr/bin/env python

import sys


from yaml import load
from yaml import Loader
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager

ROBOT_TEST_FILE = 'robot/vxlan-verify.robot'
ROBOT_REPORT_DIR = 'robot/reports'
ROBOT_REPORT_ARCH_FILE = 'robot_reports.tar.gz'

def get_services_by_state(data, state):
    result = []
    for item in data:
        if item['state'] == state:
            result.append(str(item['vni']))
    return result

if __name__ == '__main__':
    inventory_file_name = sys.argv[1]
    hosts_group = sys.argv[2]
    underlay_vars_file = sys.argv[3]
    service_vars_file = sys.argv[4]

    data_loader = DataLoader()
    inventory = InventoryManager(loader=data_loader, sources=[inventory_file_name])
    hosts = inventory.get_groups_dict()[hosts_group]

    underlay_dict = load(open(underlay_vars_file), Loader=Loader)
    services_dict = load(open(service_vars_file), Loader=Loader)

    l3vnis_str = ",".join(get_services_by_state(services_dict['l3_vnis'], 'present'))
    l2vnis_str = ",".join(get_services_by_state(services_dict['l2_vnis'], 'present'))

    with open('robot/run.sh', 'w') as fh:
        fh.write('#!/bin/bash\n')
        fh.write('\n\nEXIT_STATUS=0\n\n')
        for host in hosts:
            interfaces = map(lambda d: d['name'], underlay_dict['routed_underlay_if'][host])
            interfaces_str = ",".join(interfaces)

            fh.write('echo ""\n')
            fh.write('echo ""\n')
            fh.write('echo "#"\n')
            fh.write('echo "# Start Robot tests for {}"\n'.format(host))
            fh.write('echo "#"\n')
            fh.write('NXOS_DEVICE={} NXOS_UNDERLAY_IF_LIST={} NXOS_EVPN_L2VNI_LIST={} NXOS_EVPN_L3VNI_LIST={}'
                  ' robot -d {}/{} {} || EXIT_STATUS=$?\n\n'.format(host, interfaces_str, l2vnis_str, l3vnis_str,
                                              ROBOT_REPORT_DIR, host, ROBOT_TEST_FILE))
        fh.write('\nexit $EXIT_STATUS\n\n')
