
#------------START OF OPCODE------------------
REG_REPLY_OPC = 2;
IOT_MODEM_CONFIG = 119;
SAVE_RX_PARAMETERS = 123;
SAVE_TX_PARAMETERS = 124;
SAVE_RX_CATALINA_PARAMETERS = 125;
SAVE_TX_CATALINA_PARAMETERS = 126;
SET_MANUAL_GPS_COORDINATES = 129;
SET_MANUAL_SAT_GPS = 130;
SET_HUB_IOT_TDD_DEF = 131;
SET_MT_IOT_TDD_DEF = 134;
IOT_MODEM_CONFIG_TX = 138;
READ_MODEM_CONFIG_RX = 139;
READ_MODEM_CONFIG_TX = 141;
WRITE_SOFT_REG = 142;
READ_SOFT_REG = 143;
SET_SENSOR_RCV_PORT = 145;
ARM_REGISTER = 153;
MODEM_REGISTER = 39;
MxFE_AXI_REGISTER = 155;
MxFE_SPI_REGISTER = 156;
ADMV4420_FREQ_SET = 157;
MICROBLAZE_REGFILE_SET = 159;
LMX2592_FREQ_SET = 160;
LMX2592_REG_SET_GET = 161;
MAX2112_REG_SET_GET = 162;
ADMV1013_REG_SET_GET = 163;
PHASE_DYNAMIC_SET = 166;
ANTENNA_PWR_CTRL = 167;
ADMV4420_REG_SET_GET = 168;
PIC_REG_SET_GET = 170;
GPS_MSG = 173;
CLK_DAC_SET = 176;
#------------END OF OPCODE------------------

#---------MODEM TYPES-----------------------
MOD_BPSK = 0
MOD_OQPSK = 1
MOD_QPSK = 2
MOD_PI_4_QPSK = 3
#-------------------------------------------

#------------------Constants-------------------

sizeOfYawCoardinates = 400;
y_axisOfYawCoardCenter = 250;
x_axisOfYawCoardCenter = 255;
radiusOfYawCoardinates = sizeOfYawCoardinates / 2;

pitch_x_start = 0;
pitch_x_end = 150;
length_line = 202;
sat_x_start = 255;
sat_y_start = 250;

x_start_pitch = 50;
x_stop_pitch = 50;
y_start_pitch = 452;
y_stop_pitch = 452;
earthRadius = 6371000; ## 6, 371

#** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **

#** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **

MODEM_OSC_FREQUENCY = 40;
MHZ = 1000000.00;
GHZ = 1000000000.00;
PREAMBLE = 0xDEADBEEF;
RX_CATALINA_SAMPLE_RATE = 40.0;

INT_LOW = 0x200;
INT_HIGH = 0x201;
FRAC_LOW = 0x202;
FRAC_MID = 0x203;
FRAC_HIGH = 0x204;
MOD_LOW = 0x208;
MOD_MID = 0x209;
MOD_HIGH = 0x20A;
LMX2594_FRAC_LOW = 0x2B;
LMX2594_FRAC_HIGH = 0x2A;
LMX2594_MODE_LOW = 0x27;
LMX2594_MODE_HIGH = 0x26;
LMX2594_INT_LOW = 0x24;
LMX2594_INT_HIGH = 0x22;
MT_IF_RX = 1400000000; ## 1.4
MT_PLL_OUT = 13000000000; ## 13

#** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **

#** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
DateEn = 0x80000000;
TimeEn = 0x40000000;
Ebn0En = 0x20000000;
RemEbn0En = 0x10000000;
FreqEstEn = 0x08000000;
ModemSyncEn = 0x04000000;
GoodPackEn = 0x02000000;
CrcErrPackEn = 0x01000000;
DropPackEn = 0x00800000;
AppEvenEn = 0x00400000;
BruttoThrEn = 0x00200000;
VoiceThrEn = 0x00100000;
SipThr0En = 0x00080000;
ChatThrEn = 0x00040000;
RegEventEn = 0x00020000;
TrackStatEn = 0x00010000;
IntYawEn = 0x00008000;
IntPitchEn = 0x00004000;
IntRollEn = 0x00002000;
ExtYawEn = 0x00001000;
ExtPitchEn = 0x00000800;
ExtRollEn = 0x00000400;
GpsLatEn = 0x00000200;
GpsLonEn = 0x00000100;
GpsAltEn = 0x00000080;
VerAngEn = 0x00000040;
HorAngEn = 0x00000020;
AntPitchEn = 0x00000010;
AntAzEn = 0x00000008;
rssiAzOffsetEn = 0x00000004;
rssiElOffsetEn = 0x00000002;
northOffsetEn = 0x00000001;
batteryRepEn = 0x100000000;
DEFAULT_COLUMNS = 0x1ffbfffff; ## 0xFFBCE000;
MOBILE_TERMNAL = 1;
HUB = 2;
WRITE = 0;
READ = 1;
SPI_WRITE = 0;
SPI_READ = 1;
SPI_READ_ALL = 2;
SPI_REG_AMOUNT = 65;
#====================END OF CONSTANTS======================
