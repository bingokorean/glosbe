

import os
import sys
import codecs

output_file = codecs.open("zhkores.txt","a+")


if __name__ == '__main__':
    abs_url = os.path.abspath('/Users/wanghao87/Desktop/corpus/cj')

    filename = sys.argv[1]

    url = abs_url + filename

    print url

    with open(url, "r") as input_file :
        for line in input_file :
            output_file.write(line)



    output_file.close()


