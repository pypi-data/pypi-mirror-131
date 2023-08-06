from emBRICK.modbus_rtu import local
from emBRICK.modbus_rtu import slave
from emBRICK.modbus_rtu import bB_update
from emBRICK.modbus_rtu import bB

import threading
import math
import numpy as np
lock = threading.Lock()

class CAE_G8Di8Do:
    def __init__(self):
        self.node = 1
        self.id = 2181
        self.brick_no = ''
        # Data Lenght
        self.data_length_miso = ''
        self.data_length_mosi = ''
        # Offset
        self.offset_miso = ''
        self.offset_mosi = ''


    def findBrick(self):
        for i in range(local.info[self.node]['number of connected bricks']):
            if slave.id[self.node, i] == self.id:
                self.brick_no = i + 1
                self.data_length_miso = slave.data_length_miso[self.node, i]
                self.data_length_mosi = slave.data_length_mosi[self.node, i]
                self.offset_miso = slave.offset_miso[self.node, i]
                self.offset_mosi = slave.offset_miso[self.node, i]

    def DI(self, bit_pos):
        lock.acquire()
        byte = bB_update.updated[self.node][self.offset_miso + 1]
        lock.release()
        return 1 if (byte & (1 << bit_pos)) else 0

    def DO(self, bit_pos, value):
        lock.acquire()
        if ((bB.put[self.node][self.offset_mosi] >> bit_pos) & 1) != value:
            if value:
                bB.put[self.node][self.offset_mosi] += (1 << bit_pos)
            else:
                bB.put[self.node][self.offset_mosi] -= (1 << bit_pos)
        lock.release()

G8Di8Do = CAE_G8Di8Do()

class CAE_B3U4I:
    def __init__(self):
        self.node = 1
        self.id = [4602, 4603]
        self.brick_id = ''
        self.brick_no = ''
        # Data Lenght
        self.data_length_miso = ''
        self.data_length_mosi = ''
        # Offset
        self.offset_miso = ''
        self.offset_mosi = ''
        # Current, Voltage, Power Correction Values 4-602
        self.cur_val_602 = 0.1873508544
        self.vol_val_602 = 0.01361541109
        self.pow_val_602 = 334.3461753
        # Current, Voltage, Power Correction Values 4-603
        self.cur_val_603 = 0.005026486336
        self.vol_val_603 = 0.01361541109
        self.pow_val_603 = 8.970263239
        #
        self.result_cnt = ''
        self.power = [0] * 3
        self.power_w = []#[0] * 3
        self.phase = [0] * 3
        self.current = [0] * 3
        self.current_a = [0] * 3
        self.voltage = [0] * 3
        self.voltage_v = [0] * 3

    def findBrick(self):
        for i in range(local.info[self.node]['number of connected bricks']):
            if slave.id[self.node, i] in self.id:
                self.brick_id = slave.id[self.node, i]
                self.brick_no = i + 1
                self.data_length_miso = slave.data_length_miso[self.node, i]
                self.data_length_mosi = slave.data_length_mosi[self.node, i]
                self.offset_miso = slave.offset_miso[self.node, i]
                self.offset_mosi = slave.offset_miso[self.node, i]

    def phase_cor(self, winkel_l1, winkel_l2, winkel_l3):
        # Page auf 1 Setzen
        bB.put[self.node][self.offset_mosi] = 1
        # CommandCounter auslesen
        commandcounter = bB_update.updated[self.node][self.offset_miso + 2]

        ### Phase Correction Calculation ###
        phi = winkel_l1 / 180 * math.pi
        omega = 2 * math.pi * (50 / 8000)
        phase_correction_val = ((math.sin(phi - omega) + math.sin(omega)) / (math.sin(2 * omega - phi))) * (2 ** 27)
        phase_val = math.ceil(phase_correction_val)
        bB.put[self.node][self.offset_mosi + 4] = (phase_val >> 24) & 0xFF
        bB.put[self.node][self.offset_mosi + 5] = (phase_val >> 16) & 0xFF
        bB.put[self.node][self.offset_mosi + 6] = (phase_val >> 8) & 0xFF
        bB.put[self.node][self.offset_mosi + 7] = phase_val & 0xFF

        phi = winkel_l2 / 180 * math.pi
        phase_correction_val = ((math.sin(phi - omega) + math.sin(omega)) / (math.sin(2 * omega - phi))) * (2 ** 27)
        phase_val = math.ceil(phase_correction_val)
        bB.put[self.node][self.offset_mosi + 8] = (phase_val >> 24) & 0xFF
        bB.put[self.node][self.offset_mosi + 9] = (phase_val >> 16) & 0xFF
        bB.put[self.node][self.offset_mosi + 10] = (phase_val >> 8) & 0xFF
        bB.put[self.node][self.offset_mosi + 11] = phase_val & 0xFF

        phi = winkel_l3 / 180 * math.pi
        phase_correction_val = ((math.sin(phi - omega) + math.sin(omega)) / (math.sin(2 * omega - phi))) * (2 ** 27)
        phase_val = math.ceil(phase_correction_val)
        bB.put[self.node][self.offset_mosi + 12] = (phase_val >> 24) & 0xFF
        bB.put[self.node][self.offset_mosi + 13] = (phase_val >> 16) & 0xFF
        bB.put[self.node][self.offset_mosi + 14] = (phase_val >> 8) & 0xFF
        bB.put[self.node][self.offset_mosi + 15] = phase_val & 0xFF
        # Trigger To Sub hochzählen um die Einstellung zu speichern
        bB.put[self.node][self.offset_mosi + 1] = commandcounter + 1

    def average_depth(self, messungen):
        # Page auf 4 Setzen
        bB.put[self.node][self.offset_mosi] = 4
        # CommandCounter auslesen
        commandcounter = bB_update.updated[self.node][self.offset_miso + 2]
        # Anzahl der Messungen die gespeichter werden
        bB.put[self.node][self.offset_mosi + 11] = messungen
        # Trigger To Sub hochzählen um die Einstellung zu speichern
        bB.put[self.node][self.offset_mosi + 1] = commandcounter + 1

    def resultCnt(self):
        page = bB_update.updated[self.node][self.offset_miso + 1]
        if not page == 1:
            bB.put[self.node][self.offset_mosi] = 1
            # CommandCounter auslesen
            commandcounter = bB_update.updated[self.node][self.offset_miso + 2]
            # Trigger To Sub hochzählen um die Einstellung zu speichern
            bB.put[self.node][self.offset_mosi + 1] = commandcounter + 1
        return bB_update.updated[self.node][self.offset_miso + 3]


    def readPower(self,):
        page = bB_update.updated[self.node][self.offset_miso + 1]
        if not page == 1:
            bB.put[self.node][self.offset_mosi] = 1
            # CommandCounter auslesen
            commandcounter = bB_update.updated[self.node][self.offset_miso + 2]
            # Trigger To Sub hochzählen um die Einstellung zu speichern
            bB.put[self.node][self.offset_mosi + 1] = commandcounter + 1

        self.power[0] = (bB_update.updated[self.node][self.offset_miso + 5] << 8) + bB_update.updated[self.node][
            self.offset_miso + 6]
        self.power[1] = (bB_update.updated[self.node][self.offset_miso + 7] << 8) + bB_update.updated[self.node][
            self.offset_miso + 8]
        self.power[2] = (bB_update.updated[self.node][self.offset_miso + 9] << 8) + bB_update.updated[self.node][
            self.offset_miso + 10]
        self.power = [i * 0 for i in self.power if (i == 0 or i == 0xFFFF)]
        if self.brick_id == 4602:
            self.power_w = [i * self.pow_val_602 for i in np.int16(self.power)]
        else:
            self.power_w = [i * self.pow_val_603 for i in np.int16(self.power) ]

        return self.power_w

    def readPhase(self,):
        page = bB_update.updated[self.node][self.offset_miso + 1]
        if not page == 1:
            bB.put[self.node][self.offset_mosi] = 1
            # CommandCounter auslesen
            commandcounter = bB_update.updated[self.node][self.offset_miso + 2]
            # Trigger To Sub hochzählen um die Einstellung zu speichern
            bB.put[self.node][self.offset_mosi + 1] = commandcounter + 1

        self.phase[0] = (bB_update.updated[self.node][self.offset_miso + 11] << 8) + bB_update.updated[self.node][
            self.offset_miso + 12]
        self.phase[1] = (bB_update.updated[self.node][self.offset_miso + 13] << 8) + bB_update.updated[self.node][
            self.offset_miso + 14]
        self.phase[2] = (bB_update.updated[self.node][self.offset_miso + 15] << 8) + bB_update.updated[self.node][
            self.offset_miso + 16]
        self.phase = [i /24800 for i in self.phase]
        return self.phase

    def readCurrent(self):
        page = bB_update.updated[self.node][self.offset_miso + 1]
        if not page == 1:
            bB.put[self.node][self.offset_mosi] = 1
            # CommandCounter auslesen
            commandcounter = bB_update.updated[self.node][self.offset_miso + 2]
            # Trigger To Sub hochzählen um die Einstellung zu speichern
            bB.put[self.node][self.offset_mosi + 1] = commandcounter + 1
        self.current[0] = (bB_update.updated[self.node][self.offset_miso + 17] << 8) + bB_update.updated[self.node][
            self.offset_miso + 18]
        self.current[1] = (bB_update.updated[self.node][self.offset_miso + 19] << 8) + bB_update.updated[self.node][
            self.offset_miso + 20]
        self.current[2] = (bB_update.updated[self.node][self.offset_miso + 21] << 8) + bB_update.updated[self.node][
            self.offset_miso + 22]
        print("Current: ", self.current)
        if self.brick_id == 4602:
            self.current_a = [i * self.cur_val_602 for i in self.current]
        else:
            self.current_a = [i * self.cur_val for i in self.current]
        return self.current_a

    def readVoltage(self):
        page = bB_update.updated[self.node][self.offset_miso + 1]
        if not page == 1:
            bB.put[self.node][self.offset_mosi] = 1
            # CommandCounter auslesen
            commandcounter = bB_update.updated[self.node][self.offset_miso + 2]
            # Trigger To Sub hochzählen um die Einstellung zu speichern
            bB.put[self.node][self.offset_mosi + 1] = commandcounter + 1
        self.voltage[0] = (bB_update.updated[self.node][self.offset_miso + 23] << 8) + bB_update.updated[self.node][
            self.offset_miso + 24]
        self.voltage[1] = (bB_update.updated[self.node][self.offset_miso + 25] << 8) + bB_update.updated[self.node][
            self.offset_miso + 26]
        self.voltage[2] = (bB_update.updated[self.node][self.offset_miso + 27] << 8) + bB_update.updated[self.node][
            self.offset_miso + 28]
        if self.brick_id == 4602:
            self.voltage_v = [i * self.vol_val_602 for i in self.voltage]
        else:
            self.voltage_v = [i * self.vol_val_603 for i in self.voltage]
        return self.voltage_v

B3U4I = CAE_B3U4I()