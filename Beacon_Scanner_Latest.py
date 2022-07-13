import time
from datetime import datetime
from beacontools import BeaconScanner, IBeaconAdvertisement

from csv import writer
from csv import DictWriter

def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

    #uuidd = int(uuidd)
def callback(bt_addr, rssi, packet, additional_info):
    now = datetime.now()
    curr_time = now.strftime("%H:%M:%S")
    curr_date = now.strftime("%D")
    print("00000000000000000000000000000000")
    print(additional_info['uuid'])
    row_contents = [curr_date,curr_time,additional_info['uuid']]
   # print('*** Append new row to an existing csv file using csv.writer() in python ***')
        # Append a list as new line to an old csv file
    append_list_as_row('Beacons.csv', row_contents)
    print("%s %s %s" % (curr_date, curr_time, packet))

scanner = BeaconScanner(callback, packet_filter=IBeaconAdvertisement)
scanner.start()
#time.sleep(5)
#scanner.stop()

