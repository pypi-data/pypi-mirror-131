import sys

from xml.dom.minidom import parse

from . import burp2warc

if __name__ == '__main__':
    banner = '''
====================================
 __      ____ _ _ __ ___ ___ _ __ 
 \ \ /\ / / _` | '__/ __/ _ \ '__|
  \ V  V / (_| | | | (_|  __/ |   
   \_/\_/ \__,_|_|  \___\___|_|
====================================

    '''
    print(banner)
    if len(sys.argv) == 0 or len(sys.argv) != 4 or sys.argv[1] == '-h':
        print('usage: python warc-convert.py [command] [input file] [output file]')
        print('example: python warc-convert.py burp2warc test.xml test.warc')
    else:
        command = sys.argv[1]
        if command == 'burp2warc':
            content = parse(sys.argv[2])
            burp2warc(content, sys.argv[3])
        