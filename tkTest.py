import os


if __name__ == '__main__':

    pwd = os.path.abspath('')

    print pwd

    path = pwd + '/zh-ko_final2.txt'

    file_size = os.path.getsize(path)
    print file_size/float(1024*1024)
    print round(file_size/float(1024*1024), 2)