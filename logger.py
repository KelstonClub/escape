import os, sys
import logging

import networkzero as nw0

def main():
    logger = nw0.advertise("logger")
    message = nw0.wait_for_news_from(logger)
    print(message)

if __name__ == '__main__':
    main(*sys.argv[1:])
