import sys
import time


def delayinput(text, timeamount=0.08):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(timeamount)
    sys.stdout.write("\n")
    sys.stdout.flush()
    output = input()
    return output

def prDelay(text, timeamount=0.08):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(timeamount)
    print()


def print_with_color(text, color):
    if color == 'red':
        print('\033[91m' + text + '\033[0m')
    elif color == 'green':
        print('\033[92m' + text + '\033[0m')
    elif color == 'yellow':
        print('\033[93m' + text + '\033[0m')
    elif color == 'blue':
        print('\033[94m' + text + '\033[0m')
    elif color == 'magenta':
        print('\033[95m' + text + '\033[0m')
    elif color == 'cyan':
        print('\033[96m' + text + '\033[0m')
    elif color == 'white':
        print('\033[97m' + text + '\033[0m')
    elif color == 'black':
        print('\033[90m' + text + '\033[0m')


def print_with_wait(text, color, wait):
    print_with_color(text, color)
    time.sleep(wait)


def print_with_wait_no_color(text, wait):
    print(text)
    time.sleep(wait)


def print_with_delay_and_color(text, color, timeamount=0.08):
    if color == 'red':
        prDelay('\033[91m' + text + '\033[0m', timeamount)
    elif color == 'green':
        prDelay('\033[92m' + text + '\033[0m', timeamount)
    elif color == 'yellow':
        prDelay('\033[93m' + text + '\033[0m', timeamount)
    elif color == 'blue':
        prDelay('\033[94m' + text + '\033[0m', timeamount)
    elif color == 'magenta':
        prDelay('\033[95m' + text + '\033[0m', timeamount)
    elif color == 'cyan':
        prDelay('\033[96m' + text + '\033[0m', timeamount)
    elif color == 'white':
        prDelay('\033[97m' + text + '\033[0m', timeamount)
    elif color == 'black':
        prDelay('\033[90m' + text + '\033[0m', timeamount)


def print_with_wait_and_delay_and_color(text, color, wait, timeamount=0.08):
    print_with_delay_and_color(text, color, timeamount)
    time.sleep(wait)


def print_with_wait_and_delay(text, wait, timeamount=0.08):
    prDelay(text, timeamount)
    time.sleep(wait)
