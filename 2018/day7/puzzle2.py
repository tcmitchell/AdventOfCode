import argparse
import collections
import datetime
import logging
import sys


# Incorrect: BKCVJGHMSDXQFRYZOAULPIEWTN
# Incorrect: BKCVJMGSHDQXZFRYOAULPIEWTN
# Incorrect: BKVCMSGHJDQXZRFYOAULPIEWTN

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


def load_input(fp):
    return [(line[5], line[36]) for line in fp]


def step_duration(step):
    return ord(step) - 64


def free_workers(workers):
    return [i for i, t, s in workers if t == None]


def done_workers(workers, curr_time):
    return [i for i, t, s in workers if t == curr_time]


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    arcs = collections.defaultdict(list)
    for a, b in load_input(args.input):
       arcs[a]
       arcs[b].append(a)

    for k, v in arcs.items():
        logging.debug('{}: {}'.format(k, v))

    extra_time = 60
    num_workers = 5
    # extra_time = 0
    # num_workers = 2
    workers = [(w, None, None) for w in range(num_workers)]
    steps = []
    current_time = 0
    logging.info('Workers: {}'.format(workers))
    while arcs:
        # First, is any task complete?
        logging.info('{}\t{}'.format(current_time, workers))
        for dw in done_workers(workers, current_time):
            step = workers[dw][2]
            logging.info('Worker {} is done with step {}'.format(dw, step))
            steps.append(step)
            del arcs[step]
            for v in arcs.values():
                try:
                    v.remove(step)
                except ValueError as ve:
                    pass
            workers[dw] = (dw, None, None)
        running = [w[2] for w in workers if w[2] is not None]
        ready = sorted([k for k, v in arcs.items() if not v and k not in running])
        logging.info('Ready: {}'.format(ready))
        available_workers = free_workers(workers)
        while ready and available_workers:
            step = ready.pop(0)
            worker = available_workers.pop(0)
            done_time = step_duration(step) + extra_time + current_time
            workers[worker] = (worker, done_time, step)
        current_time += 1
    print('It took {} seconds'.format(current_time - 1))


if __name__ == '__main__':
    main(sys.argv)
