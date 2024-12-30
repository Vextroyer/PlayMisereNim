import subprocess
import random
from tkinter import *
from tkinter import messagebox

def Generate_Nim_Instance():
    n = random.randint(3,5)
    L = []
    for i in range(0,n):
        L.append(random.randint(1,100))
    return L

def Prepare_For_Nim(nim_instance):
    prepared_nim_instance = []
    for e in nim_instance:
        if e > 0:
            prepared_nim_instance.append(e)
    return prepared_nim_instance

def Play_Random(prepared_nim_instance):
    pos = random.randint(0,len(prepared_nim_instance) - 1)
    old = prepared_nim_instance[pos]
    new = random.randint(0,old - 1)
    return (old,new)

def Is_Winning_State(nim_instance):
    for e in nim_instance:
        if e != 0:
            return False
    return True

#Create UI

window = Tk()
window.title("Misere Nim")
window.geometry("480x360")

numberContainer = Frame(window,bd=5,relief=RAISED)
numberContainer.pack()

nim = Generate_Nim_Instance()
valuesVar = []
valuesLabel = []
for i in range(0,len(nim)):
    valuesVar.append(StringVar(value=nim[i]))
    valuesLabel.append(Label(numberContainer,textvariable=valuesVar[i]))
    valuesLabel[i].grid(row=1,column=i+1)


selectLabel = Label(window,text="Select a value to replace and a new value for it")
selectLabel.pack()
instructionContainer = Frame(window)
instructionContainer.pack()
oldEntryLabel = Label(instructionContainer,text="Old Value")
oldEntryLabel.grid(row=1,column=0)
oldEntry = Entry(instructionContainer,name="oldvalue")
oldEntry.grid(row=2,column=0)
oldEntryLabel = Label(instructionContainer,text="New Value")
oldEntryLabel.grid(row=1,column=1)
newEntry = Entry(instructionContainer,name="newvalue")
newEntry.grid(row=2,column=1)

def play():
    if Is_Winning_State(nim):
        messagebox.showinfo("Win","You win")
        exit(0)

    def error(message):
        messagebox.showerror("Error",message)

    try:
        oldValue = int(oldEntry.get())
    except ValueError:
        error("Old value must be a number")
        return
    try:
        newValue = int(newEntry.get())
    except ValueError:
        error("Old value must be a number")
        return

    if newValue >= oldValue:
        error("Old value must be less than New value")
        return
    
    if newValue < 0:
        error("New value must be non-negative")

    i = 0
    found = False
    while i < len(valuesVar):
        if valuesVar[i].get() == str(oldValue):
            valuesVar[i].set(str(newValue))
            nim[i] = newValue
            found = True
            break
        i = i + 1
    
    if not found:
        error("Old value not found on the board")
        return
    
    print(f"board after player {nim}")

    if Is_Winning_State(nim):
        messagebox.showinfo("Lose","You lose")
        exit(0)

    prepared_nim = Prepare_For_Nim(nim)

    print(f"prepared board {prepared_nim}")
    # Call prolog nim
    nim_execution = subprocess.run(["swipl","-s","nim.pl","-g",f"nim({prepared_nim},O,N),write(O),nl,write(N)","-t","halt"],capture_output=True,text=True)
    print(nim_execution)
    if nim_execution.returncode == 1:
        old,new = Play_Random(prepared_nim)
        print("Played Randomly")
    else:
        print("Played perfectly")
        tmp = nim_execution.stdout.splitlines()
        old = int(tmp[0])
        new = int(tmp[1])

    print(old,new)

    i = 0
    while i < len(valuesVar):
        if valuesVar[i].get() == str(old):
            valuesVar[i].set(str(new))
            nim[i] = new
            break
        i = i + 1
        
    computerMoveText.set(f"Computer turned {old} into {new}")    

button = Button(window,text="Play",command=play)
button.pack()

computerMoveText = StringVar(value="")
computerMoveLabel = Label(window,textvariable=computerMoveText)
computerMoveLabel.pack()

window.mainloop()