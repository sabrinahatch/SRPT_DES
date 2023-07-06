import numpy as np
import bisect
import sys

# Class to create job objects
class Job:
    def __init__(self, arrivalTime, size, rpt):
        self.arrivalTime = arrivalTime
        self.size = size
        self.departureTime = None
        self.rpt = rpt

# Function to generate job sizes
def generateJobSize():
    return np.random.exponential(1)

# Function that generates an interarrival time
def generateInterarrivalTime():
    return np.random.exponential(10 / 9)

# Function that handles an arrival event
def handleArr():
    global clock, serverEmpty, servingJob, nextArrTime, nextDepTime, completionTimes, jobSizes

    # Create the size of the job that just arrived
    size = generateJobSize()

    # Create a new job object with these new attributes
    job = Job(arrivalTime=clock, size=size, rpt=size)
    jobSizes.append(size)

    # # Update the preempted job's rpt to be the preempted departure time - the new job's arrival time
    # if servingJob != None and servingJob.departureTime != float('inf') and servingJob.departureTime != None:
    #     servingJob.rpt = (servingJob.departureTime - clock)
    # If the server is empty, immediately start servicing the new arrival
    if serverEmpty:
        # Immediately start servicing new job
        servingJob = job
        # Set this as the next departure time
        nextDepTime = clock + servingJob.size
        servingJob.departureTime = nextDepTime
        serverEmpty = False
    # If the new arrival has a larger size than the rpt of the job being serviced,
    # add it to the job queue and sort the list
    else:
        serverEmpty = False
        servingJob.rpt = (servingJob.departureTime - clock)
        if job.size >= servingJob.rpt:
            # Check increasing or decreasing order
            jobQueue.append(job)
            jobQueue.sort(key=lambda x: x.rpt)

        else:
            # Set placeholder for preempted job's rpt
            servingJob.departureTime = float("inf")
            jobQueue.append(servingJob)
            jobQueue.sort(key=lambda x: x.rpt)

            # Update which job is being serviced
            servingJob = job
            nextDepTime = clock + servingJob.size
            servingJob.departureTime = nextDepTime


    # # elif job.size >= servingJob.rpt: # if
    #     # Otherwise, append to the job queue
    #     bisect.insort(jobQueue, job.rpt)
    # # If the new arrival is smaller than the rpt of the job currently being serviced,
    # # change the departure time of servingJob, put that job back on the queue,
    # # and set the new servingJob to the job that just arrived
    # elif job.size < servingJob.rpt: #else
    #     # Set placeholder for preempted job's rpt
    #     servingJob.departureTime = float("inf")
    #     jobQueue.append(servingJob)
    #     # Update which job is being serviced
    #     servingJob = job
    #     nextDepTime = clock + servingJob.size

    # Generate next arrival
    nextArrTime = clock + generateInterarrivalTime()

# Function that handles a departure event
def handleDep():
    global clock, departures, serverEmpty, servingJob, nextDepTime, completionTimes

    # This section deals with departing the current job
    # Increment the counter
    servingJob.departureTime = clock
    departures += 1

    # Append the total time spent in the system
    if departures == maxDepartures:
        completionTimes.append(servingJob.departureTime - servingJob.arrivalTime)

    # These last two set up the next departure based on the status of the job queue
    # If the jobQueue is not empty, pop the next job off the queue
    if len(jobQueue) != 0:
        servingJob = jobQueue.pop()
        # Set the next departure time of the job you just popped off the queue
        nextDepTime = clock + servingJob.rpt
        servingJob.departureTime = nextDepTime
    else:
        # If the server is empty, we are done with departures
        serverEmpty = True
        nextDepTime = float("inf")
        servingJob = None

# The following lines of code run the logic of the simulation
seed = 0
maxDepartures = 20000
runCompletions = []
count = 0
runs = 5000
for i in range(runs):
    count += 1
    print("this is run " + str(count))
    np.random.seed(seed)

    departures = 0
    nextDepTime = float('inf')
    jobQueue = []
    completionTimes = []
    jobSizes = []
    servingJob = None
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

    if len(completionTimes) > 0:
        runCompletions.append(completionTimes[-1])  # Append the completion time of the last job to the list

    seed += 1

print("Average job size:", sum(jobSizes) / len(jobSizes))
print("Average completion time:", sum(completionTimes) / len(completionTimes))



with open("SRPT_LOAD_0.9.txt", "w") as fp:
    for item in runCompletions:
        fp.write("%s\n" % item)

