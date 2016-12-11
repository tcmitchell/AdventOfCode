#!/usr/bin/env python

import re
import sys

gives_regex = r'bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)'
gives_prog = re.compile(gives_regex)
value_regex = r'value (\d+) goes to bot (\d+)'
value_prog = re.compile(value_regex)

class Output(object):

    all_outputs = {}

    @classmethod
    def find_output(cls, output_id):
        if output_id in Output.all_outputs:
            output = Output.all_outputs[output_id]
        else:
            output = Output(output_id)
            Output.all_outputs[output_id] = output
        return output

    def __init__(self, id):
        self.id = id
        self.type = 'output'
        self.value = None

    def take_value(self, value):
        # print 'Output %s got %s' % (self.id, value)
        self.value = value


class Bot(object):

    all_bots = {}

    @classmethod
    def find_bot(cls, bot_id):
        if bot_id in Bot.all_bots:
            bot = Bot.all_bots[bot_id]
        else:
            bot = Bot(bot_id)
            Bot.all_bots[bot_id] = bot
        return bot

    def __init__(self, id):
        self.id = id
        self.type = 'bot'
        self.high_dest = None
        self.low_dest = None
        self.value1 = None
        self.value2 = None

    def set_dest(self, low_dest, high_dest):
        if self.low_dest or self.high_dest:
            raise Exception('Overwriting destinations for bot %s' % (self.id))
        self.low_dest = low_dest
        self.high_dest = high_dest
        self.execute()

    def execute(self):
        if (self.high_dest and self.low_dest and
            self.value1 is not None and self.value2 is not None):
            self.check_values()
            if self.value1 > self.value2:
                self.give_values(self.value2, self.value1)
            elif self.value1 < self.value2:
                self.give_values(self.value1, self.value2)
            else:
                msg = 'execute: value1 = %r, value2 = %r'
                print msg % (self.value1, self.value2)
            return True
        return False

    def give_values(self, low_value, high_value):
        # print 'Bot %s giving %s to %s %s' % (self.id, low_value, self.low_dest.type, self.low_dest.id)
        self.low_dest.take_value(low_value)
        # print 'Bot %s giving %s to %s %s' % (self.id, high_value, self.high_dest.type, self.high_dest.id)
        self.high_dest.take_value(high_value)
        self.value1 = None
        self.value2 = None

    def take_value(self, value):
        # print 'Bot %s taking %s' % (self.id, value)
        if self.value1 is None:
            self.value1 = value
        elif self.value2 is None:
            self.value2 = value
            self.execute()
        else:
            raise Exception('Bot %s already has two values!' % (self.id))

    def check_values(self):
        target = [61, 17]
        if self.value1 in target and self.value2 in target:
            msg = 'Bot %s compares %s and %s'
            # raise Exception(msg % (self.id, self.value1, self.value2))
            print msg % (self.id, self.value1, self.value2)


def find_dest(type, id):
    if type == 'bot':
        return Bot.find_bot(id)
    elif type == 'output':
        return Output.find_output(id)
    else:
        raise Exception('find_dest unkown type %r, id %s' % (type, id))

def handle_gives_command(re_match):
    bot_id = int(re_match.group(1))
    low_type = re_match.group(2)
    low_dest = int(re_match.group(3))
    high_type = re_match.group(4)
    high_dest = int(re_match.group(5))
    bot = Bot.find_bot(bot_id)
    bot.set_dest(find_dest(low_type, low_dest),
                 find_dest(high_type, high_dest))

def handle_value_command(re_match):
    "value 5 goes to bot 2"
    value = int(re_match.group(1))
    bot_id = int(re_match.group(2))
    bot = Bot.find_bot(bot_id)
    bot.take_value(value)

def parse_command(line):
    m = gives_prog.match(line)
    if m:
        return handle_gives_command(m)
    m = value_prog.match(line)
    if m:
        return handle_value_command(m)
    raise Exception('unknown command %r' % (line))

def load_data(datafile):
    with open(datafile, 'rb') as f:
        for line in f:
            parse_command(line)

# Wrong: 128 is too high - was comparing values as strings, not ints

def main(argv=None):
    if not argv:
        argv = sys.argv
    datafile = argv[1]
    load_data(datafile)
    outputs = [Output.find_output(oid) for oid in [0, 1, 2]]
    print reduce(lambda x, y: x*y, [o.value for o in outputs])

if __name__ == '__main__':
    main()
