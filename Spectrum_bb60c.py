from bbdevice.bb_api import *
import pyvisa
import time
import matplotlib.pyplot as plt
import seaborn as sns;
sns.set() # styling


class My_bb60c_sa:
    def __init__(self):
        # Open device
        self.handle = bb_open_device()["handle"]
        if bb_get_serial_number(self.handle)['serial'] == 0:
            raise Exception("Sorry, no spectrum is connected")
        self.sweep_size = 0
        self.start_freq = 0
        self.bin_size = 0

    def configure_device(self, center_freq=1.0e9, span=100.0e6, ref_level=-30.0, rbw=10.0e3, vbw=10.0e3, sweep_time=0.001):
        # Configure device
        bb_configure_center_span(self.handle, center_freq, span)
        bb_configure_level(self.handle, ref_level, BB_AUTO_ATTEN)
        bb_configure_gain(self.handle, BB_AUTO_GAIN)
        bb_configure_sweep_coupling(self.handle, rbw, vbw, sweep_time, BB_RBW_SHAPE_FLATTOP, BB_NO_SPUR_REJECT)
        bb_configure_acquisition(self.handle, BB_MIN_AND_MAX, BB_LOG_SCALE)
        bb_configure_proc_units(self.handle, BB_POWER)

    def change_ref_lvl(self, ref_level=-30.0):
        bb_configure_level(self.handle, ref_level, BB_AUTO_ATTEN)

    def change_freq_span_hz(self, center_freq, span):
        bb_configure_center_span(self.handle, center_freq, span)

    def change_ref_level(self, ref_level):
        bb_configure_level(self.handle, ref_level, BB_AUTO_ATTEN)

    def change_rbw_vbw_span_sweept(self, rbw=10.0e3, vbw=10.0e3, sweep_time=0.001):
        bb_configure_sweep_coupling(self.handle, rbw, vbw, sweep_time, BB_RBW_SHAPE_FLATTOP, BB_NO_SPUR_REJECT)

    def get_trace_info(self):
        # Initialize
        bb_initiate(self.handle, 0, 0) # BB_SWEEPING
        query = bb_query_trace_info(self.handle)
        self.sweep_size = query["sweep_size"]
        self.start_freq = query["start_freq"]
        self.bin_size = query["bin_size"]

    def get_sweep(self):
        self.sweep_max = bb_fetch_trace_32f(self.handle, self.sweep_size)["max"]
        return self.sweep_max

    def get_freqs(self):
        freqs = [self.start_freq + i * self.bin_size for i in range(self.sweep_size)]
        i = self.sweep_max.argmax()
        print(f"freq is :{freqs[i]}")
        return freqs


class bb60c_scpi:

    def get_peak_search(self, freq=3050000000.0, span=10000000.0):
        self.check_spike()
        result = []
        rm = pyvisa.ResourceManager()
        BB60C_1 = rm.open_resource('TCPIP0::localhost::5025::SOCKET', write_termination='\n')
        BB60C_1.read_termination = '\n'
#        time.sleep(3)
        BB60C_1.write(f':FREQuency:CENTer {freq}')
        BB60C_1.write(f':FREQuency:SPAN {span}')
        BB60C_1.write(f':CALCulate:MARKer:X {freq}')
        time.sleep(1)
        BB60C_1.write(':CALCulate:MARKer:MAXimum')
        temp_values = BB60C_1.query_ascii_values(':CALCulate:MARKer:X?')
        freq_max = temp_values[0]
        result.append(freq_max)
        print("5 ",freq_max)
        temp_values = BB60C_1.query_ascii_values(':CALCulate:MARKer:Y?')
        real_max = temp_values[0]
        print("6 ",real_max)
        result.append(real_max)
        BB60C_1.close()
        rm.close()
        #self.close_spike()
        return result

    def get_power_in_freq(self, freq=3000000000.0, span=20000000.0):
        self.check_spike()
        result = []
        rm = pyvisa.ResourceManager()
        BB60C_1 = rm.open_resource('TCPIP0::localhost::5025::SOCKET', write_termination='\n')
        BB60C_1.read_termination = '\n'
        BB60C_1.write(f':FREQuency:CENTer {freq}')
        BB60C_1.write(f':FREQuency:SPAN {span}')
        BB60C_1.write(f':CALCulate:MARKer:X {freq}')
        time.sleep(1)
        temp_values = BB60C_1.query_ascii_values(':CALCulate:MARKer:X?')
        freq = temp_values[0]
        result.append(freq)
        temp_values = BB60C_1.query_ascii_values(':CALCulate:MARKer:Y?')
        real = temp_values[0]
        result.append(real)
        BB60C_1.close()
        rm.close()
        self.close_spike()
        return result

    def oc_bw(self, freq=3000000000.0, span=20000000.0):
        '''gets freq and span
        returns : center freq, ocbw power, occupied bw'''
        self.check_spike()
        result = []
        rm = pyvisa.ResourceManager()
        BB60C_1 = rm.open_resource('TCPIP0::localhost::5025::SOCKET', write_termination='\n')
        BB60C_1.read_termination = '\n'
        BB60C_1.write(f':FREQuency:CENTer {freq}')
        BB60C_1.write(f':FREQuency:SPAN {span}')
        BB60C_1.write(f':OBWidth:STATe ON')
        BB60C_1.write(f':OBWidth:PERC 99')
        time.sleep(1)
        temp_values = BB60C_1.query_ascii_values(':OBWidth:CENTer?')
        freq_center = temp_values[0]
        result.append(freq_center)
        temp_values = BB60C_1.query_ascii_values(':OBWidth:POWer?')
        power_ocbw = temp_values[0]
        result.append(power_ocbw)
        temp_values = BB60C_1.query_ascii_values(':OBWidth:OBWidth?')
        ocbw = temp_values[0]
        result.append(ocbw)
        BB60C_1.close()
        rm.close()
        self.close_spike()
        print(result)
        return result

    def get_evm(self, freq_ghz=3, RfLev_dbm=-20, sym_rate_mhz=2.24):
        '''
        This func returns RMS EVM avg%(1), Freq Err avg as Hz(9), Rf Pwr avg as dBm(12)
        SNR avg as dB(13)
        '''
        result = ''
        self.close_spike()
        self.check_spike()
        rm = pyvisa.ResourceManager()
        BB60C = rm.open_resource('TCPIP0::localhost::5025::SOCKET', write_termination='\n')
        BB60C.write("INSTRUMENT:SELECT DDEMOD")
        BB60C.write("INIT:CONT ON")
        BB60C.write(f"DDEMOD:FREQ:CENT {freq_ghz}GHz")
        BB60C.write(f"DDEMOD:POW:RF:RLEV {RfLev_dbm}DBM")
        BB60C.write(f"DDEMOD:SRAT {sym_rate_mhz}MHz")
        BB60C.write("DDEMOD:MOD QPSK")
        BB60C.write("DDEMOD:RLEN 64")
        time.sleep(3)
        BB60C.write("INIT:CONT OFF")
        # BB60C.query_ascii_values(':FORMat:TRACe:DATA?', converter='s')
        time.sleep(3)
        old_timeotut = BB60C.timeout
        # print(BB60C.query(":SYSTem:DEVice:ACTive?"))
        BB60C.timeout = 6000
        BB60C.write(":FETCH:DDEMOD? 1")
        result1 = BB60C.read_bytes(6)
        result += result1.decode()
        BB60C.write(":FETCH:DDEMOD? 9")
        result1 = BB60C.read_bytes(10)
        result += result1.decode()
        BB60C.write(":FETCH:DDEMOD? 12")
        result2 = BB60C.read_bytes(6)
        result += result2.decode()
        BB60C.write(":FETCH:DDEMOD? 13")
        result3 = BB60C.read_bytes(6)
        evm_sum = result1.decode()
        result += result3.decode()

        BB60C.timeout = old_timeotut
        BB60C.read_termination = '\n'
        BB60C.close()
        rm.close()
        self.close_spike()
        return result

    def check_spike(self):
        import os
        import psutil
        import time

        if not ("Spike.exe" in (p.name() for p in psutil.process_iter())):
            os.startfile("C:/Program Files/Signal Hound/Spike/Spike.exe")
            time.sleep(5)

    def close_spike(self):
        import os
        import psutil
        import time

        if "vmware.exe" in (p.name() for p in psutil.process_iter()):
            os.system("taskkill /f /im vmware.exe")
            time.sleep(1)

        if "Spike.exe" in (p.name() for p in psutil.process_iter()):
            os.system("taskkill /f /im Spike.exe")
            time.sleep(1)

    def close_device(self):
        ''' Device no longer needed, close it'''
        bb_close_device(self.handle)


def testing_the_bb60c():
    mybb60csa = My_bb60c_sa()
    mybb60csa.configure_device()
    mybb60csa.get_trace_info()
    print(mybb60csa.get_sweep())
    print("===================")
    print(mybb60csa.get_freqs())
    print("===================")
    print(mybb60csa.get_sweep().max())
    mybb60csa.close_device()
    print('Done')


def testing_demod_with_scpi():
    mybb60csa = bb60c_scpi()
    mybb60csa.get_evm()


def testing_the_timeout():
    rm = pyvisa.ResourceManager()
    BB60C = rm.open_resource('TCPIP0::localhost::5025::SOCKET', write_termination='\n')
    print(BB60C.timeout)
    BB60C.timeout = 5000
    print(BB60C.timeout)
    print(BB60C.read_termination)
    BB60C.write('*IDN?')
    print(BB60C.read_bytes(30))

def test_peak_search():
    mybb60csa = bb60c_scpi()
    print(mybb60csa.get_peak_search(3.0*1e9, 5.0*1e6))

def check_spike():
    import os
    import psutil
    import time
    #import pygetwindow as gw

    if not ("Spike.exe" in (p.name() for p in psutil.process_iter())):
        os.startfile("C:/Program Files/Signal Hound/Spike/Spike.exe")
        time.sleep(4)
        #spike = gw.getWindowsWithTitle('Spike')
        #print(skipe)
        #for item in spike:
        #    item.minimize()


def close_spike():
    import os
    import psutil
    import time

    if "vmware.exe" in (p.name() for p in psutil.process_iter()):
        os.system("taskkill /f /im vmware.exe")
        time.sleep(1)

    if "Spike.exe" in (p.name() for p in psutil.process_iter()):
        os.system("taskkill /f /im Spike.exe")
        time.sleep(1)


if __name__ == "__main__":
    try:
        # testing_the_bb60c()
        # testing_demod_with_scpi()
        # testing_the_timeout()
        # test_peak_search()
        mybb60csa = bb60c_scpi()
        #print(mybb60csa.get_evm().split("\n"))
        mybb60csa.check_spike()
        time.sleep(5)
        mybb60csa.close_spike()

    except ValueError:
        print(ValueError)
    print('Done')
