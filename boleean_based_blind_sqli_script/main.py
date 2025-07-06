#!/usr/bin/env python3

import signal
import sys

from boolean_based_blind_sqli import Sqli

def def_handler(sig,frame):
    print(f'\n\n[!] Saliendo...\n')
    sys.exit(1)

# Ctrl + C
signal.signal(signal.SIGINT,def_handler)

if __name__ == '__main__':
    sql_injection = Sqli('http://127.0.0.1/boolean_based_blind_sqli.php')
    sql_injection.run()
