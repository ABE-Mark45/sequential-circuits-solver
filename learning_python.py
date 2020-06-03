import numpy as np

# map states names' to index and vice versa
state_index = {}
state_name = {}

n_states = int(input('Enter the number of states: '))
n_inputs = int(input('Enter the number of inputs: '))
n_outputs = int(input('Enter the number of outputs: '))

next_states = np.zeros((n_states, n_inputs))
outputs = np.zeros((n_states, n_inputs, n_outputs))


def name_array(row):
    return list(map(name_element, row))


def name_element(element):
    return state_name[element]


def main():
    """
    rows are states (0 to n_states)
    columns are inputs

    ex :
    x=0 x=1
     0   1
     3   4
     6   8
    """

    print("Fill state names column")
    for index in range(n_states):
        inp = input()
        state_index[inp] = index
        state_name[index] = inp

    state_index['-'] = -1
    state_name[-1] = '-'

    print("Fill state table")
    for state in range(n_states):
        for inp in range(n_inputs):
            print(str(state_name[state]) + " goes to what? when input is " + str(inp) + "    enter '-' for unspecified")

            next_states[state, inp] = state_index[input()]
    print(np.array(list(map(name_array, next_states))))

    print("enter '-' for unspecified")
    print("Fill output table")
    for state in range(n_states):
        for inp in range(n_inputs):
            for out in range(n_outputs):

                print(str(state_name[state]) + ", input: " + str(inp) + ", output :" + str(out))
                s = input()
                if s == '-':
                    outputs[state, inp, out] = -1
                else:
                    outputs[state, inp, out] = int(s)
    print(outputs)

    # edit cells
    print("Edit cells, enter e to end edit")
    while True:
        print("Enter 0 for next state table, 1 for outputs table")
        s = input()
        if s == 'e':
            break

        row = input("present state:")
        inp = int(input("input number:"))

        if int(s) == 0:
            new_state = input("new next state :")
            next_states[state_index[row], inp] = state_index[new_state]
            print(np.array(list(map(name_array, next_states))))
        else:
            out = int(input("output number: "))
            new_out = input("new output value:")
            if new_out == '-':
                new_out = -1
            else:
                new_out = int(new_out)
            outputs[state_index[row], inp, out] = new_out
            print(outputs)

    # implication table
    table = np.empty((n_states, n_states), dtype=object)

    # initiate all cells with empty lists
    for i in range(n_states):
        for j in range(n_states):
            table[i, j] = []

    # "mark different outputs" iteration
    for i in range(1, n_states):
        for j in range(i):
            # compare state i's and j's outputs
            for k in range(n_inputs):
                for l in range(n_outputs):
                    if outputs[i, k, l] == -1 or outputs[j, k, l] == -1:
                        continue

                    if outputs[i, k, l] != outputs[j, k, l]:
                        # different outputs detected , mark it None
                        table[i, j] = None
                        table[j, i] = None
                        break

    # "marking requirements" iteration
    for i in range(1, n_states):
        for j in range(i):
            if table[i, j] is None:
                continue

            # compare state i's and j's next states
            for k in range(n_inputs):
                if next_states[i, k] == -1 or next_states[j, k] == -1:
                    continue

                if next_states[i, k] != next_states[j, k]:
                    # different next state detected, add to its list in the table
                    table[i, j].append((next_states[i, k], next_states[j, k]))

    for l in range(1000):  # efficient yes yes
        # "checking requirements" iteration
        for i in range(1, n_states):
            for j in range(i):
                if table[i, j] is None:
                    continue

                # loop over table[i, j] requirements and check if any is impossible
                for req in table[i, j]:
                    if table[int(req[0]), int(req[1])] is None:
                        # found an impossible requirement
                        table[i, j] = None
                        table[j, i] = None

    # declaring equivalent states
    for i in range(1, n_states):
        for j in range(i):
            if table[i, j] is None:
                continue
            print(state_name[i] + " and " + state_name[j] + " are equivalent")

    print("ya")


main()
