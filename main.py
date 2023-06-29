import numpy as np
# compare the average completion time between SRPT and FCFS for a load of 0.7
# do a couple of examples for SRPT (give a specific arrival time and size)
# do pseudocode for PS


# class to create job objects
class Job:
    def __init__(self, arrivalTime, size, rpt):
        self.arrivalTime = arrivalTime
        self.size = size
        self.departureTime = None
        self.rpt = rpt


# fcn to generate job sizes
def generateJobSize():
    return np.random.exponential(1)


# fcn that generates an interarrival time
def generateInterarrivalTime():
    return np.random.exponential(10 / 7)


# fcn that handles an arrival event
def handleArr():
    global clock, serverEmpty, servingJob, nextArrTime, nextDepTime, completionTimes, jobSizes
    # create the size of the job that just arrived
    size = generateJobSize()
    # create a new job object with these new attributes
    job = Job(arrivalTime=clock, size=size, rpt=size)
    jobSizes.append(size)
    # if the server is empty, immediately start servicing the new arrival
    if serverEmpty:
        servingJob = job
        # set this as the next departure time
        nextDepTime = clock + servingJob.size
        serverEmpty = False
    # if the new arrival has a larger size than the rpt of the job being servived, add it to the job queue and sort your list
    elif job.size > servingJob.rpt:
        # otherwise, append to the job queue
        jobQueue.append(job)
        jobQueue.sort(key=lambda x: x.rpt)
        serverEmpty = False


    # if the new arrival is smaller than the rpt of the job currently being serviced
    # change the departure time of servingJob, put that job back on the queue, and set the new servingJob to the job that just arrived
    elif job.size < servingJob.rpt:
        # set place holder for prempted job's rpt
        servingJob.departureTime = float("inf")
        # update the prempted job's rpt to be the prempted deptime - the new job's arrival time
        servingJob.rpt = (servingJob.departureTime - job.arrivalTime)
        jobQueue.append(servingJob)
        # update which job is being serviced
        servingJob = job
        serverEmpty = False
        nextDepTime = clock + servingJob.size

    # generate next arrival
    interArrTime = generateInterarrivalTime()
    nextArrTime = clock + interArrTime


# fcn that handles a departure event
def handleDep():
    global clock, departures, serverEmpty, servingJob, nextDepTime, completionTimes
    # this sections deals with departing the current job
    # inc the counter
    departures += 1
    # set the departure time of the job that is currently departing
    servingJob.departureTime = clock + servingJob.rpt
    # append the total time spent in the system
    completionTimes.append(servingJob.departureTime - servingJob.arrivalTime)
    # these last 2 set up the next departure based on the status of the job queue
    # if the jobQueue is not empty, pop the next job off the queue
    if len(jobQueue) != 0:
        servingJob = jobQueue.pop()
        # set the next departure time of the job you just popped off the queue
        nextDepTime = clock + servingJob.rpt
    else:
        # if the server is empty, we are done with departures
        serverEmpty = True
        nextDepTime = float("inf")
        servingJob = None


# the following lines of code run the logic of the sim
seed = 0
maxDepartures = 5000
runCompletions = []

runs = 20000
for i in range(runs):
    np.random.seed(seed)

    departures = 0
    nextDepTime = float('inf')
    jobQueue = []
    completionTimes = []
    jobSizes = []

    serverEmpty = True

    nextArrTime = generateInterarrivalTime()
    clock = 0.0

    while departures <= maxDepartures:
        if nextArrTime <= nextDepTime:
            clock = nextArrTime
            handleArr()
        else:
            clock = nextDepTime
            handleDep()
    runCompletions.append(completionTimes.pop())
    seed += 1
print(len(runCompletions))

# print(sum(completionTimes) / len(completionTimes))
print(sum(jobSizes) / len(jobSizes))


with open("SRPT_LOAD_0.7.txt", "w") as fp:
    for item in runCompletions:
        fp.write("%s\n" % item)
