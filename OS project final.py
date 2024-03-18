class Process:
    def __init__(self, id, arrival, burst):
        self.id = id
        self.arrival = arrival
        self.burst = burst
        self.remainingTime = burst
        self.StartCycle = None
        self.ExitCycle = None
        self.Finished = False

    def executeRR(self, quantum, cycle):

        if(self.remainingTime == self.burst): #process gets cpu for the first time
            self.StartCycle = cycle
        
        if(self.remainingTime <= quantum): #if the process need q time or less
            self.ExitCycle = cycle + self.remainingTime
            # self.remainingTime = 0
            self.Finished = True
        else: #the process need more than q to finish 
            self.remainingTime -= quantum
            self.Finished = False
    
    def executeFCFS(self, cycle):
        self.ExitCycle = cycle + self.remainingTime
        self.Finished = True

    def getResponse(self):
        return self.StartCycle - self.arrival

    def getTurnAround(self):
        return self.ExitCycle - self.arrival
    
    def getWaiting(self):
        return self.getTurnAround() - self.burst




quantum1 =8
quantum2 = 16
ready_q = []
finished_process = []
q1 = []
q2 = []
totalBurstTimes = 0
ready_size = int(input("Enter Number of processes to equeue to ready queue: "))
for i in range(ready_size):
    burst = int(input("Enter Burst Time: "))
    arrival = int(input("Enter Arrival Time: "))
    p1= Process(i, arrival, burst)
    totalBurstTimes+=burst
    ready_q.append(p1)




#sort ready_q according to arrival time
ready_q= sorted(ready_q,key = lambda x:x.arrival, reverse=False)

#allocated CPU time for each queue
q0_time = int(totalBurstTimes*0.6)
q1_time = int(totalBurstTimes*0.25) + q0_time
q2_time = int(totalBurstTimes*0.15) + q1_time

CPU_cycle = 0
for p in ready_q:
    #if this queue used more than of allocated cpu time then break and move to the next queue
    if(CPU_cycle> q0_time):
        break
    p.executeRR(quantum1,CPU_cycle)
    if(p.Finished == False):
        q1.append(p)
        CPU_cycle+=quantum1
    else:
        CPU_cycle += p.remainingTime
        finished_process.append(p)

for p in q1:
    #if this queue used more than of allocated cpu time then break and move to the next queue
    if(CPU_cycle > q1_time):
        break
    p.executeRR(quantum2,CPU_cycle)
    if(p.Finished == False):
        q2.append(p)
        CPU_cycle+=quantum2
    else:
        CPU_cycle += p.remainingTime
        finished_process.append(p)

for p in q2:
    #if this queue used more than of allocated cpu time then break and move to the next step
    if(CPU_cycle> q2_time):
        break
    p.executeFCFS(CPU_cycle)
    CPU_cycle += p.remainingTime
    finished_process.append(p)



totalWaiting = 0
totalResponse = 0
totalTurnArround = 0
for process in finished_process:
    totalWaiting+= process.getWaiting()
    totalResponse+= process.getResponse()
    totalTurnArround+= process.getTurnAround()

for p in finished_process:
    print("--------------------------------------------------------------------------------------")
    print(f"PID: {p.id}\n")
    print(f"Start of execution: {p.StartCycle}")
    print(f"End of Execution: {p.ExitCycle}")
    print(f"Response Time: {p.getResponse()}")
    print(f"Turnaround Time: {p.getTurnAround()}")
    print(f"Waiting Time: {p.getWaiting()}")
    print("--------------------------------------------------------------------------------------")



print("--------------------------------------------------------------------------------------")
print("Execution Summary: ")
print(f"Average Waiting = {totalWaiting/ready_size}")
print(f"Average Response = {totalResponse/ready_size}")
print(f"Average TurnArround = {totalTurnArround/ready_size}")
print("--------------------------------------------------------------------------------------")




