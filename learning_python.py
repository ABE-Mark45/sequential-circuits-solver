import numpy as np


n_states = int(input('Enter the number of states: '))

if (n_states > 10):
   exit()


n_inputs = int(input('Enter the number of inputs: '))


'''
rows are states (0 to n_states)
columns are inputs

ex :
x=0 x=1
 0   1
 3   4
 6   8 

'''


next_states = np.zeros((n_states, n_inputs), dtype=np.uint8)
outputs = np.zeros((n_states, n_inputs), dtype=np.uint8)
print("States numbered 0 to " + str(n_states) + " has been created")


print("Fill state table")
for state in range (n_states):
    for inp in range (n_inputs):
        print(str(state) + " goes to what? when input is " + str(inp) + " :                     [states start from 0]")
        next_states[state, inp] = int(input());

print(next_states)


print("Fill output table")
for state in range (n_states):
    for inp in range (n_inputs):
        print(str(state) + " outputs what? when input is " + str(inp) + " :                     [states start from 0]")
        outputs[state, inp] = int(input());

print(outputs)



"""next_states = np.array
 [[4 4]
 [2 4]
 [8 7]
 [7 0]
 [8 5]
 [4 6]
 [7 1]
 [2 3]
 [5 1]]

outputs = np.array([[1 1]
 [1 1]
 [0 0]
 [1 1]
 [0 0]
 [0 0]
 [1 1]
 [0 0]
 [1 1]]"""


table = np.empty((n_states,  n_states), dtype=object)
for i in range (n_states):
    for j in range(n_states):
        table[i,j] = []


#different outputs iteration
for i in range (1, n_states):
    for j in range(i):
        #compare state i's and j's outputs
        for k in range(n_inputs):
            if outputs[i, k] != outputs[j, k]:
                #different outputs detected , mark it None
                table[i,j] = None
                table[j,i] = None
                break

# marking requirments iteration
for i in range(1, n_states):
    for j in range(i):
        if table[i, j] == None:
            continue

        # compare state i's and j's next states
        for k in range(n_inputs):
            if next_states[i, k] != next_states[j, k]:
                # different next state detected
                # print(table[i,j])
                table[i, j].append(str(next_states[i, k]) + str(next_states[j, k]))



for l in range(1000): #effecient yes yes
    #checking requirments iteration
    for i in range (1, n_states):
        for j in range(i):
            if table[i, j] == None:
                continue

            #loop over table[i, j] requirements and check if any is impossible
            for req in table[i, j]:
                if table[ int(req[0]), int(req[1]) ]  == None:
                    #found an impossible requirement
                    table[i, j] = None
                    table[j, i] = None

#print(table)

#declaring equivalnet states
for i in range(1, n_states):
    for j in range(i):
        if table[i, j] == None:
            continue
        print(str(i) + " and " + str(j) + " are equivalent")

print("ya")
