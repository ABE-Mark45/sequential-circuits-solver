import numpy as np
import xlwt

workbook = xlwt.Workbook()

styles = [xlwt.easyxf("align: vert centre, horiz centre;pattern: pattern solid, fore_colour red"),
          xlwt.easyxf("align: vert centre, horiz centre;pattern: pattern solid, fore_colour light_green"),
          xlwt.easyxf("align: vert centre, horiz centre;font: bold 1")]

n_states = int(input('Enter the number of states: '))
n_inputs = int(input('Enter the number of inputs: '))
present_states = np.zeros((2**n_states, n_states), dtype=np.uint8)
next_states = np.zeros((2**n_inputs, 2**n_states, n_states), dtype=np.uint8)

state_names = []
print("Enter states names (starting from MSB): ")
for i in range(n_states):
    state_names.append(input("Bit " + str(n_states - i) + ": "))

input_name = 'X' if n_inputs == 1 else 'XY'
#print("Enter the present states: ")

for i in range(2**n_states):
    s = format(i, '0'+str(n_states)+'b')
    present_states[i] = np.array([int(s[x]) for x in range(n_states)])

print("Enter the next states: ")

for current_input in range(2**n_inputs):
    print("Enter the next state when " + input_name + "=" + format(current_input, '0'+str(n_inputs)+'b'))
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
    print("Enter the type of flip flop for state " + state_names[i])
    FF_types[i] = int(input())

FF_Excitations = []

T_Flip_Flop_Excitation_Table = np.zeros((2, 3), dtype=object)
T_Flip_Flop_Excitation_Table[0, 0] = 0
T_Flip_Flop_Excitation_Table[0, 1] = 1
T_Flip_Flop_Excitation_Table[1, 0] = 1
T_Flip_Flop_Excitation_Table[1, 1] = 0
T_Flip_Flop_Excitation_Table[0, 2] = 2
T_Flip_Flop_Excitation_Table[1, 2] = 2

D_Flip_Flop_Excitation_Table = np.zeros((2, 3), dtype=object)
D_Flip_Flop_Excitation_Table[0, 0] = 0
D_Flip_Flop_Excitation_Table[0, 1] = 1
D_Flip_Flop_Excitation_Table[1, 0] = 0
D_Flip_Flop_Excitation_Table[1, 1] = 1
D_Flip_Flop_Excitation_Table[0, 2] = 2
D_Flip_Flop_Excitation_Table[1, 2] = 2


JK_Flip_Flop_Excitation_Table = np.zeros((2, 3), dtype=object)
JK_Flip_Flop_Excitation_Table[0, 0] = (0, 2)
JK_Flip_Flop_Excitation_Table[0, 1] = (1, 2)
JK_Flip_Flop_Excitation_Table[1, 0] = (2, 1)
JK_Flip_Flop_Excitation_Table[1, 1] = (2, 0)
JK_Flip_Flop_Excitation_Table[0, 2] = (2, 2)
JK_Flip_Flop_Excitation_Table[1, 2] = (2, 2)


SR_Flip_Flop_Excitation_Table = np.zeros((2, 3), dtype=object)
SR_Flip_Flop_Excitation_Table[0, 0] = (0, 2)
SR_Flip_Flop_Excitation_Table[0, 1] = (1, 0)
SR_Flip_Flop_Excitation_Table[1, 0] = (0, 1)
SR_Flip_Flop_Excitation_Table[1, 1] = (2, 0)
SR_Flip_Flop_Excitation_Table[0, 2] = (2, 2)
SR_Flip_Flop_Excitation_Table[1, 2] = (2, 2)


for cur_state in range(n_states):
    cur_flip_flop = np.zeros((2**n_inputs, 2**n_states), dtype=object)

    for current_input in range(2**n_inputs):
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

FF_Excitations = np.array(FF_Excitations)
sheet = workbook.add_sheet("Solution")

sheet.write(0, 1, "Present State", styles[2])
sheet.write(0, n_states+1, "Next State", styles[2])


#state_names = ['Q3', 'Q2', 'Q1']
FF_names = ["", 'T', 'D', 'JK', 'SR']
for i in range(n_states):
    sheet.write(2, i, state_names[i], styles[2])

for current_input in range(2**n_inputs):
    sheet.write(1, (current_input+1)*n_states, input_name+"=" + format(current_input, '02b'), styles[2])
    for cur_state in range(n_states):
        sheet.write(2, (current_input+1)*n_states+cur_state, state_names[cur_state] + "+", styles[2])

for row in range(2**n_states):
    for col in range(n_states):
        num = int(present_states[row, col])
        sheet.write(3+row, col, num if num != 2 else 'X', styles[num])

for current_input in range(2**n_inputs):
    for row in range(2**n_states):
        for col in range(n_states):
            num = int(next_states[current_input, row, col])
            sheet.write(3+row, (current_input+1)*n_states + col, num if num != 2 else 'X', styles[num])


last_column = n_states + n_states * 2**n_inputs

for current_ff in range(len(FF_Excitations)):
    if FF_types[current_ff] <= 2:
        sheet.write(1, last_column, FF_names[FF_types[current_ff]], styles[2])
        for current_input in range(2**n_inputs):
            sheet.write(2, last_column, input_name+"="+format(current_input, '0'+str(n_inputs)+'b'), styles[2])
            for row in range(3, 3+2**n_states):
                num = FF_Excitations[current_ff, current_input, row-3]
                sheet.write(row, last_column,num if num != 2 else 'X', styles[num])
            last_column += 1
    else:
        for current_input in range(2 ** n_inputs):
            sheet.write(2, last_column, FF_names[FF_types[current_ff]][0], styles[2])
            sheet.write(2, last_column + 1, FF_names[FF_types[current_ff]][1], styles[2])
            sheet.write(1, last_column, input_name+"=" + format(current_input, '0'+str(n_inputs)+'b'), styles[2])
            for channel in range(2):
                for row in range(3, 3 + 2 ** n_states):
                    num = FF_Excitations[current_ff, current_input, row - 3][channel]
                    sheet.write(row, last_column, num if num != 2 else 'X', styles[num])
                last_column += 1
workbook.save("sol.xls")
print(FF_Excitations)
