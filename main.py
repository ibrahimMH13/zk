#!/usr/bin/python

import sys
import argparse
from zk import ZK, const
import json
parser = argparse.ArgumentParser()
parser.add_argument("--ip", help="print finger IP Address [required]")
parser.add_argument("--type", help="data type users or attendance [required]")
parser.add_argument("--date", help="date argument must be with format mm/yyyy like 03/2022 [optional]")
args = parser.parse_args()
conn = None
port = 4370
ip = args.ip
op_type = args.type
op_date = args.date
result = dict()
try:
    if ip is None or op_type is None:
        raise Exception('ERROR# missing some required argument')

    zk = ZK(ip, port=port, timeout=1000, password=0, force_udp=False, ommit_ping=False)
    try:
        conn = zk.connect()
        conn.disable_device()
        result['status'] = 'OK'
        result['code'] = 200
        result['firmware_version'] = conn.get_firmware_version()
        result['device_name'] = conn.get_device_name()
        result['device_ip'] = conn.get_network_params()
        if op_type == 'users':
            users = conn.get_users()
            usersList = list()
            for user in users:
                usersList.append({'uid': user.uid, 'name': user.name, 'user_id': user.user_id})
            result['users_count'] = len(users)
            result['users_list'] = usersList
            result['type'] = op_type
            print(json.dumps(result))
        elif op_type == 'attendance':
            attendances = conn.get_attendance()
            attendancesRecord = list()
            for attendance in attendances:
                if op_date:
                    if op_date == str(attendance.timestamp.strftime('%m/%Y')):
                       attendancesRecord.append({'uid': attendance.uid, 'status': attendance.status, 'user_id': attendance.user_id,'timestamp':str(attendance.timestamp),'punch':attendance.punch})
                else:
                    attendancesRecord.append({'uid': attendance.uid, 'status': attendance.status, 'user_id': attendance.user_id,'timestamp':str(attendance.timestamp),'punch':attendance.punch})
            result['all_attendances_count'] = len(attendances)
            result['fetch_attendances__count'] = len(attendancesRecord)
            result['attendances_list'] = attendancesRecord
            result['type'] = op_type
            print(json.dumps(result))

    except Exception as err:
        result['status'] = 'ERROR'
        result['code'] = 505
        result['error_message'] = err
        print(result)
except Exception as error:
    result['status'] = 'ERROR'
    result['code'] = 505
    result['error_message'] = error.__str__()
    print(result)
