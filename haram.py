import numpy as np

cur_flip_flop = np.zeros((2, 2**3), dtype=object)
cur_flip_flop[0, 0] = (0, 0)


n_states = int(input('Enter the number of states: '))
n_inputs = int(input('Enter the number of inputs: '))
present_states = np.zeros((2**n_states, n_states), dtype=np.uint8)
next_states = np.zeros((n_inputs, 2**n_states, n_states), dtype=np.uint8)

print("Enter the present states: ")

for i in range(2**n_states):
    print(str(i) + ": ", end='')
    s = input()
    present_states[i] = np.array([int(s[x]) for x in range(n_states)])

print("Enter the next states: ")

for current_input in range(n_inputs):
    print("Enter the next state when input=" + str(bin(current_input)))
    for i in range(2**n_states):
        print(str(i) + ": ", end='')
        s = input()
        next_states[current_input, i] = np.array([int(s[x]) for x in range(n_states)])


FF_types = np.zeros((n_states,), dtype=np.uint8)

print("1. T Flip Flop")
print("2. D Flip Flop")
print("3. JK Flip Flop")
print("4. SR Flip Flop")

for i in range(n_states):
    print("Enter the type of flip flop for state Q" + str(n_states-i))
    FF_types[i] = int(input())

FF_Excitations = []

T_Flip_Flop_Excitation_Table = np.zeros((2, 2), dtype=object)
T_Flip_Flop_Excitation_Table[0, 0] = 0
T_Flip_Flop_Excitation_Table[0, 1] = 1
T_Flip_Flop_Excitation_Table[1, 0] = 1
T_Flip_Flop_Excitation_Table[1, 1] = 0

D_Flip_Flop_Excitation_Table = np.zeros((2, 2), dtype=object)
D_Flip_Flop_Excitation_Table[0, 0] = 0
D_Flip_Flop_Excitation_Table[0, 1] = 1
D_Flip_Flop_Excitation_Table[1, 0] = 0
D_Flip_Flop_Excitation_Table[1, 1] = 1

JK_Flip_Flop_Excitation_Table = np.zeros((2, 2), dtype=object)
JK_Flip_Flop_Excitation_Table[0, 0] = (0, 2)
JK_Flip_Flop_Excitation_Table[0, 1] = (1, 2)
JK_Flip_Flop_Excitation_Table[1, 0] = (2, 1)
JK_Flip_Flop_Excitation_Table[1, 1] = (2, 0)


SR_Flip_Flop_Excitation_Table = np.zeros((2, 2), dtype=object)
SR_Flip_Flop_Excitation_Table[0, 0] = (0, 2)
SR_Flip_Flop_Excitation_Table[0, 1] = (1, 0)
SR_Flip_Flop_Excitation_Table[1, 0] = (0, 1)
SR_Flip_Flop_Excitation_Table[1, 1] = (2, 0)


for cur_state in range(n_states):
    cur_flip_flop = np.zeros((n_inputs, 2**n_states), dtype=object)

    for current_input in range(n_inputs):
        for i in range(2**n_states):
            if FF_types[cur_state] == 1:
                cur_flip_flop[current_input, i] = T_Flip_Flop_Excitation_Table[present_states[i, cur_state], next_states[current_input, i, cur_state]]
            elif FF_types[cur_state] == 2:
                cur_flip_flop[current_input, i] = D_Flip_Flop_Excitation_Table[present_states[i, cur_state], next_states[current_input, i, cur_state]]
            elif FF_types[cur_state] == 3:
                cur_flip_flop[current_input, i] = JK_Flip_Flop_Excitation_Table[present_states[i, cur_state], next_states[current_input, i, cur_state]]
            elif FF_types[cur_state] == 4:
                cur_flip_flop[current_input, i] = SR_Flip_Flop_Excitation_Table[present_states[i, cur_state], next_states[current_input, i, cur_state]]

    FF_Excitations.append(cur_flip_flop)


print(FF_Excitations)