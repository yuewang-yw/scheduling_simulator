'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
'''
import sys
import copy

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time, index):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
        self.index = index
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrival_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum ):
    #store the (switching time, proccess_id) pair
    schedule = []
    schedule_idx = []
    current_time = 0
    waiting_time = 0
    process_queue = []
    process_list_cp = copy.deepcopy(process_list)
    process_no = len(process_list_cp)
    while process_queue != [] or process_list_cp!= []:
        if process_queue == []:
            process_queue.append(process_list_cp[0])
            current_time = process_list_cp[0].arrive_time
            process_list_cp.pop(0)
        else:
            current_process = process_queue.pop(0)
            # Append to schedule if it's not the same process as the last quantum
            if schedule == [] or current_process.index != schedule_idx[-1]:
                schedule.append((current_time, current_process.id, current_process.index))
                schedule_idx.append(current_process.index)
                # update wait time and last scheduled time
                waiting_time = waiting_time + current_time - current_process.last_scheduled_time
                current_process.last_scheduled_time = current_time + time_quantum
            # update current time and remaining time of current process
            # current time = the time when current process ends
            if current_process.burst_time > time_quantum:
                current_time = current_time + time_quantum
                current_process.burst_time = current_process.burst_time - time_quantum
            else:
                current_time = current_time + current_process.burst_time
                current_process.burst_time = 0
            process_queue_no = 0
            # add process arrived by current time in queue
            for process in process_list_cp:
                if process.arrive_time <= current_time:
                    process.last_scheduled_time = process.arrive_time
                    process_queue.append(process)
                    process_queue_no = process_queue_no + 1
                else:
                    break
            # clear process list
            for i in range(process_queue_no):
                process_list_cp.pop(0)
            # Append current process to end of queue
            if current_process.burst_time > 0:
                process_queue.append(current_process)

    average_waiting_time = waiting_time/float(process_no)
    return schedule, average_waiting_time


def SRTF_scheduling(process_list):
    #return (["to be completed, scheduling process_list on SRTF, using process.burst_time to calculate the remaining time of the current process "], 0.0)
    schedule = []
    schedule_idx = []
    current_time = 0
    waiting_time = 0
    process_queue = []
    process_list_cp = process_list.copy()
    process_no = len(process_list_cp)

    while process_queue != [] or process_list_cp!= []:
        if process_queue == []:
            process_queue.append(process_list_cp[0])
            current_time = process_list_cp[0].arrive_time
            process_list_cp.pop(0)
        else:
            if process_list_cp != []:
                next_arrival_process = process_list_cp[0]
                next_arrival_process.last_scheduled_time = next_arrival_process.arrive_time
                if schedule == [] or process_queue[0].index != schedule_idx[-1]:
                    schedule.append((current_time, process_queue[0].id, process_queue[0].index))
                    schedule_idx.append(process_queue[0].index)
                    waiting_time = waiting_time + current_time - process_queue[0].last_scheduled_time
                # If next arrival is earlier than the completion of current process
                if next_arrival_process.arrive_time <= current_time + process_queue[0].burst_time:
                    exec_time = next_arrival_process.arrive_time - current_time
                    current_time = current_time + exec_time
                    process_queue[0].burst_time = process_queue[0].burst_time - exec_time
                    process_queue[0].last_scheduled_time = current_time
                    process_queue.append(next_arrival_process)
                    process_queue.sort(key=lambda x: x.burst_time, reverse=False)
                    process_list_cp.pop(0)
                else:
                    current_time = current_time + process_queue[0].burst_time
                    process_queue.pop(0)
            else:
                for process in process_queue:
                    if schedule == [] or process.index != schedule_idx[-1]:
                        schedule.append((current_time, process.id, process.index))
                        schedule_idx.append(process.index)
                        waiting_time = waiting_time + current_time - process.last_scheduled_time
                        process.last_scheduled_time = current_time
                    current_time = current_time + process.burst_time
                process_queue=[]

    average_waiting_time = waiting_time/float(process_no)
    return schedule, average_waiting_time
def SJF_scheduling(process_list, alpha):
    return (["to be completed, scheduling SJF without using information from process.burst_time"],0.0)


def read_input():
    result = []
    index = 0
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2]), index))
            index = index + 1
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    #main(sys.argv[1:])
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )
