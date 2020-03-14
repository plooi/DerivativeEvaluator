from tkinter import *
import derivative_evaluator as de

def calculate():
    
    expression = entry.get()
    try:
        res = str(de.simplify(de.derive(de.parse(expression))))
    except:
        res = "???"
        
        
    if res == None or res == "None": res = "???"
    set_result(res)
def set_result(res):
    result.config(state="normal")
    result.delete(0,END)
    result.insert(0,res)
    result.config(state=DISABLED)
    return
def main():
    window.mainloop()




window = Tk()
window.geometry("1000x1000")
window.title("Derivative Evaluator")

window.grid_columnconfigure(0,weight=1)
window.grid_columnconfigure(2,weight=1)
window.grid_rowconfigure(4, minsize=60)
window.grid_rowconfigure(6, minsize=60)
window.grid_rowconfigure(1, minsize=60)

lbl = Label(text="Derivative Evaluator",font="Segoe_UI 30 bold")
lbl.grid(column=1, row=0)

lbl = Label(text="Enter expression",font="Segoe_UI 15")
lbl.grid(column=1, row=2)
#lbl.pack()

entry = Entry(wid = 35, font = "Segoe_UI 25")
entry.grid(column=1,row=3)
#entry.pack()

b = Button(text="Derive", command = calculate,wid = 25)
b.grid(column=1,row=5)
#b.pack()

lbl2 = Label(window, text="Derivative",font="Segoe_UI 15")
lbl2.grid(column=1, row=7)
#lbl2.pack()

result = Entry(wid = 35,font="Segoe_UI 25")
result.grid(column=1,row=8)
result.config(state=DISABLED)

instructions = Message(text = """
Guidelines
1. Put '*' in between all multiplications. So, '3x' becomes '3*x'
2. Cannot derive in respect to anything except x.
3. Allowed functions:
    ... + ...
    ... - ...
    ... * ...
    ... / ...
    sin(...)
    cos(...)
    tan(...)
4. Use x*x instead of x squared, x*x*x for x cubed, and so on
""")
instructions.grid(column=1, row=9)

    
if __name__ == "__main__": main()


