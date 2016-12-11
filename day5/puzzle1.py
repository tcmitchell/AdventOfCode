#!/usr/bin/env python

import sys
import md5

def nextChar(door_id, index, digest_prefix, digest_index):
    idx = index
    while True:
        x = md5.new(door_id + str(idx))
        digest = x.hexdigest()
        if digest.startswith(digest_prefix):
            print 'Digest prefix match:', digest, 'at index', idx
            return (digest[digest_index], idx)
        else:
            idx += 1

def main(argv):
    digest_prefix = '00000'
    digest_index = 5  # 6th character
    password_length = 8
    door_id = argv[1]
    password = ''
    index = -1
    while len(password) < password_length:
        (char, index)  = nextChar(door_id, index + 1, digest_prefix, digest_index)
        password += char
        print 'In progess:', password
    print password

if __name__ == '__main__':
    main(sys.argv)
