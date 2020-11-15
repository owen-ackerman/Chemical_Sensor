from tkinter import *
import tkinter.scrolledtext as st 
state = False
list = [404, 404]

def scanning():
    if state:  # If start button was clicked
        print("STATE TRUE")
    # After 1 second, call scanning again (create a recursive loop)
    root.after(1000, scanning)

def start():
    global state
    state = True

def stop():
    global state
    state = False


root = Tk() #creates tk gui
root.title("COM State") #title 
root.geometry("210x500") #window size

start = Button(text="Open COM Port", command=start, fg="green") #buttons widget.
stop = Button(text="Close COM Port", command=stop, fg="red")

start.grid(column = 0, row = 0) #places buttons with the .grid() function
stop.grid(column = 1, row = 0, sticky=W)

w = Label(root,  
         text = "ScrolledText Widget",  
         font = ("Times New Roman", 12),  
         background = 'blue', 
         padx = 40, 
         foreground = "white")
w.grid(row = 1, columnspan=2, sticky=W)

text_area = st.ScrolledText(root, 
                            width = 10,  
                            height = 8,  
                            font = ("Times New Roman", 
                                    15)) 
  
text_area.grid(column = 0, pady = 10, padx = 15, columnspan = 2)
text_area.insert(INSERT, list) 
  
# Making the text read only 
text_area.configure(state ='disabled') 
  # After 1 second, call scanning
root.after(1000, scanning)
root.mainloop()