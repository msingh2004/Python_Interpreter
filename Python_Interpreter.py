lines = [] # initalise to empty list
with open('input_file.txt') as f:
    lines = f.readlines() # read all lines into a list of strings

import sys
BINARY_OPS = ['+', '-', '*', '/', '==', '!=', '>', '<', '>=', '<=', 'and', 'or']  #The list of binary operators
UNARY_OPS = ['-', 'not'] #The list of unary operators
 
opcodes = ['BE', 'BLE', 'BLT']         
DATA = []            
INSTRUCTIONS = []

#I have used None to describe the value of the branch destination when there is no branching point and to symbolize the opcode when there is no opcode.

#I have handled the exception cases when the loop body of the while is not properly indented and when there is a non boolean expression in the while statement
#For the first case, we can just check after each loop statement, whether the next statement has a higher number of tabs or not and the second is easily checked by the operator in the expression


def print_all(DATA):
    #To print the values of all variables
    #Input: the DATA list
    #Output: a list containing the variables and the values they refer to
    l = []
    for i in range(len(DATA)): #Iterating through DATA list
        if isinstance(DATA[i], tuple): #Looking at only the tuples, and going to the address pointed to by the variable
            l.append(DATA[i][0] + ' : ' + str(DATA[DATA[i][1]]))
    return l 

def print_garbage(DATA): #Creating the garbage list
    #Input: DATA list
    #Output: the garbage list
    garbage = []
    for i in range(len(DATA)):
        if not isinstance(DATA[i], tuple):
            #Not looking at the tuples
            bool_found = False
            for j in range(len(DATA)):
                if isinstance(DATA[j], tuple) and DATA[j][1] == i:
                    #We found a variable referring to DATA[i], so it wont be in garbage
                    bool_found = True
            if not bool_found:
                garbage.append(DATA[i]) #Appending garbage
    return garbage
                    

        
def var_string(variable):
    #Input: Takes a list variable
    #Output: Returns the variable converted to a string
    empty_string = ''
    for character in variable:
        empty_string = empty_string + character  #As we are iterating through the whole list, the time complexity is O(len(variable))
    return empty_string

def token_check(token_list): #Checking whether the statement has atleast one assignment operator if it is non empty
    if len(token_list) != 0 and not('=' in token_list): #Time complexity is O(len(token_list)) as '=' in token_list will take O(len(token_list)) time in worst case
        sys.exit("SyntaxError: Statement should have atleast one assignment operator")

def is_variable(variable_string):#Time Complexity is O(len(variable_string))
    #Input: a string
    #Output: boolean value indicating if it is a possible variable name
        return variable_string.isalpha() and (variable_string != 'True') and (variable_string != 'False')

    
def is_term(x): #Time Complexity is O(len(x))
    #Input: a string x
    #Output: True is x is a valid term, False otherwise
    if x.isnumeric():
        return True
    elif x == 'True' or x == 'False':
        return True
    else:
        return is_variable(x)
     
def expression_check_out(expression):  #Checking for syntactic errors in the expression
        #Input: a list expression
        #Time complexity is O(1) as all checks involved are with lists of constant length
    if len(expression) > 3 or len(expression) == 0: 
        sys.exit("SyntaxError: Invalid Expression")
    elif '=' in expression:
        sys.exit("SyntaxError: Invalid Expression: Statement can have only one assignment operator")
    elif len(expression) == 1:
        if not is_term(expression[0]):
            sys.exit("SyntaxError: Invalid Expression")
    elif len(expression) == 2:
        if not(expression[0] in UNARY_OPS): #this should be the unary operator case
            sys.exit("SyntaxError: Invalid Expression")
        else:
            if not is_term(expression[1]):
                sys.exit("SyntaxError: Invalid Expression")
    elif len(expression) == 3:
        if not (expression[1] in BINARY_OPS): #this should be the binary operator case
            sys.exit("SyntaxError: Invalid Expression, incorrect operator")
        else:
            if (not is_term(expression[0])) or (not is_term(expression[2])):
                sys.exit("SyntaxError: Invalid Expression")


def variable_check_out(variable):  #Checking for syntactic errors in variable
    if len(variable) != 1:
        sys.exit("SyntaxError: Variable is not correct")
    else:
        for i in range(len(variable)): #Time Complexity is O(len(variable)) as we have to iterate through the entire variable list
            if not variable[i].isalpha():
                sys.exit("SyntaxError: Invalid variable name(We have only considered variables to be sequence of letters as given in assignment)")
         
def search_value(val):
    #Input: a value val(maybe an integer or a boolean)
    #Output: A tuple, with first element indicating whether val was found in the DATA list or not, if the first element is True then the second denotes the address in the DATA list 
    for i in range(len(DATA)): #Time Complexity is O(len(DATA)) in the worst case
        if DATA[i] is val:
            return True, i #returning the index as well
    return False, 0

def search_variable(variable):
    #Input: A string representing the variable
    #Output: A tuple, with first element indicating whether variable was found in the DATA list or not, if the first element is True then the second denotes the address in the DATA list 
    for i in range(len(DATA)): #Time complexity is O(len(DATA)) in the worst case
        if isinstance(DATA[i], tuple) and DATA[i][0] == var_string(variable): #and executes the second statement only when the first is True, so this does not cause any errors
            return True, i
    return False, 0

def type_cast(x):  # Function to convert the string x to its appropriate type, time complexity is O(len(x)), to check isnumeric().
    if x.isnumeric():  #isnumeric returns true if x is a number
        return int(x)
    elif x == 'True': #Boolean values can only be True or False
        return True
    elif x == 'False':
        return False
    else:
        return x

def is_OP(x):  #Whether x is an operator or not
    #Time Complexity is O(1) as BINARY_OPS and UNARY_OPS are constant lists
    #Input: a string x representing an operator
    #Output: True if x is an operator, False if x is not an operator
    #Time complexity is O(1) as BINARY_OPS and UNARY_OPS are of fixed length
    for i in range(len(BINARY_OPS)):
        if BINARY_OPS[i] == x:
            return True
    for j in range(len(UNARY_OPS)):
        if UNARY_OPS[j] == x:
            return True
    return False

    
def stringify_expression(expression):
        #Input: a list expression
        #Output: Converting it to a string with spaces in between
        #Time complexity is O(len(expression)), this can also be written as O(1) as len(expression) <= 3
    empty_string = ''
    for character in expression:
        empty_string = empty_string + ' ' + character #adding spaces as well to use in eval function
    return empty_string

def div_0_check(expression): #checking for division by 0
    #Input: a list expression
        #Time complexity is O(1)
    if len(expression) == 3:
        if expression[1] == '//' and expression[2] == '0':
            sys.exit("Division by 0 error")





            

class Instruction:
    #The attributes for the instruction class are the tab count, the opcode(BLT, BLE, BE or Branch), the token_list of that statement to execute and the branching destination if any
    def __init__(self, tabs, opcode, token_list, branch):
        self.tabs = tabs
        self.opcode = opcode
        self.token_list = token_list
        self.branch = branch
        
    def __str__(self):
        if self.opcode is None:
            return stringify_expression(self.token_list)
        elif self.opcode == 'Branch':
            return 'Branch' + ' ' + str(self.branch)
        else:
            return str(self.opcode) + ' ' + str(self.token_list) + ' ' + str(self.branch)

    def __repr__(self): #Used to get the output in a single line
        if self.opcode is None:
            return stringify_expression(self.token_list)
        elif self.opcode == 'Branch':
            return 'Branch' + ' ' + str(self.branch)
        else:
            return str(self.opcode) + ' ' + str(self.token_list) + ' ' + str(self.branch)


    
    def execute(self): #Using code of assignment 5a to execute an instruction
        l = self.token_list.copy() #creating a copy, so that the token_list is unchanged because we have to come back to it again
        if True:
            token_check(l) #implementing the check
            
            for i in range(len(l)):
                if l[i] == "=":
                    variable = l[0:i] #separating the variable and expression parts at the first '='
                    expression = l[i+1:]
                    break
            self.expression_check(expression)#implementing expression and variable checks
            self.variable_check(variable)
            
            for i in range(len(expression)): #Iterating through the expression list
                item = expression[i]
                if not is_OP(item): #If item is a term
                    item = type_cast(item)
                    if type(item) == str:
                        (item_DATA, address) = search_variable(item)
                        if not item_DATA:
                            sys.exit("Variable " + item + " not defined") #item is a previously undefined variable
                        else:
                            expression[i] = str(DATA[DATA[address][1]])  #If it is defined previously, replacing its value in the expression list
                    else:
                        (item_DATA, address) = search_value(item)
                        if not item_DATA:
                            DATA.append(item) #If previously undefined object like integer or boolean, append it to DATA
                if item == '/':
                    expression[1] = '//' #As we have to keep integer values, we use integer division

            
            div_0_check(expression)
            
            variable_string = var_string(variable) #converting list to string
            
            val_expression = eval(stringify_expression(expression))  #Using eval to evaluate the expression, time complexity is O(1) as expression is of bounded length
            
            (val_expression_DATA, address_val) = search_value(val_expression)  #Check if this value is present in DATA
            
            (variable_DATA, address_variable) = search_variable(variable_string) #Check if variable is present in DATA

            if val_expression_DATA and (not variable_DATA):
                #expression found in DATA but variable not found
                DATA.append((variable_string, address_val))

            elif (not val_expression_DATA) and variable_DATA:
                #Variable found in DATA, but expression not found in data
                DATA.append(val_expression)
                address_new = len(DATA) - 1
                DATA[address_variable] = (variable_string, address_new)
            elif not val_expression_DATA and not variable_DATA:
                #Both expression and variable not found in DATA
                DATA.append(val_expression)
                address_new = len(DATA) - 1
                DATA.append((variable_string, address_new))
            else:
                #Both expression and variable are in DATA
                DATA[address_variable] = (variable_string, address_val)

    def expression_check(self, expression):  #Checking for syntactic errors in the expression

        #Time complexity is O(1) as all checks involved are with lists of constant length
        if len(expression) > 3 or len(expression) == 0: 
            sys.exit("SyntaxError: Invalid Expression")
        elif '=' in expression:
            sys.exit("SyntaxError: Invalid Expression: Statement can have only one assignment operator")
        elif len(expression) == 1:
            if not is_term(expression[0]):
                sys.exit("SyntaxError: Invalid Expression")
        elif len(expression) == 2:
            if not(expression[0] in UNARY_OPS): #this should be the unary operator case
                sys.exit("SyntaxError: Invalid Expression")
            else:
                if not is_term(expression[1]):
                    sys.exit("SyntaxError: Invalid Expression")
        elif len(expression) == 3:
            if not (expression[1] in BINARY_OPS): #this should be the binary operator case
                sys.exit("SyntaxError: Invalid Expression, incorrect operator")
            else:
                if (not is_term(expression[0])) or (not is_term(expression[2])):
                    sys.exit("SyntaxError: Invalid Expression")


    def variable_check(self, variable):#Checking for syntactic errors in variable
        #Input: the variable list
        if len(variable) != 1:
            sys.exit("SyntaxError: Variable is not correct")
        else:
            for i in range(len(variable)): #Time Complexity is O(len(variable)) as we have to iterate through the entire variable list
                if not variable[i].isalpha():
                    sys.exit("SyntaxError: Invalid variable name(We have only considered variables to be sequence of letters as given in assignment)")
            

    def evaluate_expression(self):
        #Output: the boolean value True or False, guiding the branching statement of the while
        #To be used to check the condition in case of BLE, BLT
        if self.opcode == 'BLE' or self.opcode == 'BLT' or self.opcode == 'BE':
            x = self.token_list[0]
            y = self.token_list[len(self.token_list) - 1]
            x_new = type_cast(x)
            y_new = type_cast(y)
            #Using type_cast to correct the type of the string
            if type(x_new) == str:
                (item_DATA_x, address_x) = search_variable(x_new)
                if not item_DATA_x:
                    sys.exit('Variable ' + x_new + ' not defined')
                x_new = DATA[DATA[address_x][1]]
            else:
                (item_DATA_x, address_x) = search_value(x_new)
                if not item_DATA_x:
                    DATA.append(x_new)
            if type(y_new) == str:
                (item_DATA_y, address_y) = search_variable(y_new)
                if not item_DATA_y:
                    sys.exit('Variable ' + y_new + ' not defined')
                y_new = DATA[DATA[address_y][1]]
            else:
                (item_DATA_y, address_y) = search_value(y_new)
                if not item_DATA_y:
                    DATA.append(y_new)

            
            if self.opcode == 'BE':
                if self.token_list[1] == '==':
                    return (x_new != y_new)
                else:
                    return (x_new == y_new)
            elif self.opcode == 'BLE':
                return (x_new <= y_new)
            elif self.opcode == 'BLT':
                return (x_new < y_new)
        
        

            
#Now we set up the instruction list

for stat_count in range(len(lines)):
    statement = lines[stat_count]
    tabs = 0
    while statement[tabs] == '\t':
        tabs += 1

    token_list = statement.split()
    n = len(token_list)

    if n == 0:
        continue #Ignoring the blank statements

    else:
        if token_list[0] == 'while':
            #Encountering a while loop
            expression = token_list[1: n - 1]
            expression_check_out(expression) #Checking the expression in while for syntactical errors
            #Adding the appropriate opcode based on the expression
            if expression[1] == '==' or expression[1] == '!=':
                opcode = 'BE'
                instr = Instruction(tabs, opcode, (expression[0], expression[1], expression[2]), None)
            elif expression[1] == '>=':
                opcode = 'BLT'
                instr = Instruction(tabs, opcode, (expression[0], expression[2]), None)
            elif expression[1] == '<=':
                opcode = 'BLT'
                instr = Instruction(tabs, opcode, (expression[2], expression[0]), None)
            elif expression[1] == '>':
                opcode = 'BLE'
                instr = Instruction(tabs, opcode, (expression[0], expression[2]), None)
            elif expression[1] == '<':
                opcode = 'BLE'
                instr = Instruction(tabs, opcode, (expression[2], expression[0]), None)
            elif expression[1] == '+' or expression[1] == '-' or expression[1] == '/' or expression[1] == '*':
                sys.exit('SyntaxError: Expression in while must of boolean type')
            INSTRUCTIONS.append(instr)
            

        else:
            instr = Instruction(tabs, None, token_list, None)
            INSTRUCTIONS.append(instr)


for statement_number in range(len(INSTRUCTIONS)): #Checking the code for improper indentation
    instr_check = INSTRUCTIONS[statement_number]
    if instr_check.opcode in opcodes:
        if statement_number == len(INSTRUCTIONS) or instr_check.tabs != INSTRUCTIONS[statement_number + 1].tabs - 1:
            sys.exit('SyntaxError: Improper Indent')

            
#Now we start setting up the branches, first look at the statements where we need to place unconditional branches
stat_count = 0
while stat_count < len(INSTRUCTIONS):
    instr = INSTRUCTIONS[stat_count]
    #print('setting branch for', instr)
    #print(stat_count, len(INSTRUCTIONS))
    if instr.token_list == []:
        stat_count = stat_count + 1
        continue
    else:
        if stat_count == len(INSTRUCTIONS) - 1 and  instr.tabs != 0:#reaching the end of the program
            #print('something')
            for j in range(stat_count, -1, -1):
                if INSTRUCTIONS[j].tabs == instr.tabs - 1 and INSTRUCTIONS[j].opcode in opcodes:
                    #we found the correct loop
                    instr_new = Instruction(instr.tabs, 'Branch', [], j)
                    INSTRUCTIONS.append(instr_new)
                    break

        elif stat_count == len(INSTRUCTIONS) - 1 and instr.tabs == 0:
            stat_count = stat_count + 1
            continue
        else:
            #Not the end of the program
            #print('going the wrong way')
            if INSTRUCTIONS[stat_count + 1].tabs < instr.tabs:
                #The last indented line, instr needs to branch to the previous while loop
                for j in range(stat_count, -1, -1):
                    if INSTRUCTIONS[j].opcode in opcodes and INSTRUCTIONS[j].tabs == instr.tabs - 1:
                        instr_new = Instruction(instr.tabs, 'Branch', [], j)
                        INSTRUCTIONS.insert(stat_count + 1, instr_new)
                        break
            else:
                stat_count = stat_count + 1
                continue
    stat_count = stat_count + 1


#setting appropriate branches for while statements
for stat_count in range(len(INSTRUCTIONS)):
    #print('went into this for loop')
    instr = INSTRUCTIONS[stat_count]
    if instr.token_list == []:
        continue #skipping unconditional branch statements
    
    if instr.opcode in opcodes: #While loop
        bool_found = False
        for j in range(stat_count+1, len(INSTRUCTIONS)):
            if INSTRUCTIONS[j].tabs == instr.tabs:
                #We found a statement with same indent level as that of while
                instr.branch = j
                bool_found = True
                break
        if not bool_found and instr.tabs != 0:
            #No statement with same indent level
            for j in range(stat_count, -1, -1):
                if INSTRUCTIONS[j].opcode in opcodes and INSTRUCTIONS[j].tabs == instr.tabs - 1:
                    instr.branch = j
                    break
        elif not bool_found and instr.tabs == 0: #The while loop has nothing to branch to
            instr.branch = -1
        

print(INSTRUCTIONS)

#Now we start executing the instruction list

prog_length = len(INSTRUCTIONS)
               
prog_count = 0
while prog_count < prog_length and prog_count != -1: #If prog_count == -1, we exit
    instr = INSTRUCTIONS[prog_count]
    if len(instr.token_list) != 0:
        if instr.opcode is None:
            instr.execute() #executing normal statements
            prog_count = prog_count + 1
            
        elif instr.opcode in opcodes: # a while loop
            if instr.evaluate_expression(): #evaluating the branch condition(if true then branch)
                prog_count = instr.branch
            else:
                #If false then simply continue to next statement
                prog_count = prog_count + 1

    else:
        #The statement with an empty token_list is one which has unconditional branch statement
        prog_count = instr.branch #Move to branch
        print(stringify_expression(print_all(DATA))) #Whenever we encounter unconditional branch, it means that the iteration is complete, so we print the variables and garbage list
        print(print_garbage(DATA))

print(stringify_expression(print_all(DATA))) #printing variables after completion
print(print_garbage(DATA)) #printing garbage list after completion



'''
Input:
a = 10
b = 1
while a > b :
    a = a - 1
c = 1

Output:
[ a = 10,  b = 1, BLE ('a', 'b') 5,  a = a - 1, Branch 2,  c = 1]
 a : 9 b : 1
[10]
 a : 8 b : 1
[10, 9]
 a : 7 b : 1
[10, 9, 8]
 a : 6 b : 1
[10, 9, 8, 7]
 a : 5 b : 1
[10, 9, 8, 7, 6]
 a : 4 b : 1
[10, 9, 8, 7, 6, 5]
 a : 3 b : 1
[10, 9, 8, 7, 6, 5, 4]
 a : 2 b : 1
[10, 9, 8, 7, 6, 5, 4, 3]
 a : 1 b : 1
[10, 9, 8, 7, 6, 5, 4, 3, 2]
 a : 1 b : 1 c : 1
[10, 9, 8, 7, 6, 5, 4, 3, 2]
DATA = [10, ('a', 2), 1, ('b', 2), 9, 8, 7, 6, 5, 4, 3, 2, ('c', 2)]


The time complexity of my program(to set up the instruction list) will be O(m^2) where m is the number of lines in the input program, because in the worst case we have to check each statement of the input to find
the corresponding while loop to branch too and similarly to find the appropriate branching point of the while loop.

The time complexity of execution will depend on the input program but we can say that it will be atleast O(n^2) where n is the number of elements in the DATA list(because we will have to search the entire data list
to print garbage list).


'''

'''
Input:
i = 1
n = 1
while i < 5 :
    n = n * i
    i = i + 1

Output:
[ i = 1,  n = 1, BLE ('5', 'i') -1,  n = n * i,  i = i + 1, Branch 2]
 i : 2 n : 1
[5]
 i : 3 n : 2
[1, 5]
 i : 4 n : 6
[1, 5, 2, 3]
 i : 5 n : 24
[1, 2, 3, 6, 4]
 i : 5 n : 24
[1, 2, 3, 6, 4]
DATA = [1, ('i', 3), ('n', 8), 5, 2, 3, 6, 4, 24]

The time complexity of my program(to set up the instruction list) will be O(m^2) where m is the number of lines in the input program, because in the worst case we have to check each statement of the input to find
the corresponding while loop to branch too and similarly to find the appropriate branching point of the while loop.

The time complexity of execution will depend on the input program but we can say that it will be atleast O(n^2) where n is the number of elements in the DATA list(because we will have to search the entire data list
to print garbage list).
'''

