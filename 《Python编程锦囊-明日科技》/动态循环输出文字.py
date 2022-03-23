import sys
import time


def print_act(word):
    sys.stdout.write("\r")
    sys.stdout.flush()
    for item in word:

        sys.stdout.write(item)
        sys.stdout.flush()
        time.sleep(0.1)
    print('访澳旅客    ' + chr(0xf090) +' '+chr(0xf091)+'    访澳旅客')
while True:
    print_act('VISITANTES     VISITANTES' +'\n')