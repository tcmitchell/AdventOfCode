from __future__ import annotations
import argparse
import logging
from typing import TextIO, Union


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType('r'),
                        metavar="PUZZLE_INPUT")
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args(args)
    return args


def init_logging(debug=False):
    msg_format = '%(asctime)s %(levelname)s %(message)s'
    date_format = '%m/%d/%Y %H:%M:%S'
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(format=msg_format, datefmt=date_format, level=level)


def load_input(fp: TextIO):
    return fp.read().strip()


def hex2bin(packet: str) -> str:
    target_len = len(packet) * 4
    i = int(packet, 16)
    b = bin(i)
    # drop the '0b' prefix
    b = b[2:]
    # pad out to the target length
    return b.zfill(target_len)


class Literal:

    def __init__(self, version: int, p_type: int):
        logging.debug("Version: %d", version)
        self.version = version
        self.p_type = p_type
        self.value = None

    def parse(self, packet: str) -> str:
        literal_bits = ''
        parse_more = True
        while parse_more:
            parse_more = packet[0] == '1'
            literal_bits += packet[1:5]
            packet = packet[5:]
        self.value = int(literal_bits, base=2)
        logging.debug("Parsed literal: %d", self.value)
        return packet

    def sum_versions(self) -> int:
        return self.version


class Operator:

    def __init__(self, version: int, op_type: int):
        logging.debug("Version: %d", version)
        self.version = version
        self.op_type = op_type
        self.children = []

    def parse(self, packet: str) -> str:
        lti = packet[0]
        if lti == '0':
            bit_len = int(packet[1:16], base=2)
            packet = packet[16:]
            subpacket = packet[:bit_len]
            packet = packet[bit_len:]
            while subpacket:
                subpacket, thing = parse_packet(subpacket)
                self.children.append(thing)
        else:
            subpacket_count = int(packet[1:12], base=2)
            packet = packet[12:]
            for i in range(subpacket_count):
                packet, thing = parse_packet(packet)
                self.children.append(thing)
        return packet

    def sum_versions(self) -> int:
        return self.version + sum([child.sum_versions() for child in self.children])


TYPE_LITERAL = 4


def parse_header(packet: str) -> tuple[str, int, int]:
    version = int(packet[:3], base=2)
    p_type = int(packet[3:6], base=2)
    return packet[6:], version, p_type


def parse_packet(packet: str) -> tuple[str, Union[Literal, Operator]]:
    packet, version, p_type = parse_header(packet)
    if p_type == TYPE_LITERAL:
        literal = Literal(version, p_type)
        packet = literal.parse(packet)
        return packet, literal
    else:
        # Anything non-literal is an operator
        operator = Operator(version, p_type)
        packet = operator.parse(packet)
        return packet, operator


def puzzle1(packet: str) -> int:
    packet = hex2bin(packet)
    _, thing = parse_packet(packet)
    return thing.sum_versions()


def puzzle2(data) -> int:
    return 0


def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    data = load_input(args.input)
    answer = puzzle1(data)
    logging.info('Puzzle 1: %d', answer)
    answer = puzzle2(data)
    logging.info('Puzzle 2: %d', answer)


if __name__ == '__main__':
    main()
