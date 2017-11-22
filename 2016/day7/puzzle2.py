#!/usr/bin/env python

import re
import sys

class IPv7(object):

    def __init__(self, addr):
        self.addr = addr
        (self.supernets, self.hypernets) = self._parse_addr(addr)

    def _parse_addr(self, addr):
        """Return a list of supernets and a list of hypernets"""
        snets = []
        hnets = []
        prog = re.compile('([^[]+)\[([^\]]+)\]')
        m = prog.match(addr)
        while m:
            snets.append(m.group(1))
            hnets.append(m.group(2))
            addr = addr[len(m.group(0)):]
            m = prog.match(addr)
        snets.append(addr)
        return (snets, hnets)

    def supports_tls(self):
        for h in self.hypernets:
            if has_abba(h):
                return False
        for s in self.supernets:
            if has_abba(s):
                return True
        return False

    def supports_ssl(self):
        all_aba = []
        for s in self.supernets:
            all_aba.extend(has_aba(s))
        all_bab = [aba2bab(x) for x in all_aba]
        for bab in all_bab:
            for h in self.hypernets:
                if bab in h:
                    return True
        return False

def is_abba(text):
    return (text[0] == text[3] and
            text[1] == text[2] and
            text[0] != text[1])

def has_abba(text):
    while len(text) >= 4:
        if is_abba(text):
            return True
        text = text[1:]
    return False

def is_aba(text):
    return (text[0] == text[2] and
            text[0] != text[1])

def has_aba(text):
    aba_matches = []
    while len(text) >= 3:
        if is_aba(text):
            aba_matches.append(text[0:3])
        text = text[1:]
    return aba_matches

def aba2bab(x):
    return ''.join([x[1], x[0], x[1]])

def parse_data(datafile):
    addrs = []
    with open(datafile, 'rb') as f:
        for line in f:
            line = line.strip()
            ipv7 = IPv7(line)
            addrs.append(ipv7)
    return addrs

def main(argv):
    datafile = argv[1]
    addrs = parse_data(datafile)
    tls_count = sum(addr.supports_tls() for addr in addrs)
    print 'TLS count:', tls_count
    ssl_count = sum(addr.supports_ssl() for addr in addrs)
    print 'SSL count:', ssl_count

# The answer is NOT 114
# 109 is too low

if __name__ == '__main__':
    main(sys.argv)
