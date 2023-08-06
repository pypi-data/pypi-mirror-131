#!/usr/bin/evn python3
# Import Threading Module
import threading
import time
import math
from datetime import datetime
# Import pymodbus for the Modbus RTU Module
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
lock = threading.Lock()
filename = 'error.txt'


def splitBytes(list16bit):
    # Function to split a list with 16 bit elements into 8 bit element list
    list8bit = []
    for value in list16bit:
        a = (value >> 8) & 0xff
        b = value & 0xff
        list8bit.append(a)
        list8bit.append(b)
    return list8bit


def addBytes(list8bit):
    list16bit = []
    if not len(list8bit) // 2:
        list8bit.append(0)
    for num in range(len(list8bit)):
        if not num % 2:
            byte0 = list8bit[num] << 8
        else:
            byte1 = list8bit[num]
            byte = byte0 + byte1
            list16bit.append(byte)
    return list16bit


class local_master:
    # Sorting the information about the local master
    def __init__(self):
        self.info = {}

    def data(self):
        for id in connect.unit_id:
            self.info[id] = {'number of connected bricks': bB_update.local_data[id][0],
                         'status of the local-master': bB_update.local_data[id][1],
                         'component ID of the local-master': ((bB_update.local_data[id][2] << 8) + bB_update.local_data[id][3]),
                         'remote bus protocol version': bB_update.local_data[id][4],
                         'software version of local-master': bB_update.local_data[id][5],
                         'Local Master manufacturer ID': bB_update.local_data[id][6],
                         'Reserved1': bB_update.local_data[id][7],
                         'Reserved2': bB_update.local_data[id][8]}

local = local_master()

class slave_module:
    # Sorting the Information about the emBricks
    def __init__(self):
        self.status = {}
        self.data_length_mosi = {}
        self.data_length_miso = {}
        self.pro_ver = {}
        self.hard_rev = {}
        self.id = {}
        self.manu_id = {}
        self.offset_mosi = {}
        self.offset_miso = {}
    def info(self):
        for id in connect.unit_id:
            for i in range(local.info[id]['number of connected bricks']):
                self.status[id, i] = bB_update.local_data[id][9+(i*11)+0]
                self.data_length_mosi[id, i] = bB_update.local_data[id][9+(i*11)+1]
                self.data_length_miso[id, i] = bB_update.local_data[id][9+(i*11)+2]
                self.pro_ver[id, i] = bB_update.local_data[id][9+(i*11)+3]
                self.hard_rev[id, i] = bB_update.local_data[id][9+(i*11)+4]
                self.id[id, i] = (bB_update.local_data[id][9+(i*11)+5] << 8) + bB_update.local_data[id][9+(i*11)+6]
                self.manu_id[id, i] = (bB_update.local_data[id][9+(i*11)+7] << 8) + bB_update.local_data[id][9+(i*11)+8]
                self.offset_mosi[id, i] = bB_update.local_data[id][9+(i*11)+9]
                self.offset_miso[id, i] = bB_update.local_data[id][9+(i*11)+10]
slave = slave_module()

class connection:
    def __init__(self):
        self.port = ''
        self.baudrate = 460800
        self.number = 0
        self.slave_address = []
        self.unit_id = []

        self.node = ''
        self.timeout = 0.1
        self.updateRate = 0.005


    def start(self):
        print("---------------------------------------------------\n")
        print("emBRICK(R), Starterkit Modbus RTU Python\n")
        print("(c) 2021 by IMACS GmbH \n")
        print("---------------------------------------------------\n")
        error = open(filename, 'wt')

        # Connecting to the LWC's on the given Slave Adress
        self.node = ModbusClient(method='rtu', port=self.port, timeout= self.timeout, baudrate= self.baudrate)
        error.write(f'Error Log\nCommunication over Modbus RTU with Python\
         Baudrate: {self.baudrate}, \tPort: {self.port}, \tTimeout: {self.timeout}\n\n')

        if self.node.is_socket_open() == True:
            self.node.close()
        connected = self.node.connect()
        if not connected:
            error.write(f'Connection with Port {self.port} failed!')
            error.close()
            exit()
        error.close
        # Initialize the Functions to start the Program
        bB_update.getLWCsInfo()
        local.data()
        slave.info()
        bB_update.update_first()
        bB.createEmptyList()
        t1 = threading.Thread(target=bB_update.update)

        t1.start()
        init()
        #time.sleep(1)
        #t1.join()

connect = connection()


class brickBus_communication:
    #
    def __init__(self):
        self.local_data = {}
        self.updated = {}
        self.updates = {}

    def getLWCsInfo(self):

        for id in connect.unit_id:
            # Reads in the Init Data in the address range 1000h ... 107 ch
            responce = connect.node.read_input_registers(4096,104, unit = id)
            if not responce.isError():
                data_16byte = responce.registers
                self.local_data[id] = splitBytes(data_16byte)
            else:
                error = open(filename, 'at')
                error.write(f'{datetime.now()}\tConnection to the Coupling-Master with Modbus Address {id} failed!\n')
                error.close()

    def update_first(self, ):
        # Update the emBricks in the individual updaterate
        for id in connect.unit_id:
            responce = connect.node.read_input_registers(0, 120, unit=id)
            time.sleep(0.005)
            if not responce.isError():
                self.updates[id] = responce.registers
            else:
                error = open(filename, 'at')
                error.write(f'{datetime.now()}\tChecksum Error\n')
                error.close()
            if self.updates[id] != 0:
                self.updated[id] = splitBytes(self.updates[id])
        #bB.createEmptyList()

    def update(self):
        # Update the emBricks in the individual updaterate
        while True:
            if not connect.node.is_socket_open() == True:
                connect.node.connect()
            for id in connect.unit_id:
                if not bB.put[id] == []:
                    with lock:
                        bB.set[id] = addBytes(bB.put[id])
                arguments = {
                    'read_address': 0,
                    'read_count': bB.buffer_length[id],
                    'write_address': 0,
                    'write_registers': bB.set[id],
                }

                responce = connect.node.readwrite_registers(unit=id, **arguments)
                if not responce.isError():
                    self.updates[id] = responce.registers
                else:
                    error = open(filename, 'at')
                    error.write(f'{datetime.now()}\tChecksum Error\n')
                    error.close()

                if self.updates[id] != 0:
                    lock.acquire()
                    self.updated[id] = splitBytes(self.updates[id])
                    lock.release()

bB_update = brickBus_communication()



class functions:
    # Implement the 6 Main Function to Control the emBricks
    def __init__(self, ):
        self.gS = 0
        self.gByte = 0
        self.gBit = 0
        self.pShort = []
        self.pByte = []
        self.pBit = []
        self.put = {}
        self.set = {}
        self.buffer_length = {}
        self.printed_pBit = False
        self.printed_pB = False
        self.printed_pS = False

    def createEmptyList(self):
        for id in connect.unit_id:
            output = 0
            input = 0
            for j in range(local.info[id]['number of connected bricks']):
                output += slave.data_length_mosi[id, j]
                input += slave.data_length_miso[id, j]
            input = math.ceil(input / 2)
            self.put[id] = [0] * output
            self.buffer_length[id] = input

    def getShort(self, node, module, bytePos):
        # Return the value in Size of 2 bytes(16bit) of the desired Byte Position
        if  ((node,module-1) in slave.offset_miso):
            lock.acquire()
            byte1 = (bB_update.updated[node][slave.offset_miso[node, module-1] + bytePos + 1]) << 8
            byte2 = bB_update.updated[node][slave.offset_miso[node, module-1] + bytePos + 2]
            lock.release()
            self.gS = byte1 + byte2
        else:
            self.gS = None
        return self.gS

    def getByte(self, node, module, bytePos):
        # Return the value in Size of 1 byte(8bit) of the desired Byte Position
        if  ((node,module-1) in slave.offset_miso):
            #print(bB_update.updated)
            byte = slave.offset_miso[node, module-1] + bytePos + 1
            lock.acquire()
            self.gByte = bB_update.updated[node][byte]
            lock.release()
        else:
            self.gByte = None
        return self.gByte

    def getBit(self, node, module, bytePos, bitPos):
        # Return the value in Size of a Bit of the desired Byte -> Bit Position
        if  ((node,module-1) in slave.offset_miso):
            lock.acquire()
            byte = bB_update.updated[node][slave.offset_miso[node, module-1] + bytePos + 1]
            lock.release()
            self.gBit = 1 if (byte & (1 << bitPos)) else 0
        else:
            self.gBit = None
        return self.gBit


    def putShort(self, node, module, bytePos, value):
        # Put the desired value in Size 2 bytes to the desired Byte Position
        try:
            output = slave.offset_mosi[node, module - 1] + bytePos
            output1 = (value >> 8) & 0xFF
            output2 = value & 0xFF
            self.pShort = [output1] + [output2]
            self.put[node][output] = self.pShort[0]
            self.put[node][(output + 1)] = self.pShort[1]
        except:
            if self.printed_pS == False:
                error = open(filename, 'at')
                error.write(f'Node: {node}, Module: {module}, BytePos: {bytePos} not found!\n')
                error.close()
                self.printed_pS = True


    def putByte(self, node, module, bytePos, value):
        # Put the desired value in Size 1 bytes to the desired Byte Position

        try:
            output = slave.offset_mosi[node, module - 1] + bytePos
            self.pByte = value
            self.put[node][output] = self.pByte
        except:
            if self.printed_pB == False:
                error = open(filename, 'at')
                error.write(f'Node: {node}, Module: {module}, BytePos: {bytePos} not found!\n')
                error.close()
                self.printed_pB = True

    def putBit(self, node, module, bytePos, bitPos, value):
        # Put the desired value in Size 1 bit to the desired Byte -> Bit Position
        try:
            output = slave.offset_mosi[node, module - 1] + bytePos
            self.pBit = 1 << bitPos
            val0 = 2 ** (bitPos + 1) - 1
            val = ((self.put[node][output]) & val0) >> bitPos
            if value:
                if not val:
                    self.put[node][output] += self.pBit
            else:
                if val >= 1:
                    self.put[node][output] -= self.pBit
        except:
            if self.printed_pBit == False:
                error = open(filename, 'at')
                error.write(f'Node: {node}, Module: {module}, BytePos: {bytePos}, BitPos: {bitPos} not found!\n')
                error.close()
                self.printed_pBit = True


bB = functions()


def init():
    #Prints the Information about the Local Master and the connected Bricks to him
    for id in connect.unit_id:
        print(f'\nNode {id} is connected with the local master: '
              f'{local.info[id]["component ID of the local-master"] // 1000}-{local.info[id]["component ID of the local-master"] % 1000} '
              f'with Software Version: {local.info[id]["software version of local-master"]}')
        print(f'With following modules:')
        for i in range(local.info[id]['number of connected bricks']):
            print(f'{i + 1}: {slave.id[id, i] // 1000}-{slave.id[id, i] % 1000} with Hardware Revision: {slave.hard_rev[id, i]}')
    print("To abort the program please press STRG + C\n\n")
