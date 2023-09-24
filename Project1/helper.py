import heapq
from message import Message
from command import Command
def recursion(graph,result, start, end, time, types, msg,visited, received_cancel,length):
    # types->int
    if time > length:
        return
    if result.get(time) is None:
        result[time] = {}
    if result.get(time).get(end) is None:
        result[time][end] = [] # store all msg at given time

    if types == 0:
        if received_cancel.get(end) is None:
            received_cancel[end] = time



    if start != -1:
        received_msg = Message(msg, types, start, end, 0)
        heapq.heappush(result[time][end], received_msg)
        if end in visited and types == 0:
            return
    # if current time is greater than the time we receive cancellation, and we are going to send alert later
    # we can just stop
    if time > received_cancel.get(end, length + 1) and types == 1:
        return

    if types == 0:
        visited.add(end)

    # send message to all reachable devices and increase total time by time+val
    for key, val in sorted(graph.get(end).items()):
        sent_msg = Message(msg, types,end,key,1)
        heapq.heappush(result[time][end],sent_msg)
        recursion(graph,result,end,key,time+val, types,msg,visited,received_cancel,length)

    if types == 0:
        visited.remove(end)


def display_result(result, length):
    for time, subdict in sorted(result.items()):
        for _, msgs in sorted(subdict.items()):
            for m in msgs:
                print(f'@{time}:{m}')
    print(f'@{length}: END')


def read_files(f, graph):
    contents = f.readlines()

    for line in contents:
        if line.strip() and '#' not in line:
            stripped_line = line.strip()
            segments = stripped_line.split(' ')
            if 'LENGTH' in segments:
                length = int(segments[1]) * 60000

            elif 'PROPAGATE' in segments:
                start = int(segments[1])
                end = int(segments[2])
                delay = int(segments[3])
                if graph.get(start) is None:
                    graph[start] = {}
                graph[start][end] = delay

            elif 'ALERT' in segments or 'CANCEL' in segments:
                types = 0 if segments[0] == 'CANCEL' else 1
                msg = segments[2]
                node = int(segments[1])
                time = int(segments[3])
                com = Command(msg, time, node, types)
                Command.add(com)
    return length