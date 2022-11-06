from tkinter import *
from turtle import left

from pyparsing import col

def clear():
    CheckVar1.set(0)
    CheckVar2.set(0)
    CheckVar3.set(0)
    CheckVar4.set(0)
    CheckVar5.set(0)
    CheckVar6.set(0)
    result_string = ''
    result_value_label.config(text = result_string, bg="yellow")

def check_musicsel():
    result_string = ''
    C1_Var = CheckVar1.get()
    C2_Var = CheckVar2.get()
    C3_Var = CheckVar3.get()
    C4_Var = CheckVar4.get()
    C5_Var = CheckVar5.get()
    C6_Var = CheckVar6.get()
    output_result_label.config(text='You have selected the following: ')
    if C1_Var == 1:
        result_string = result_string + 'Jazz;'
         
    if C2_Var == 1:
        result_string = result_string + 'K-Pop/J-Pop; '
    
    if C3_Var == 1:
        result_string = result_string + 'Country; '
    
    if C4_Var == 1:
        result_string = result_string + 'Hip-Hop; '
    
    if C5_Var == 1:
        result_string = result_string + 'Rock; '
    
    if C6_Var == 1:
        result_string= result_string + 'Classical; '
    
    result_value_label.config(text = result_string, bg="yellow")

def music_options():
    clear()
    check_label = Label(root, text = 'Please choose some examples that you like.')
    check_label.grid(row=0,column=1)
    C1 = Checkbutton(root, text = "Jazz", variable = CheckVar1, anchor='w',\
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, command = check_musicsel)
    C2 = Checkbutton(root, text = "K-Pop/J-Pop", variable = CheckVar2, anchor='w',\
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, command = check_musicsel)
    C3 = Checkbutton(root, text = "Country", variable = CheckVar3, anchor='w',\
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, command = check_musicsel)
    C4 = Checkbutton(root, text = "Hip-Hop", variable = CheckVar4, anchor='w',\
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, command = check_musicsel)
    C5 = Checkbutton(root, text = "Rock", variable = CheckVar5, anchor='w',\
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, command = check_musicsel)
    C6 = Checkbutton(root, text = "Classical", variable = CheckVar6, anchor='w',\
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, command = check_musicsel)
    C1.grid(row=1,column=1,sticky="W")
    C2.grid(row=2,column=1,sticky="W")
    C3.grid(row=3,column=1,sticky="W")
    C4.grid(row=4,column=1,sticky="W")
    C5.grid(row=5,column=1,sticky="W")
    C6.grid(row=6,column=1,sticky="W")

def check_moviesel():
    result_string = ''
    C1_Var = CheckVar1.get()
    C2_Var = CheckVar2.get()
    C3_Var = CheckVar3.get()
    C4_Var = CheckVar4.get()
    C5_Var = CheckVar5.get()
    C6_Var = CheckVar6.get()
    output_result_label.config(text='You have selected the following: ')
    if C1_Var == 1:
        result_string = result_string + 'The Titanic; '
    
    if C2_Var == 1:
        result_string = result_string + 'Any Marvel Movie/TV Show; '
    
    if C3_Var == 1:
        result_string = result_string + 'Friends; '
    
    if C4_Var == 1:
        result_string = result_string + 'Stranger Things; '
    
    if C5_Var == 1:
        result_string = result_string + 'Any Anime Movie/TV Show; '
    
    if C6_Var == 1:
        result_string = result_string + 'Money Heist; '
    
    result_value_label.config(text = result_string,bg="yellow")

def movie_options():
    clear()
    check_label = Label(root, text = 'Please choose some examples that you like.')
    check_label.grid(row=0,column=1)
    C1 = Checkbutton(root, text = "The Titanic", variable = CheckVar1, anchor='w',\
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, command = check_moviesel)
    C2 = Checkbutton(root, text = "Any Marvel Movie/TV Show", variable = CheckVar2, anchor='w',\
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, command = check_moviesel)
    C3 = Checkbutton(root, text = "Friends", variable = CheckVar3, anchor='w',\
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, command = check_moviesel)
    C4 = Checkbutton(root, text = "Stranger Things", variable = CheckVar4, anchor='w',\
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, command = check_moviesel)
    C5 = Checkbutton(root, text = "Any Anime Movie/TV Show", variable = CheckVar5, anchor='w',\
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, command = check_moviesel)
    C6 = Checkbutton(root, text = "Money Heist", variable = CheckVar6, anchor='w',\
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, command = check_moviesel)
    C1.grid(row=1,column=1,sticky="W")
    C2.grid(row=2,column=1,sticky="W")
    C3.grid(row=3,column=1,sticky="W")
    C4.grid(row=4,column=1,sticky="W")
    C5.grid(row=5,column=1,sticky="W")
    C6.grid(row=6,column=1,sticky="W")

root = Tk()
root.title('Getting To Know the User')
label_input = Label(root, text = 'Please pick one of two options below.')
label_input.grid(row=0,column=0)
CheckVar1 = IntVar()
CheckVar2 = IntVar()
CheckVar3 = IntVar()
CheckVar4 = IntVar()
CheckVar5 = IntVar()
CheckVar6 = IntVar()
#print(CheckVar1, type(CheckVar1))
var = IntVar()

music_select = Radiobutton(root, text = 'Music', variable=var, value = 1,
                  command=music_options)
music_select.grid(row=1,column=0,sticky="W")
movie_select = Radiobutton(root, text = 'Movies/TV Shows', variable=var, value = 2,
                  command=movie_options)
movie_select.grid(row=2,column=0,sticky="W")

output_result_label = Label(root)
output_result_label.grid(row=8,column=0,sticky="W")
result_value_label = Label(root)
result_value_label.grid(row=8,column=1,sticky="W")

root.mainloop()