 #====================================[  Library  ]=======================================


def extractData(start,stop, raw_data):
    data = []
    for i in range(len(raw_data)):
        a = raw_data[i]
        if len(a)>12:
            data.append(a[start:stop])
    while("" in data):
        data.remove("")
    return data

#Split string into nth
def String_split_nth(str_line,n):
    list_splited = [str_line[i:i+n] for i in range(0,len(str_line),n)] #Split done here
    print(list_splited)
    for i in range(len(list_splited)):
        list_splited[i] = int(list_splited[i],16)  # turn list of strings to list of hex one-by-one
    return list_splited


# convert list to 1 list with 2 character per element
def list_hex(list):
    list_out = []
    for i in range(0,len(list)):
        list_out.append(String_split_nth(list[i],2))
    combine = compress_list(list_out)
    return combine

#  turn Datafile into 2D-list of hex
def Datafile2hex(Data_list): 
    Data_extracted = list_hex(extractData(11,-3,Data_list))
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
        filled_list.append(hex(255))
        idx+=1
    return filled_list



# turn list to numpy Block[n]
def reshape_list(block,width):
    data = []
    for i in range(0,len(block),width):
        line = block[i:i+width]
        data.append(line)
    return data

# convert hex list to numpy Block can be used for flashing
def convert_hex_file(list):
    return reshape_list(fill(Datafile2hex(list)),128)