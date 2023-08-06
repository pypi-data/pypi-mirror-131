#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
It is aimed to integrate Google adb Tool into an application made/will made
with Python and to provide ease of use.
"""

__author__ = 'ibrahim CÖRÜT'
__email__ = 'ibrhmcorut@gmail.com'

import platform
import threading
from ..DateTime import add_date_time_to_line
from ..OS import get_path_home, join_directory, try_except
from ..ParallelProcessing import ThreadWithReturnValue
from ..Shell import run_cmd, run_cmd_2, print_error
from ppadb.client import Client as _Client


class Client:
    def __init__(self):
        self.__adb_path = self.get_path()
        self.__client = None
        self.__device = None
        self.__lock = None
        self.__reader_status_pause = False
        self.__reader_status = False
        self.__thread = None
        self.data = None
        self.device = None
        self.devices = None

    @staticmethod
    def get_path():
        if platform.system() == 'Windows':
            return join_directory([get_path_home(), '.GoogleADB', 'adb.exe'])
        else:
            return 'adb'

    @try_except
    def get_devices(self):
        print(f'Google ADB Application Path:{self.__adb_path}')
        run_cmd(f'{self.__adb_path} version')
        self.devices = ['None']
        for device in run_cmd_2(f'{self.__adb_path} devices', do_combine=True).splitlines():
            if '\tdevice' in device:
                self.devices.append(device.strip('\tdevice').strip(':5555'))
        print(f'Google Devices List:{self.devices}')
        return self.devices

    def connect(self, device=None):
        self.device = self.device if device is None else device
        if self.device:
            try:
                self.__client = _Client(host='127.0.0.1', port=5037)
                print(f'{self.__adb_path} Version:%s' % self.__client.version())
                if self.device.replace('.', '').isdigit() and len(self.device.split('.')) == 4:
                    self.__client.remote_connect(self.device, 5555)
                    self.device = f'{self.device}:5555'
                self.__device = self.__client.device(device)
                print(f':::::::::::> ADB Connected successfully Device:{self.device}')
            except ConnectionRefusedError as error:
                print(f'#########> ADB CONNECTION ERROR! :::>{error}')
            except Exception as error:
                print_error(error, locals())
                self.disconnect()

    def disconnect(self):
        self.__reader_status = False
        if self.__thread:
            self.__thread.stop()
        run_cmd(f'{self.__adb_path} disconnect {self.device}')
        self.__device = None
        print(':::::::::::> ADB connection was disconnected successfully')

    def shell(self, command):
        result = None
        try:
            print(f'-----> ADB Shell Command:{command}')
            self.__device = self.__client.device(self.device)
            result = str(self.__device.shell(command))
        except Exception as error:
            print(f"#########> ADB Shell problem:::>{error}")
        return result

    def pull(self, source, target):
        try:
            self.__device = self.__client.device(self.device)
            self.__device.pull(source, target)
            print(f'-----> ADB Pull Source:{source} --- Target:{target}')
            return True
        except Exception as error:
            print(f"#########> ADB Pull problem:::>{error}")
            return False

    def push(self, source, target):
        try:
            self.__device = self.__client.device(self.device)
            self.__device.push(source, target)
            print(f'-----> ADB Push Source:{source} --- Target:{target}')
        except Exception as error:
            print(f"#########> ADB Push problem:::>{error}")

    def install_or_uninstall(self, process, package):
        try:
            self.__device = self.__client.device(self.device)
            if str(process).lower() == 'install':
                self.__device.install(package, test=True, reinstall=True)
            if str(process).lower() == 'uninstall':
                self.__device.uninstall(package)
            print(f'-----> ADB {str(process).title()}ed:{self.device} --- {package}')
        except Exception as error:
            print(f"#########> ADB Install or Uninstall problem for  --- {package}:::::::>{error}")

    def grab_image(self, path):
        try:
            self.__device = self.__client.device(self.device)
            result = self.__device.screencap()
            with open(path, "wb") as fp:
                fp.write(result)
            print(f'-----> ADB Device:{self.device} Capture image successfully received: {path}')
            return True
        except Exception as error:
            print(f'-----> There was a problem while capturing the ADB device image: {error}')
            return False

    def start_log_reader(self):
        try:
            self.__reader_status = True
            self.__thread = ThreadWithReturnValue(
                target=self.__start_log_reader,
                name=f'ADB LOGCAT {self.device}',
                daemon=True
            )
            self.__thread.start()
        except (KeyboardInterrupt, SystemExit) as error:
            print(f'-------------> Error Thread ADB Logcat Reader:{error}')
            self.disconnect()
            self.__reader_status_pause = False

    def __start_log_reader(self):
        self.__device = self.__client.device(self.device)
        self.__device.shell("logcat -c")
        self.__device.shell("logcat", handler=self.dump_logcat)

    def dump_logcat(self, connection):
        self.__lock = threading.Lock()
        self.data = [f'<::::::: Logcat Log Read Start :::::::> {self.device}\n']
        print(f'-------------> ADB Logcat Reader Start:{self.device}')
        stream = connection.socket.makefile('rwb', encoding='utf8')
        while self.__reader_status:
            try:
                if not self.__reader_status_pause:
                    line = stream.readline()
                    if len(line) > 0:
                        self.__lock.acquire()
                        self.data.append(
                            add_date_time_to_line(
                                line.rstrip().decode(encoding='UTF-8', errors='ignore')
                            )
                        )
                        self.__lock.release()
            except Exception as error:
                print(f'-------------> Error ADB Logcat Reader:{error}')
        stream.close()
        connection.close()
        print(f'-------------> ADB Logcat Reader Stopped:{self.device}')

    def data_clean(self, status):
        if status == 'End':
            self.__reader_status_pause = True
            self.__lock.acquire()
            self.data.append(f'<::::::: Logcat Log Read End :::::::> {self.device}\n')
            self.__lock.release()
        elif status == 'Start':
            self.__lock.acquire()
            self.data.clear()
            self.data = [f'<::::::: Logcat Log Read Start :::::::> {self.device}\n']
            self.__lock.release()
            self.__reader_status_pause = False
