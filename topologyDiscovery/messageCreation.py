import csv
import math
from numpy.random import randint

# MESSAGE FORMAT:
# creationTime | eventType | msgID | source | destination | msgSize | [respSize]
# 2 C M2 1 8 1000

EVENT_TYPE = 'C'  # C stands for Message Create Event
MSG_CREATION_INTERVAL = 2
MSG_SIZE = 1000
RESP_SIZE = 500
FLOODING_MSG_LABEL = 'F'
ADVANCED_FLOODING_MSG_LABEL = 'A'
NODES = 100


def generate_source_destination():
    n = [0, 0]
    while n[0] == n[1]:
        n = randint(0, NODES, 2)
    return n


def create_normal_messages(number_of_msgs):
    with open('../data/floodingMessages.txt', 'w') as f:
        sim_time = MSG_CREATION_INTERVAL
        i = 0
        while i < number_of_msgs:
            nodes = generate_source_destination()

            line = str(sim_time) + ' ' + EVENT_TYPE + ' ' + FLOODING_MSG_LABEL + str(i) + ' ' +\
                   str(nodes[0]) + ' ' + str(nodes[1]) + ' ' + str(MSG_SIZE)
            f.write("%s\n" % line)

            sim_time += MSG_CREATION_INTERVAL
            i = i + 1

    f.close()


def create_random_messages(number_of_msgs):
    with open('../data/floodingMessages.txt', 'a') as f:
        i = number_of_msgs
        st = FLOODING_PHASE_DURATION + MSG_CREATION_INTERVAL
        while st < END_TIME:
            # ESEMPIO formato: 11 C E11 2 7 1000 500
            nodes = generate_source_destination()

            line = str(st) + ' ' + EVENT_TYPE + ' ' + ADVANCED_FLOODING_MSG_LABEL + str(i) + ' ' +\
                   str(nodes[0]) + ' ' + str(nodes[1]) + ' ' + str(MSG_SIZE) + ' ' + str(RESP_SIZE)
            f.write("%s\n" % line)

            st += MSG_CREATION_INTERVAL
            i += 1

    f.close()


def create_advanced_messages(number_of_msgs, input_source):
    if input_source == 'BAYESIAN':
        path = '../data/inferenceSources.csv'
    elif input_source == 'RELAYED_MSG':
        path = '../data/relayedMsgSources.csv'
    elif input_source == 'HOP_COUNT':
        path = '../data/hopCountSources.csv'

    with open(path) as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')

        with open('../data/floodingMessages.txt', 'a') as f:
            i = number_of_msgs
            st = FLOODING_PHASE_DURATION + MSG_CREATION_INTERVAL

            for row in csv_reader:

                line = str(st) + ' ' + EVENT_TYPE + ' ' + ADVANCED_FLOODING_MSG_LABEL + str(i) + ' ' +\
                       str(row[0]) + ' ' + str(row[1]) + ' ' + str(MSG_SIZE) + ' ' + str(RESP_SIZE)
                f.write("%s\n" % line)

                st += MSG_CREATION_INTERVAL
                i += 1
        f.close()
    csv_file.close()


CREATION_METHOD = 'ADVANCED'  # possible values: 'NORMAL', 'ADVANCED'
INPUT_SOURCE = 'RELAYED_MSG'  # 'HOP_COUNT', 'RELAYED_MSG', 'BAYESIAN', 'RANDOM'
END_TIME = 0  # only for ADVANCED, RANDOM
FLOODING_PHASE_DURATION = 60


def main():
    number_of_msgs = math.floor(FLOODING_PHASE_DURATION / MSG_CREATION_INTERVAL)

    if CREATION_METHOD == 'NORMAL':
        create_normal_messages(number_of_msgs)
    elif CREATION_METHOD == 'ADVANCED':
        if INPUT_SOURCE == 'RANDOM':
            create_random_messages(number_of_msgs)
        else:
            create_advanced_messages(number_of_msgs, INPUT_SOURCE)


if __name__ == "__main__":
    main()
