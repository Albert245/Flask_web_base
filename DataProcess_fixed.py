# ====================================[  Library  ]=======================================


def extractData(start, stop, raw_data):
    data = []
    recent_addr = int(raw_data[0][3:7], 16)
    bytes_count = int(raw_data[0][1:3], 16)
    for i in range(len(raw_data)):
        a = raw_data[i]
        if a[8] == '0':
            current_addr = int(a[3:7], 16)
            if recent_addr == current_addr:
                fill_count = 0
            else:
                fill_count = current_addr - recent_addr - bytes_count
            print('address {} to {} fill {} times'.format(recent_addr, current_addr, fill_count))
            data.append('FF'*fill_count)
            data.append(a[start:stop])
            recent_addr = current_addr
            bytes_count = int(a[1:3], 16)

    while ("" in data):
        data.remove("")
    return data


# Split string into nth
def String_split_nth(str_line, n):
    list_splited = [str_line[i:i + n] for i in range(0, len(str_line), n)]  # Split done here
    print(list_splited)
    for i in range(len(list_splited)):
        list_splited[i] = int(list_splited[i], 16)  # turn list of strings to list of hex one-by-one
    return list_splited


def String_split_nth_raw(str_line, n):
    list_splited = [str_line[i:i + n] for i in range(0, len(str_line), n)]  # Split done here
    print(list_splited)
    return list_splited


# convert list to 1 list with 2 character per element
def list_hex(list):
    list_out = []
    for i in range(0, len(list)):
        list_out.append(String_split_nth(list[i], 2))
    combine = compress_list(list_out)
    return combine


def list_hex_raw(list):
    list_out = []
    for i in range(0, len(list)):
        list_out.append(String_split_nth_raw(list[i], 2))
    combine = compress_list(list_out)
    return combine


#  turn Datafile into 2D-list of hex
def Datafile2hex(Data_list):
    Data_extracted = list_hex(extractData(9, -2, Data_list))
    return Data_extracted


def Datafile2hex_raw(Data_list):
    Data_extracted = list_hex_raw(extractData(11, -3, Data_list))
    return Data_extracted


# compress list of list to 1 list
def compress_list(list):
    compress = []
    for i in range(len(list)):
        compress += list[i]
    return compress


# fill list to 128 per
def fill(list):
    filled_list = []
    idx = 0
    for i in range(len(list)):
        filled_list.append(list[i])
        idx += 1
    while idx % 128 != 0:
        filled_list.append(255)
        idx += 1
    return filled_list


def fill_raw(list):
    filled_list = []
    idx = 0
    for i in range(len(list)):
        filled_list.append(list[i])
        idx += 1
    while idx % 128 != 0:
        filled_list.append('FF')
        idx += 1
    return filled_list


# turn list to numpy Block[n]
def reshape_list(block, width):
    data = []
    for i in range(0, len(block), width):
        line = block[i:i + width]
        data.append(line)
    return data


# convert hex list to numpy Block can be used for flashing
def convert_raw(lists):
    return fill_raw(Datafile2hex_raw(lists))


def convert_hex_file(list):
    return reshape_list(fill(Datafile2hex(list)), 128)
