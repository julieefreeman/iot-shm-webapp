__author__ = 'rasha'
import csv
import numpy as np
from sklearn import svm
from sklearn.externals import joblib

fft_size=1000

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
    print(xfour)
    yfour=np.fft.rfft(ybuff)
    zfour=np.fft.rfft(zbuff)
    xreal=complex_split(xfour, fft_size)
    yreal=complex_split(yfour, fft_size)
    zreal=complex_split(zfour, fft_size)
    # np.savetxt('xFourData.csv', xreal, delimiter=',')
# try with 3d fft
#     ndbuff=np.vstack((xbuff,ybuff,zbuff))
#     ndfourier=np.fft.rfftn(ndbuff)
# clf=svm.OneClassSVM(gamma=.001)
# print('classifier made')
# clf.fit(xreal, sample_weight=None)

