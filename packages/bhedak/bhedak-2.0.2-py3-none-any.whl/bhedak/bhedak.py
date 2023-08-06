from re import sub
from urllib.parse import quote
from sys import stdin, stdout, argv, exit

def runBhedak():
    try:
        value = quote(str(argv[1]), safe='')
    except IndexError:
        value = quote("FUZZ", safe='')

    try:
        for url in stdin.readlines():
            domain = str(url.strip())
            stdout.write(sub(r"=[^?\|&]*", '=' + str(value), str(domain)) + '\n')
    except KeyboardInterrupt:
        exit (0)
    except:
        exit(127)
