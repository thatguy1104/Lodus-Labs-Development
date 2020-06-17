import sys
import time


def progress(count, total, suffix=''):
    bar_len = 40
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '*' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s written to <play_dev_ranks> %s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()

def run():
    counter = 0
    total = 100

    for i in range(total):
        progress(i, total)
        time.sleep(0.05)

    sys.stdout.write('\n')

run()