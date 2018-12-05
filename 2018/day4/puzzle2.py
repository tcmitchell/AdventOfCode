import argparse
import collections
import datetime
import logging
import sys

DATE_FORMAT = '[%Y-%m-%d %H:%M]'
STATE_SLEEP = 'SLEEP'
STATE_WAKE = 'WAKE'


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType('r'),
                        metavar="PUZZLE_INPUT")
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    return args


def init_logging(debug=False):
    msgFormat = '%(asctime)s %(levelname)s %(message)s'
    dateFormat = '%m/%d/%Y %H:%M:%S'
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(format=msgFormat, datefmt=dateFormat, level=level)


def parse_event(event_str):
    elems = event_str.split(' ')
    logging.debug('split: {}'.format(elems))
    datestr = ' '.join(elems[0:2])
    logging.debug('datestr: {}'.format(datestr))
    dt = datetime.datetime.strptime(datestr, DATE_FORMAT)
    if elems[2] == 'wakes':
        evt_type = STATE_WAKE
    elif elems[2] == 'falls':
        evt_type = STATE_SLEEP
    else:
        evt_type = int(elems[3][1:])

    logging.debug('{} {}'.format(dt, evt_type))
    return (dt, evt_type)


def load_input(fp):
    return [parse_event(line.strip()) for line in fp]
        

def hourlist():
    return [0 for m in range(60)]

def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    events = load_input(args.input)
    events.sort(key=lambda x: x[0])
    sleep_time = collections.defaultdict(hourlist)
    curr_guard = None
    curr_state = None
    sleep_start = None
    for e in events:
        evt_state = e[1]
        if type(evt_state) == int:
            curr_guard = evt_state
            curr_state = STATE_WAKE
        elif evt_state == STATE_SLEEP:
            curr_state = evt_state
            sleep_start = e[0].minute
        elif evt_state == STATE_WAKE:
            curr_state = evt_state
            sleep_end = e[0].minute
            for m in range(sleep_start, sleep_end):
                sleep_time[curr_guard][m] += 1
            sleep_start = None
    sleepiest_guard = None
    sleepiest_minute = -1
    sleepiest_times = -1
    for guard, hour in sleep_time.items():
        for m in range(len(hour)):
            if hour[m] > sleepiest_times:
                sleepiest_guard = guard
                sleepiest_minute = m
                sleepiest_times = hour[m]
    logging.info('Guard {} sleepiest minute is {} with {} occurrences'.format(sleepiest_guard,
                                                                              sleepiest_minute,
                                                                              sleepiest_times))
    answer = sleepiest_guard * sleepiest_minute
    logging.info('Answer: Guard {} * minute {} = {}'.format(sleepiest_guard, sleepiest_minute, answer))


if __name__ == '__main__':
    main(sys.argv)
