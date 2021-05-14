import random 
import time
import math
import itertools

# this function checks if two tasks are conflicting. It assumes L is sorted according to starting time
def is_conflict(L):
    for i in range(len(L)-1):
        if L[i][1] > L[i+1][0]: return True
    return False

# this function makes a random search for assignments
def random_search(L):
    vec_assignment = [0]*len(L)
    
    while True:         
        non_conflicting_tasks = []
        for i,el in enumerate(L):
            if vec_assignment[i] == 0:
                vec_assignment[i] = 1
                assignment = [L[k] for k in range(len(L)) if vec_assignment[k]==1 ]
                if not is_conflict(assignment):
                    non_conflicting_tasks.append(i)
                vec_assignment[i] = 0
                        
        if len(non_conflicting_tasks)==0:
            assignment = [L[k] for k in range(len(L)) if vec_assignment[k]==1 ]
            val = sum([k[2] for k in assignment])
            return (val,assignment)
        
        i = non_conflicting_tasks[random.randint(0,len(non_conflicting_tasks)-1)]
        vec_assignment[i] = 1        


    
# this function makes a brute force search for assignments
## need to create a list of all combinations of elements ##
## This is known as a powerset which contain all possible subset of
## list ##
def powerset(lst):
    subset_lst = []
    length = len(lst)
    for num in range(0,length + 1):
        for elem in itertools.combinations(lst,num):
            subset_lst.append(list(elem))

    return subset_lst

def check_conflict(lst):
    length = len(lst)
    for i in range(length - 1):
        for j in range(i + 1,length):
            if lst[j][0] >= lst[i][1]:
                continue
            else:
                return False

    return True 

def brute_force(L):
    # list of all possible schedules # 
    powerset_lst = powerset(L)

    # stores all schedules with no conficts #
    no_conflicts = []

    # iterate through powerset to eliminate schedules with
    # conflict
    for schedule in powerset_lst:
        clash = check_conflict(schedule)

        if clash:
            no_conflicts.append(schedule)
            continue
        
        ## there are conflicts ## 
        else:
            continue 

    # Find the schedule with the greatest benefit #
    length = len(no_conflicts) 
    max_benefit = -float('inf')
    idx = 0 
    for num in range(length): 
        schedule = no_conflicts[num]
        ## add up all benefits in schedule # 
        benefit = 0 
        for request in schedule: 
          benefit += request[-1] 
        
        if benefit > max_benefit:
            max_benefit = benefit
            idx = num

    best_schedule = no_conflicts[idx]

    return (max_benefit,best_schedule)

# this function makes a greedy force search for assignments
def is_clash(schedule,job):
    ## Assume that there is no conflict first ##
    conflict = False 
    for request in schedule:
        # check whether request is earlier or job is earlier #
        if request[0] <= job[0]:
            # clash will occur if end time of request is larger than
            # job starting time
            if request[1] > job[0]:
                conflict = True 
                break
            else:
                # No clash so far # 
                continue
        # request begins much later than job # 
        else:
            if job[1] > request[0]:
                conflict = True
                break
            else:
                continue

    return conflict 

def greedy(lst):
    ascending_order = sorted(lst,key = lambda k:k[2])
    descending_order = ascending_order[::-1]
    optimal_choice = []
    # First element is always in the optimal choice # 
    optimal_choice.append(descending_order.pop(0))

    for request in descending_order:
        ## Need to check that the request do not conflict
        ## with requests in optimal choice before adding
        conflict = is_clash(optimal_choice,request)

        if not conflict:
            optimal_choice.append(request)

        else:
            continue

    # compute the total benefit of optimal schedule #
    total_benefit = 0 
    length = len(optimal_choice)
    for num in range(length):
        request = optimal_choice[num]
        total_benefit += request[-1]

    return (total_benefit,optimal_choice) 


# this function makes a dynamic programing search for assignments
def dynamic_prog(L):
    length = len(L)
    table = [0] * length
    master_lst = [[]*length for num in range(length)]
    # double loop ensures that prev is always lesser than
    # curr by at least 1 
    for curr in range(length):
        previous_iteration = [] 
        for prev in range(curr):
            # check that there is no clash # 
            if L[curr][0] >= L[prev][1]:
                # check that we use the previous iteration
                # that gives the maximum benefit #
                if table[prev] > table[curr]:
                    table[curr] = table[prev]
                    previous_iteration = master_lst[prev].copy() 

        ## append current index to previous iteration ##
        previous_iteration.append(curr)
        ## update the master_lst ##
        master_lst[curr] = previous_iteration
        table[curr] += L[curr][-1]

    ## find the schedule that gives the largest benefit ##
    max_benefit = -float('inf')
    idx = 0 
    for num in range(length):
        benefit = table[num]
        if benefit > max_benefit:
            max_benefit = benefit
            idx = num
    
    optimal_choice = []

    for request in master_lst[idx]: 
      optimal_choice.append(L[request])


    return (max_benefit,optimal_choice) 
    
'''
example = [(0,6,60),(5,9,50),(1,4,30),(5,7,30),(3,5,10),(7,8,10)]
print(dynamic_prog(example))
test = [(185, 213, 92), (187, 331, 6), (275, 433, 98), (353, 438, 90), (368, 524, 69), (406, 493, 35), (440, 457, 41), (458, 561, 64), (477, 509, 19), (482, 530, 71)]
print(dynamic_prog(test))
'''

# this function prints the taskes
def print_tasks(L):
    for i,t in enumerate(L):
        print("task %2i (b=%2i):" %(i,t[2]),end="")
        print(" "*round(t[0]/10) + "-"*round((t[1]-t[0])/10))
        

# this function tests and times a telescope tasks assignment search
def test_telescope(algo,my_tab,display):
    tab = my_tab.copy()
    print("testing",algo,str(" "*(14-len(algo))),"... ",end='')
    t = time.time()
    (max_temp,assignment_temp) = eval(algo + "(tab)")
    print("done ! It took {:.2f} seconds".format(time.time() - t))
    if max_temp!=None:
        print("Solution with benefit = %i" %(max_temp),end='\n')
    if display: 
        if assignment_temp!=None:
            print_tasks(assignment_temp)
            print()
    

MAX_BENEFIT = 99
MAX_START_TIME = 500
MAX_DURATION = 250

NUMBER_OF_ELEMENTS = 10
print("\n ******** Testing to solve for %i events ********" %(NUMBER_OF_ELEMENTS))
val = [(random.randint(1, MAX_START_TIME),random.randint(1, MAX_DURATION),random.randint(1, MAX_BENEFIT)) for i in range(NUMBER_OF_ELEMENTS)] 
tab = sorted([(val[i][0],val[i][0]+val[i][1],val[i][2]) for i in range(NUMBER_OF_ELEMENTS)])
print("Problem instance: ")
print_tasks(tab)
print("")
test_telescope("random_search",tab,True)
test_telescope("brute_force",tab,True)
test_telescope("greedy",tab,True)
test_telescope("dynamic_prog",tab,True)


NUMBER_OF_ELEMENTS = 20
print("\n ******** Testing to solve for %i events ********" %(NUMBER_OF_ELEMENTS))
val = [(random.randint(1, MAX_START_TIME),random.randint(1, MAX_DURATION),random.randint(1, MAX_BENEFIT)) for i in range(NUMBER_OF_ELEMENTS)] 
tab = sorted([(val[i][0],val[i][0]+val[i][1],val[i][2]) for i in range(NUMBER_OF_ELEMENTS)])
test_telescope("random_search",tab,False)
test_telescope("brute_force",tab,False)
test_telescope("greedy",tab,False)
test_telescope("dynamic_prog",tab,False)

