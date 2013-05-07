#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
#import lib.server.server_threaded as server_threaded
import lib.server.server as server
import lib.config as config
import threading

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mmpath') 
    args = parser.parse_args()
    config.mm_path = args.mmpath
    try:
        server.run()
    except:
        config.logger.warn("Server at port 9000 already running")

if __name__ == '__main__':
    main() 