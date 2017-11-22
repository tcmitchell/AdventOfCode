#!/usr/bin/env python

import sys
import md5

def nextChar(door_id, index, digest_prefix, digest_index, pos_index):
    idx = index
    while True:
        x = md5.new(door_id + str(idx))
        digest = x.hexdigest()
        if digest.startswith(digest_prefix):
            print 'Digest prefix match:', digest, 'at index', idx
            return (digest[digest_index], digest[pos_index], idx)
        else:
            idx += 1

def main(argv):
    digest_prefix = '00000'
    digest_index = 6  # 7th character
    pos_index = 5  # 6th character
    password_length = 8
    door_id = argv[1]
    password = [' '] * password_length
    index = -1
    while ' ' in password:
        (char, pos, index)  = nextChar(door_id, index + 1, digest_prefix,
                                       digest_index, pos_index)
        try:
            pos = int(pos)
        except:
            print 'Skipping pos', pos
            pos = len(password)
        print 'char:', char, 'pos:', pos, 'index:', index
        if pos < len(password) and password[pos] == ' ':
            password[pos] = char
        else:
            print 'pos', pos, '>=', len(password)
        print 'In progess:', ''.join(password)
    print ''.join(password)

if __name__ == '__main__':
    main(sys.argv)
