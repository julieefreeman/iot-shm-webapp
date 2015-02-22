__author__ = 'rasha'
import csv
import numpy as np
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
    array_mag=np.array((abs(four_array[0])))
    for i in range(1,int(fft_size/2)):
        array_mag_i=np.array((abs(four_array[i])))
        array_mag=np.vstack((array_mag, array_mag_i))
    return array_mag

fft_size=1024
fs=92
# Create Frequency Vector
freq_array=np.array((0))
for i in range(1,int(fft_size/2)):
    freq_i=np.array((i*fs/fft_size))
    freq_array=np.vstack((freq_array,freq_i))
xbuff=np.empty((fft_size))
ybuff=np.empty((fft_size))
zbuff=np.empty((fft_size))
with open('adxl345test.csv') as f:
    reader=csv.reader(f,dialect='excel')
    a=next(reader)
    while reader.line_num < fft_size+1:
        # print(reader.line_num)
        a=next(reader)
        xbuff=create_buffer(a,fft_size, 0, xbuff)
        ybuff=create_buffer(a,fft_size,1,ybuff)
        zbuff=create_buffer(a,fft_size,2,zbuff)
    xfour=np.fft.rfft(xbuff)
    yfour=np.fft.rfft(ybuff)
    zfour=np.fft.rfft(zbuff)
    x_mag=create_mag_array(xfour, fft_size)
    y_mag=create_mag_array(yfour, fft_size)
    z_mag=create_mag_array(zfour, fft_size)
    x_magfreq=np.hstack((freq_array,x_mag))
    y_magfreq=np.hstack((freq_array, y_mag))
    z_magfreq=np.hstack((freq_array, y_mag))
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

