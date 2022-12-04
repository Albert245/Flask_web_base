import socket 
import DataProcess as DP
import time
Command = {
    'Resp_STK_OK'	                : 0x10,
    'Resp_STK_FAILED'	            : 0x11,
    'Resp_STK_UNKNOWN'	            : 0x12,
    'Resp_STK_NODEVICE'	            : 0x13,
    'Resp_STK_INSYNC'	            : 0x14,
    'Resp_STK_NOSYNC'	            : 0x15,
    'Resp_ADC_CHANNEL_ERROR'	    : 0x16,
    'Resp_ADC_MEASURE_OK'	        : 0x17,
    'Resp_PWM_CHANNEL_ERROR'	    : 0x18,
    'Resp_PWM_ADJUST_OK'	        : 0x19,

    'Sync_CRC_EOP'	                : 0x20,

    'Cmnd_STK_GET_SYNC'	            : 0x30,
    'Cmnd_STK_GET_SIGN_ON'	        : 0x31,
    'Cmnd_STK_RESET'	            : 0x32,
    'Cmnd_STK_SINGLE_CLOCK'	        : 0x33,
    'Cmnd_STK_STORE_PARAMETERS'	    : 0x34,
    'Cmnd_STK_SET_PARAMETER'	    : 0x40,
    'Cmnd_STK_GET_PARAMETER'	    : 0x41,
    'Cmnd_STK_SET_DEVICE'	        : 0x42,
    'Cmnd_STK_GET_DEVICE'	        : 0x43,
    'Cmnd_STK_GET_STATUS'	        : 0x44,
    'Cmnd_STK_SET_DEVICE_EXT'	    : 0x45,
    'Cmnd_STK_ENTER_PROGMODE'	    : 0x50,
    'Cmnd_STK_LEAVE_PROGMODE'	    : 0x51,
    'Cmnd_STK_CHIP_ERASE'	        : 0x52,
    'Cmnd_STK_CHECK_AUTOINC'	    : 0x53,
    'Cmnd_STK_CHECK_DEVICE'	        : 0x54,
    'Cmnd_STK_LOAD_ADDRESS'	        : 0x55,
    'Cmnd_STK_UNIVERSAL'	        : 0x56,
    'Cmnd_STK_PROG_FLASH'	        : 0x60,
    'Cmnd_STK_PROG_DATA'	        : 0x61,
    'Cmnd_STK_PROG_FUSE'	        : 0x62,
    'Cmnd_STK_PROG_LOCK'	        : 0x63,
    'Cmnd_STK_PROG_PAGE'	        : 0x64,
    'Cmnd_STK_PROG_FUSE_EXT'	    : 0x65,
    'Cmnd_STK_READ_FLASH'	        : 0x70,
    'Cmnd_STK_READ_DATA'	        : 0x71,
    'Cmnd_STK_READ_FUSE'	        : 0x72,
    'Cmnd_STK_READ_LOCK'	        : 0x73,
    'Cmnd_STK_READ_PAGE'	        : 0x74,
    'Cmnd_STK_READ_SIGN'	        : 0x75,
    'Cmnd_STK_READ_OSCCAL'	        : 0x76,
    'Cmnd_STK_READ_FUSE_EXT'	    : 0x77,
    'Cmnd_STK_READ_OSCCAL_EXT'	    : 0x78,

    'Parm_STK_HW_VER'	            : 0x80,
    'Parm_STK_SW_MAJOR'	            : 0x81,
    'Parm_STK_SW_MINOR'	            : 0x82,
    'Parm_STK_LEDS'	                : 0x83,
    'Parm_STK_VTARGET'	            : 0x84,
    'Parm_STK_VADJUST'	            : 0x85,
    'Parm_STK_OSC_PSCALE'	        : 0x86,
    'Parm_STK_OSC_CMATCH'	        : 0x87,
    'Parm_STK_RESET_DURATION'	    : 0x88,
    'Parm_STK_SCK_DURATION'	        : 0x89,
    'Parm_STK_BUFSIZEL'	            : 0x90,
    'Parm_STK_BUFSIZEH'	            : 0x91,
    'Parm_STK_DEVICE'	            : 0x92,
    'Parm_STK_PROGMODE'	            : 0x93,
    'Parm_STK_PARAMODE'	            : 0x94,
    'Parm_STK_POLLING'	            : 0x95,
    'Parm_STK_SELFTIMED'	        : 0x96,

    'Stat_STK_INSYNC'	            : 0x01,
    'Stat_STK_PROGMODE'	            : 0x02,
    'Stat_STK_STANDALONE'	        : 0x04,
    'Stat_STK_RESET'	            : 0x08,
    'Stat_STK_PROGRAM'	            : 0x10,
    'Stat_STK_LEDG'	                : 0x20,
    'Stat_STK_LEDR'	                : 0x40,
    'Stat_STK_LEDBLINK'	            : 0x80,
}
AVR_signature = [
    [0x1e, 0x90, 0x07],
    [0x1e, 0x91, 0x0a],
    [0x1e, 0x92, 0x0a],
    [0x1e, 0x93, 0x07],
    [0x1e, 0x94, 0x06],
    [0x1e, 0x95, 0x02],
    [0x1e, 0x95, 0x0f],
    [0x1e, 0x95, 0x14],
    [0x1e, 0x96, 0x02],
    [0x1e, 0x96, 0x09],
    [0x1e, 0x97, 0x02],
    [0x1e, 0x97, 0x03],
    [0x1e, 0x98, 0x01]
]

AVR_model = [
    'ATtiny13',
    'ATtiny2313',
    'ATmega48P',
    'ATmega8',
    'ATmega168',
    'ATmega32',
    'ATmega328P',
    'ATmega328-PU',
    'ATmega64',
    'ATmega644',
    'ATmega128',
    'ATmega1280',
    'ATmega2560'
]



s = socket.socket()


def AVR_ISP(ip,port,hex_data):
    logs = []
    addr = [0x00,0x00]
    add_count = len(hex_data)
    start_prog(ip,port)
    getSync()
    setProg()
    setProgEx()
    enterProgMode()
    getSignature()
    readPage(add_count)
    end_prog()
    pass


def start_prog(ip,port):
    s.connect((ip,port))

def end_prog():
    s.close()

def sendByte(list,logs):
    logs.append(list)
    data = bytes(list)
    s.send(data)
    time.sleep(0.1)
    ret = s.recv(1024)
    logs.append(ret)
    return list(ret)

# list type hex in --> send to programmer return (True: 1, False: error log)
def excCmd(list,resp,log):
    ret = sendByte(list,log)                #list of int
    check = 1
    for i in resp:
        if i not in ret:
            check = 0
    if check == 0:
        err_hex = ret
        err_read = []
        for i in err_hex:
            for name,value in Command.items():
                if i == value:
                    err_read.append(name)
        return log.append(err_read)
    return 1

# check if in sync
def getSync(log):
    return excCmd([0x30, 0x20],[0x14, 0x10],log)

# set Device
def setProg():
    cmd = [0x42, 0x86, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x03, 0xff, 0xff, 0xff, 0xff, 0x00, 0x80, 0x04, 0x00, 0x00, 0x00, 0x80, 0x00, 0x20]
    return sendByte(cmd)

# set Device extend
def setProgEx():
    cmd = [0x45, 0x05, 0x04, 0xd7, 0xc2, 0x00, 0x20]
    return sendByte(cmd)

#Enter Program mode
def enterProgMode():
    cmd = [0x50, 0x20]
    return sendByte(cmd)

#Get signature
def getSignature():
    cmd = [0x75, 0x20]
    sign = sendByte(cmd)
    signature = sign[1:-1:1]
    for s in AVR_signature:
        if s == signature:
            return AVR_model[s]
    return 'Unkown model (signature {}), please check again'.format(signature)

# Leave Program mode
def exProgMode():
    cmd = [0x51, 0x20]
    return sendByte(cmd)


def IncreaseAddress(addr):
    addr[1] += 0x40
    if addr[1]>255:
        addr[1] = addr[1] % 255
        addr[0] += 0x1
    return addr


def loadAddress(addr):
    head = [0x55]
    tail = [0x20]
    load_addr = head + addr + tail
    return sendByte(load_addr)

def compare(page,block):
    page_read = page[1:-1:1]
    for i in range(len(page_read)):
        if page_read[i] != block[i]:
            return 'Verification Failure'
    return 1

def flashPage(data):
    head = [0x64, 0x00, 0x80,0x46]
    tail = [0x20]
    flash_page = head + data + tail
    return sendByte(flash_page)

# Read page on microchip
def readPage(count):
    read_addr = [0x00,0x00]
    cmd = [0x74, 0x00, 0x80, 0x46, 0x20]
    read_page =[]
    for i in range(count):
        loadAddress(read_addr)
        read_page.append(sendByte(cmd))
    return read_page