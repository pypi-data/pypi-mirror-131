# Copyright (C) <2021>  YUANXIN INFORMATION TECHNOLOGY GROUP CO.LTD and Jinzhe Wang
# This file is part of uitestrunner_syberos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import multiprocessing

import base64
import json
import os
import platform
import re
import threading
import time
import ctypes
from ctypes import *
from subprocess import *
from .selenium_phantomjs.webdriver.remote import webdriver
from .Item import Item
from .Connection import Connection
from .Events import Events
import configparser
from multiprocessing import Process, Pipe
from .Watcher import *
import psutil
import warnings


def _watcher_process(main_pid, host, port, conn):
    device = Device(host=host, port=port, main=False)
    WatchWorker(device, conn, main_pid).run()


def _start_watcher(host, port, watcher_conn):
    watcher_process = Process(target=_watcher_process, args=(os.getpid(), host, port, watcher_conn))
    watcher_process.daemon = True
    watcher_process.start()


def _web_driver_daemon(main_pid, wb_pid, parent_pid):
    psutil.Process(parent_pid).kill()
    main_process = psutil.Process(main_pid)
    wb_process = psutil.Process(wb_pid)
    while main_process.is_running():
        time.sleep(3)
    wb_process.kill()
    exit(0)


def _create_orphan_thread(main_pid, wb_pid):
    wb_daemon_process = Process(target=_web_driver_daemon, args=(main_pid, wb_pid, os.getpid()))
    wb_daemon_process.daemon = False
    wb_daemon_process.start()


def _start_web_driver_daemon(wb_pid):
    orphan_thread = Process(target=_create_orphan_thread, args=(os.getpid(), wb_pid))
    orphan_thread.daemon = False
    orphan_thread.start()


class Device(Events):
    con = Connection()
    __osVersion = ""
    __serialNumber = ""
    xmlStr = ""
    __xpath_file = "./xpath_list.ini"
    __screenshots = "./screenshots/"
    default_timeout = 30
    __syslog_output = False
    __syslog_output_keyword = ""
    __syslog_save = False
    __syslog_save_path = "./syslog/"
    __syslog_save_name = ""
    __syslog_save_keyword = ""
    watcher_list = []
    __main_conn, __watcher_conn = Pipe()
    __width = 0
    __height = 0
    __syslog_tid = None
    """
    control_host_type:
        0: anywhere
        1: windows amd64
        2: linux x86_64
        3: darwin x86_64
    """
    control_host_type = 0

    def __init__(self, host="192.168.100.100", port=10008, main=True):
        super().__init__(d=self)
        warnings.simplefilter('ignore', ResourceWarning)
        self.con.host = host
        self.con.port = port
        self.con.connect()
        self.__path = os.path.realpath(__file__).split(os.path.basename(__file__))[0]
        self.__serialNumber = str(self.con.get(path="getSerialNumber").read(), 'utf-8')
        self.__osVersion = str(self.con.get(path="getOsVersion").read(), 'utf-8')
        self.__set_display_size()
        if main:
            self.__check_platform()
            if self.control_host_type != 0:
                _start_web_driver_daemon(self.__wb_process.pid)
                _start_watcher(host, port, self.__watcher_conn)
            syslog_thread = threading.Thread(target=self.__logger)
            syslog_thread.setDaemon(True)
            syslog_thread.start()
        self.refresh_layout()
        if self.control_host_type != 0:
            self.webdriver = webdriver.WebDriver(command_executor='http://127.0.0.1:8910/wd/hub')

    def __check_platform(self):
        p = platform.system()
        m = platform.machine()
        if p == "Windows" and m == "AMD64":
            self.control_host_type = 1
            self.__init_webdriver("win32_x86_64_phantomjs", "libsimulation-rendering.dll")
        elif p == "Linux" and m == "x86_64":
            self.control_host_type = 2
            self.__init_webdriver("linux_x86_64_phantomjs", "libsimulation-rendering.so")
        elif p == "Darwin" and m == "x86_64":
            self.control_host_type = 3
            self.__init_webdriver("darwin_x86_64_phantomjs", "libsimulation-rendering.dylib")

    def __init_webdriver(self, p_name, l_name):
        self.__wb_process = Popen([self.__path + "data/" + p_name, self.__path + "data/ghostdriver/main.js", str(self.__width), str(self.__height)], stdout=PIPE, stderr=PIPE)
        for i in range(2):
            self.__wb_process.stdout.readline()
        ll = cdll.LoadLibrary
        self.libsr = ll(self.__path + "data/" + l_name)
        self.libsr.go.restype = ctypes.c_char_p

    def push_watcher_data(self):
        self.__main_conn.send({'watcher_list': self.watcher_list})

    def watcher(self, name: str):
        w = Watcher({'name': name}, self)
        return w

    def __logger_pingpong(self):
        self.con.get(path="SSEPingpong", args="tid=" + str(self.__syslog_tid))
        threading.Timer(5, self.__logger_pingpong).start()

    def __logger(self):
        syslog_save_path = ""
        syslog_file = None
        first = True
        messages = self.device.con.sse("SysLogger")
        for msg in messages:
            log_str = str(msg.data)
            if first:
                self.__syslog_tid = log_str
                threading.Timer(5, self.__logger_pingpong).start()
                first = False
            if self.__syslog_output and re.search(self.__syslog_output_keyword, log_str):
                print(log_str)
            if self.__syslog_save and re.search(self.__syslog_save_keyword, log_str):
                if syslog_save_path != self.__syslog_save_path + "/" + self.__syslog_save_name:
                    syslog_save_path = self.__syslog_save_path + "/" + self.__syslog_save_name
                    if not os.path.exists(self.__syslog_save_path):
                        os.makedirs(self.__syslog_save_path)
                    syslog_file = open(syslog_save_path, 'w')
                syslog_file.write(log_str + "\n")
                syslog_file.flush()

    def set_syslog_output(self, is_enable, keyword=""):
        self.__syslog_output_keyword = keyword
        self.__syslog_output = is_enable

    def syslog_output(self):
        return self.__syslog_output

    def syslog_output_keyword(self):
        return self.__syslog_output_keyword

    def set_syslog_save_start(self, save_path="./syslog/", save_name=None, save_keyword=""):
        self.__syslog_save_path = save_path
        if save_name is None:
            current_remote_time = self.con.get(path="getSystemTime").read()
            self.__syslog_save_name = str(current_remote_time, 'utf-8') + ".log"
        self.__syslog_save_keyword = save_keyword
        self.__syslog_save = True

    def set_syslog_save_stop(self):
        self.__syslog_save = False

    def syslog_save(self):
        return self.__syslog_save

    def syslog_save_path(self):
        return self.__syslog_save_path

    def syslog_save_name(self):
        return self.__syslog_save_name

    def syslog_save_keyword(self):
        return self.__syslog_save_keyword

    def set_default_timeout(self, timeout):
        self.default_timeout = timeout

    def set_xpath_list(self, path):
        self.__xpath_file = path

    def set_screenshots_path(self, path):
        self.__screenshots = path

    def screenshot(self, path=__screenshots):
        if not os.path.exists(path):
            os.makedirs(path)
        img_base64 = str(self.con.get(path="getScreenShot").read(), 'utf-8').split(',')[0]
        current_remote_time = self.con.get(path="getSystemTime").read()
        file_name = str(current_remote_time, 'utf-8') + ".png"
        image = open(path + "/" + file_name, "wb")
        image.write(base64.b64decode(img_base64))
        image.close()
        return file_name

    def __set_display_size(self):
        image_data = str(self.con.get(path="getScreenShot").read(), 'utf-8')
        self.__height = int(image_data.split(",")[1])
        self.__width = int(image_data.split(",")[2])

    def display_width(self):
        return self.__width

    def display_height(self):
        return self.__height

    def get_xpath(self, sop_id, key):
        if not os.path.exists(self.__xpath_file):
            f = open(self.__xpath_file, "w")
            f.close()
        conf = configparser.ConfigParser()
        conf.read(self.__xpath_file)
        return conf.get(sop_id, key)

    def refresh_layout(self):
        self.xmlStr = str(self.con.get(path="getLayoutXML").read(), 'utf-8')

    def os_version(self):
        return self.__osVersion

    def serial_number(self):
        return self.__serialNumber
    
    def find_item_by_xpath_key(self, sopid, xpath_key):
        i = Item(d=self, s=sopid, xpath=self.get_xpath(sopid, xpath_key))
        return i

    def find_item_by_xpath(self, sopid, xpath):
        i = Item(d=self, s=sopid, xpath=xpath)
        return i
