__author__ = 'rasha'
import csv
import numpy as np
import mysql.connector
import datetime
import uuid
from sklearn import svm
from sklearn.externals import joblib

def complex_split(arr, fft_size):
    real_arr=np.array((arr[0].real,arr[0].imag))
    for i in range(1,int(fft_size/2)):
        row_values=np.array([arr[i].real, arr[i].imag])
        real_arr=np.vstack((real_arr,row_values))
    return real_arr

def create_buffer(currLine, fft_size,ind, buff):
    temp_in=(float(currLine[ind]))
    buff=np.hstack((temp_in,buff))
    buff=buff[0:fft_size]
    return buff

def create_mag_array(four_array, fft_size):
    array_mag=np.array((abs(four_array[1])))
    for i in range(2,int(fft_size/2)):
        array_mag_i=np.array((abs(four_array[i])))
        array_mag=np.vstack((array_mag, array_mag_i))
    return array_mag

fft_size=1024
fs=92

USERNAME = 'iotshm'
PASSWORD = 'pa$$word'
DB_NAME = 'iotshm'

# Create Frequency Vector
freq_array=np.array((1))
for i in range(2,int(fft_size/2)):
    freq_i=np.array((i*fs/fft_size))
    freq_array=np.vstack((freq_array,freq_i))
xbuff=np.empty((fft_size))
ybuff=np.empty((fft_size))
zbuff=np.empty((fft_size))
tbuff=np.empty((fft_size))
with open('adxl345test.csv') as f:
    reader=csv.reader(f,dialect='excel')
    a=next(reader)
    while reader.line_num < fft_size+1:
        # print(reader.line_num)
        a=next(reader)
        xbuff=create_buffer(a,fft_size, 0, xbuff)
        ybuff=create_buffer(a,fft_size,1,ybuff)
        zbuff=create_buffer(a,fft_size,2,zbuff)
        tbuff=create_buffer(a, fft_size, 3, tbuff)
    xfour=np.fft.rfft(xbuff)
    yfour=np.fft.rfft(ybuff)
    zfour=np.fft.rfft(zbuff)
    TimeStamp=tbuff[fft_size-1]
    print(TimeStamp)
    x_mag=create_mag_array(xfour, fft_size)
    y_mag=create_mag_array(yfour, fft_size)
    z_mag=create_mag_array(zfour, fft_size)
    x_magfreq=np.hstack((freq_array,x_mag))
    y_magfreq=np.hstack((freq_array, y_mag))
    z_magfreq=np.hstack((freq_array, y_mag))

conn = mysql.connector.connect(host='iotshm-data.ck3sx5qm0blx.us-west-2.rds.amazonaws.com',database=DB_NAME,user=USERNAME,password=PASSWORD)
print(conn)
cursor=conn.cursor()
date_time=datetime.datetime.fromtimestamp(TimeStamp).strftime('%Y-%m-%d %H:%M:%S')
print(date_time)
#query="SELECT * FROM Health"
#cursor.execute(query)
#row = cursor.fetchone()
#while row is not None:
#    print(row)
#    row = cursor.fetchone()
#query="INSERT INTO Health(sensor_id,timestamp,x_health,y_health,z_health) VALUES('%s', '%s', %i, %i, %i)"
#args=('1',date_time, 1, 1, 0)
#cursor.execute(query%args)
#conn.commit()

for i in range(0,int(fft_size/2)-1):
    freq_i=freq_array[i]
    x_i=x_mag[i]
    y_i=y_mag[i]
    z_i=z_mag[i]
    serial_num=uuid.uuid4()
    print(serial_num)
    query="INSERT INTO Magnitude(frequency,sensor_id,x_magnitude,y_magnitude,z_magnitude, timestamp, reading_id) VALUES(%f, '%s', %f, %f, %f, '%s', '%s')"
    args=(freq_i,'1', x_i, y_i, z_i, date_time, serial_num)
    cursor.execute(query%args)
    conn.commit()
cursor.close
conn.close

#print(conn.list_tables())
#rt_table=Table('dynamo-iotshm-realtime',connection=conn)
#desc=rt_table.describe()
#print(desc)

#for i in range(0,int(fft_size/2)-1):
#    freq_i=freq_array[i]
#    x_i=x_mag[i]
#    y_i=y_mag[i]
#    z_i=z_mag[i]
#    item = rt_table.put_item(data={
#                      'Sensor Id':'1',
#                      'TimeStamp': TimeStamp,
#                      'Frequency': freq_i,
#                      'X Magnitude': x_i,
#                      'Y Maginitude': y_i,
#                      'Z Magnitude': z_i,
#                      },overwrite=True)
# xreal=complex_split(xfour, fft_size)
# yreal=complex_split(yfour, fft_size)
# zreal=complex_split(zfour, fft_size)
# np.savetxt('xFourData.csv', xreal, delimiter=',')
# try with 3d fft
#     ndbuff=np.vstack((xbuff,ybuff,zbuff))
#     ndfourier=np.fft.rfftn(ndbuff)
# clf=svm.OneClassSVM(gamma=.001)
# print('classifier made')
# clf.fit(xreal, sample_weight=None)

