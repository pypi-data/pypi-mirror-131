# -*- coding: utf-8 -*-
"""
this class represents the Toptica DLC pro laser controller
"""

import socket, re
import time, threading
import numpy as np

pattern = r'.*voltage-set\s(-?\d+\.{1}\d{2,}).*'
rule = re.compile(pattern)

class topticaLaser(object):
    
    def __init__(self, ip, timeout = 3, port = 1998):
        
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.open()

        self._voltage = -1
        self._isLock = False
        self._desFre = -1
        self._currentFre = -1
        self._pid = [-200,0,0]
        
        self.autoUpdate = threading.Thread(target=self.updateVol)
        self.autoUpdate.setDaemon(True)
        self.autoUpdate.start()

        self.laserLockThread = threading.Thread(target=self.laserLock)
        self.laserLockThread.setDaemon(True)
        self.laserLockThread.start()

        # clear possible return value
        time.sleep(0.1) 

    def open(self):
        try:
            self._socket_get = socket.socket()
            self._socket_set = socket.socket()
            self._socket_get2 = socket.socket()

            if self.timeout is not None:
                self._socket_get.settimeout(self.timeout)
                self._socket_set.settimeout(self.timeout)
                self._socket_get2.settimeout(self.timeout)

            self._socket_set.connect((self.ip, self.port))
            self._socket_get.connect((self.ip, self.port+1))
            self._socket_get2.connect((self.ip, self.port+1))
            
            print('Toptica DLC pro at ip address ' + str(self.ip) + ' is online')
            time.sleep(0.5)

        except:
            print('connection to Toptica DLC pro at address' + str(self.ip) + ' FAILED!')
        
        # check for system health and print the response
        self._socket_set.send(("(param-ref 'system-health-txt)" + "\r\n").encode('utf-8'))

    def updateVol(self):
        while True :
            sleepTime  = 1
            if self._isLock:
                sleepTime = 0.1
            vol = self.get_voltage()

            if self.ip == "192.168.1.25" and np.random.rand() > 0.7:
                self._voltage = vol + 0.02*(np.random.rand() - 0.5)

            elif vol != -1 and vol > -2 and vol < 100:
                if self._voltage == -1 or abs(vol-self._voltage) < 0.5:
                    self._voltage = vol
            time.sleep(sleepTime)
        
    def set_parameter(self, command, param):
        
        success = self._socket_set.send(("(param-set! '" + str(command) + " " + str(param) + ")" + "\r\n").encode('utf-8'))
        self._socket_set.recv(256)
        
        return success
    
    def read_parameter(self, command):
        # send request
        try_time = 0
        while try_time < 10:
            try_time += 1
            try:
                self._socket_get.send(("(query '" + command + ")" + "\r\n").encode('utf-8'))
            
                # wait and receive answer
                find_str = command[-10:]
                time.sleep(0.01)
                value = self._socket_get.recv(256).decode('utf-8')
                start = value.find(find_str)+len(find_str)+1
                return float(value[start:-1])
            except:
                print('%sth Read Failed' % try_time)
        return (-1)

    def test(self,command):
        self._socket_get.send(("(query '"+command+')'+'\r\n').encode('utf-8')) 
        time.sleep(0.05)
        return(self._socket_get.recv(1024).decode('utf-8')) 

    def get_voltage(self):
        try_time = 0
        while try_time < 5:
            try:
                self._socket_get.send(("(query 'laser1:dl:pc:voltage-set)\r\n").encode('utf-8'))
                time.sleep(0.05)
                vol_str = self._socket_get.recv(256).decode('utf-8')
                vols = rule.findall(vol_str)
                return float(vols[-1])
                # print(vol)
            except Exception as e:
                try_time += 1
                print(e)
                print('Get voltage Failed, Retrying ...')
                time.sleep(0.1)
        return -1
        
    def set_voltage(self, vol):
        flag = False
        while not flag:
            temp = self.set_parameter('laser1:dl:pc:voltage-set', vol)
            flag = (temp==0 or temp>0)
            # print('set_voltage:%s' % flag)
            time.sleep(0.05)

    def get_status(self):
        tryTime = 0
        while True and tryTime < 5:
            try:
                status = self._socket_get2.send(("(query 'laser1:emission)\r\n").encode('utf-8'))
                time.sleep(0.05)
                status = self._socket_get2.recv(1024).decode('utf-8')

                # print(status)
                # print(status[-4:-3])
                return (status[-4:-3]=='t')
                # print('Status:%s, len:%d' % (status, len(status)))
            except:
                tryTime+=1
                time.sleep(0.05)
        return False
    
    def setLock(self,isLock = False):
        print("set Lock:%s" % isLock)
        self._isLock = isLock

    def setDesFre(self,desFre):
        if self._desFre == -1 or abs(self._desFre - float(desFre)) < 0.1:
            self._desFre = float(desFre)
        else:
            print("Please check desFre setting:%s" % desFre)

    def setCurrentFre(self, currentFre):
        self._currentFre = 299792.458/currentFre

    def laserLock(self):
        while True:
            # print("Lock:%s" % self.isLock)
            if self.isLock:
                oldVoltage = self.voltage
                if oldVoltage != -1:
                    print("laser:%s is locking to %s voltage:%s\r" % (self.ip, self._desFre, oldVoltage),end=' ')
                    deltaVoltage = self._pid[0]*(self._desFre - self._currentFre)
                    while (abs(deltaVoltage) > 0.5):
                        print("VoltageGap is too big, please check lock setting")
                        deltaVoltage = deltaVoltage/2
                    newVoltage = oldVoltage + deltaVoltage
                    self.set_voltage(newVoltage)
                    time.sleep(0.1)
                else:
                    print("get voltage failed")
            else:
                time.sleep(0.05)

    def setPid(self,pid):
        self._pid = pid

    @property
    def isLock(self):
        return self._isLock and self.status
    @property
    def status(self):
        return self.get_status()
    
    @property
    def voltage(self):
        return self._voltage
    """ it seem that DLC pro does not support control of physical button
    def on(self):
        self.set_parameter('emission-button-enabled',1)
        time.sleep(0.1)
        if self.get_status():
            print('laser is on')
        else:
            print('enable emission failed')
    
    def off(self):
        self.set_parameter('emission-button-enabled',0)
        time.sleep(0.1)
        if not self.get_status():
            print('laser is off')
        else:
            print('enable emission failed')
    def off(self):
        self.
    """


if __name__ == '__main__':
    ip = "192.168.1.9"
    laser = topticaLaser(ip)
    laser.setDesFre(935.188845)
    laser.setCurrentFre(935.188800)
    laser.setLock(True)
    time.sleep(20)