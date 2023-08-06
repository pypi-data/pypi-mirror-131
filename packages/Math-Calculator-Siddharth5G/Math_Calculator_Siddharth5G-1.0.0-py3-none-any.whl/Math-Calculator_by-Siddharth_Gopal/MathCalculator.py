def reset_No(c): 
     b = float(input('Type your second number__'))
     operator = input('Type your operator__')
     print("I am here")
     if(operator == '+'):
        c = c + b
        print(c)
     if(operator == '-'):
        c = c - b
        print(c)
     if(operator == 'x' or operator == 'X'):
        c = c * b
        print(c)
     if(operator == '/'):
        c = c / b
        print(c)
     if(operator == '*'):
        c = c ** b
        print(c)
     if(operator == '//'):
        c = c // b
        print(c)
     if(operator == '%'):
        c = c % b
        print(c)
     contin = input('quit?__')
     if(contin == 'yes'):
        print('quitting...')
        exit()
     elif(contin == 'no'):
       reset = input('Reset calculator?__')
     if reset == 'yes':
        reset_Yes()
     if reset == 'no':
        reset_No(c) 

def reset_Yes():
     print('resetting...')
     a = float(input('Type your first number__'))
     b = float(input('Type your second number__'))
     operator = input('Type your operator__')
     if(operator == '+'):
        c = a + b
        print(c)
     if(operator == '-'):
        c = a - b
        print(c)
     if(operator == 'x' or operator == 'X'):
        c = a * b
        print(c)
     if(operator == '/'):
        c = a / b
        print(c)
     if(operator == '*'):
        c = a ** b
        print(c)
     if(operator == '//'):
        c = a // b
        print(c)
     if(operator == '%'):
        c = a % b
        print(c)

     contin = input('quit?__')
     if(contin == 'yes'):
        print('quitting...')
        exit()
     elif(contin == 'no'):
        reset = input('Reset calculator?__')
     if reset == 'yes':
        reset_Yes()
     if reset == 'no':
        reset_No(c) 

print('Hello!, This is a Math Calculator:')
a = float(input('Type your first number__'))
b = float(input('Type your second number__'))
operator = input('Type your operator__')
# global c
if(operator == '+'):
    c = a + b
    print(c)
if(operator == '-'):
    c = a - b
    print(c)
if(operator == 'x' or operator == 'X'):
    c = a * b
    print(c)
if(operator == '/'):
    c = a / b
    print(c)
if(operator == '*'):
    c = a ** b
    print(c)
if(operator == '//'):
    c = a // b
    print(c)
if(operator == '%'):
    c = a % b
    print(c)
contin = input('quit?__')
if(contin == 'yes'):
     print('quitting...')
     exit()
elif(contin == 'no'):
       reset = input('Reset calculator?__')
       if reset == 'yes':
          reset_Yes()
       if reset == 'no':
          reset_No(c)

        
