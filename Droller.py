from tkinter import *
from tkinter import ttk
import random
import os
import sys
from PIL import ImageTk, Image

def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")
	#endtry

	return os.path.join(base_path, relative_path)
#enddef

root = Tk()
root.title("Dice Roller")
root.geometry('775x550')
root.configure(bg="#1b1f1a")
root.resizable("false","false")

def zeroDice():
	for die in 4, 6, 8, 10, 12, 20, 100, 1:
		d[die].delete(0, END)
		d[die].insert(0, "0")
	#endfor
	output.delete("1.0", END)
	output.insert("1.0", "All dice reset to zero.")
#enddef

def roll():
	output.delete(1.0, END)
	rollTotal = 0
	for die in 4, 6, 8, 10, 12, 20, 100, 1:
		i=0
		sub = 0
		if d[die].get() != "":
			if int(d[die].get()) <= 0:
				d[die].delete(0, END)
				d[die].insert(0, "0")
			#endif
			if int(d[die].get()) > 20:
				d[die].delete(0, END)
				d[die].insert(0, "20")
			#endif
			if d[die].get() != "0":
				if die == 1:
					if int(sizeX.get()) == 0:
						output.insert(END, f'You asked to roll {numX.get()}d0. I can\'t roll a zero-sided die.')
						break
					else:
						output.insert(END, f'd{int(sizeX.get())}: ')
					#endif
				else:
					output.insert(END, f'd{die}: ')
				#endif
			#endif
			while i < int(d[die].get()):
				i += 1
				if die == 1:
					newRoll = random.randint(1,int(sizeX.get()))
				else:
					newRoll = random.randint(1,die)
				#endif
				output.insert(END, f'{newRoll}')
				sub += newRoll
				if i == int(d[die].get()):
					if die == 1:
						output.insert(END, f'\n\n Sub-total for d{int(sizeX.get())}: {sub}\n\n')
					else:
						output.insert(END, f'\n\n Sub-total for d{die}: {sub}\n\n')
					#endif
					rollTotal += sub
				else:
					output.insert(END, f', ')
				#endif
			#endwhile
		else:
			break
		#endif
	totText.delete("1.0", END)
	totText.insert(END, f'Total: {rollTotal}')
	#endfor
#enddef

dFrame = Frame(root, bg="#1b1f1a")
dFrame.place(anchor=W, x=10, rely=0.15)

#img4 = ImageTk.PhotoImage(Image.open(os.path.abspath("E:\\Creations\\Programs\\Droller\\d4.png")).resize((75,75)))
img4 = ImageTk.PhotoImage(Image.open(resource_path("d4.png")).resize((75,75)))

can4 = Canvas(dFrame, width=75, height=75, bg="#151014", bd=0, highlightthickness=0)
can4.create_image(0, 0, image=img4, anchor=NW)

can4.bind("<Button-1>", lambda event, mode="plus": mod(mode, 4))
can4.bind("<Button-2>", lambda event, mode="minus": mod(mode, 4))
can4.bind("<Button-3>", lambda event, mode="minus": mod(mode, 4))
can4.bind("<MouseWheel>", lambda event: mouse_wheel(event, 4))
can4.grid(row=0, column=0, columnspan=2, sticky=EW, padx=0)

num4 = ttk.Entry(dFrame, width = 8, justify=CENTER)
num4.insert(0,"0")
num4.grid(row = 1, column=0, columnspan=2, pady=8)

line = ttk.Separator(dFrame, orient='vertical').grid(row = 0, column=2, rowspan=20, sticky="ns", padx=10)

img6 = ImageTk.PhotoImage(Image.open(resource_path("d6.png")).resize((75,75)))

can6 = Canvas(dFrame, width=75, height=75, bg="#151014", bd=0, highlightthickness=0)
can6.create_image(0, 0, image=img6, anchor=NW)

can6.bind("<Button-1>", lambda event, mode="plus": mod(mode, 6))
can6.bind("<Button-2>", lambda event, mode="minus": mod(mode, 6))
can6.bind("<Button-3>", lambda event, mode="minus": mod(mode, 6))
can6.bind("<MouseWheel>", lambda event: mouse_wheel(event, 6))
can6.grid(row=0, column=3, columnspan=2, sticky=EW)

num6 = ttk.Entry(dFrame, width = 8, justify=CENTER)
num6.insert(0,"0")
num6.grid(row = 1, column=3, columnspan=2, pady=8)

line = ttk.Separator(dFrame, orient='vertical').grid(row = 0, column=5, rowspan=20, sticky="ns", padx=10)

img8 = ImageTk.PhotoImage(Image.open(resource_path("d8.png")).resize((75,75)))

can8 = Canvas(dFrame, width=75, height=75, bg="#151014", bd=0, highlightthickness=0)
can8.create_image(0, 0, image=img8, anchor=NW)

can8.bind("<Button-1>", lambda event, mode="plus": mod(mode, 8))
can8.bind("<Button-2>", lambda event, mode="minus": mod(mode, 8))
can8.bind("<Button-3>", lambda event, mode="minus": mod(mode, 8))
can8.bind("<MouseWheel>", lambda event: mouse_wheel(event, 8))
can8.grid(row=0, column=6, columnspan=2, sticky=EW)

num8 = ttk.Entry(dFrame, width = 8, justify=CENTER)
num8.insert(0,"0")
num8.grid(row = 1, column=6, columnspan=2, pady=8)

line = ttk.Separator(dFrame, orient='vertical').grid(row = 0, column=8, rowspan=20, sticky="ns", padx=10)

img10 = ImageTk.PhotoImage(Image.open(resource_path("d10.png")).resize((75,75)))

can10 = Canvas(dFrame, width=75, height=75, bg="#151014", bd=0, highlightthickness=0)
can10.create_image(0, 0, image=img10, anchor=NW)

can10.bind("<Button-1>", lambda event, mode="plus": mod(mode, 10))
can10.bind("<Button-2>", lambda event, mode="minus": mod(mode, 10))
can10.bind("<Button-3>", lambda event, mode="minus": mod(mode, 10))
can10.bind("<MouseWheel>", lambda event: mouse_wheel(event, 10))
can10.grid(row=0, column=9, columnspan=2, sticky=EW)

num10 = ttk.Entry(dFrame, width = 8, justify=CENTER)
num10.insert(0,"0")
num10.grid(row = 1, column=9, columnspan=2, pady=8)

line = ttk.Separator(dFrame, orient='vertical').grid(row = 0, column=11, rowspan=20, sticky="ns", padx=10)

img12 = ImageTk.PhotoImage(Image.open(resource_path("d12.png")).resize((75,75)))

can12 = Canvas(dFrame, width=75, height=75, bg="#151014", bd=0, highlightthickness=0)
can12.create_image(0, 0, image=img12, anchor=NW)

can12.bind("<Button-1>", lambda event, mode="plus": mod(mode, 12))
can12.bind("<Button-2>", lambda event, mode="minus": mod(mode, 12))
can12.bind("<Button-3>", lambda event, mode="minus": mod(mode, 12))
can12.bind("<MouseWheel>", lambda event: mouse_wheel(event, 12))
can12.grid(row=0, column=12, columnspan=2, sticky=EW)

num12 = ttk.Entry(dFrame, width = 8, justify=CENTER)
num12.insert(0,"0")
num12.grid(row = 1, column=12, columnspan=2, pady=8)

line = ttk.Separator(dFrame, orient='vertical').grid(row = 0, column=14, rowspan=20, sticky="ns", padx=10)

img20 = ImageTk.PhotoImage(Image.open(resource_path("d20.png")).resize((75,75)))

can20 = Canvas(dFrame, width=75, height=75, bg="#151014", bd=0, highlightthickness=0)
can20.create_image(0, 0, image=img20, anchor=NW)

can20.bind("<Button-1>", lambda event, mode="plus": mod(mode, 20))
can20.bind("<Button-2>", lambda event, mode="minus": mod(mode, 20))
can20.bind("<Button-3>", lambda event, mode="minus": mod(mode, 20))
can20.bind("<MouseWheel>", lambda event: mouse_wheel(event, 20))
can20.grid(row=0, column=15, columnspan=2, sticky=EW)

num20 = ttk.Entry(dFrame, width = 8, justify=CENTER)
num20.insert(0,"0")
num20.grid(row = 1, column=15, columnspan=2, pady=8)

line = ttk.Separator(dFrame, orient='vertical').grid(row = 0, column=17, rowspan=20, sticky="ns", padx=10)

img100 = ImageTk.PhotoImage(Image.open(resource_path("d100.png")).resize((75,75)))

can100 = Canvas(dFrame, width=75, height=75, bg="#151014", bd=0, highlightthickness=0)
can100.create_image(0, 0, image=img100, anchor=NW)

can100.bind("<Button-1>", lambda event, mode="plus": mod(mode, 100))
can100.bind("<Button-2>", lambda event, mode="minus": mod(mode, 100))
can100.bind("<Button-3>", lambda event, mode="minus": mod(mode, 100))
can100.bind("<MouseWheel>", lambda event: mouse_wheel(event, 100))
can100.grid(row=0, column=18, columnspan=2, sticky=EW)

num100 = ttk.Entry(dFrame, width = 8, justify=CENTER)
num100.insert(0,"0")
num100.grid(row = 1, column=18, columnspan=2, pady=8)

line = ttk.Separator(dFrame, orient='vertical').grid(row = 0, column=20, rowspan=20, sticky="ns", padx=10)

imgX = ImageTk.PhotoImage(Image.open(resource_path("dx.png")).resize((75,75)))

canX = Canvas(dFrame, width=75, height=75, bg="#151014", bd=0, highlightthickness=0)
canX.create_image(0, 0, image=imgX, anchor=NW)

canX.bind("<Button-1>", lambda event, mode="plus": mod(mode, 1))
canX.bind("<Button-2>", lambda event, mode="minus": mod(mode, 1))
canX.bind("<Button-3>", lambda event, mode="minus": mod(mode, 1))
canX.bind("<MouseWheel>", lambda event: mouse_wheel(event, 1))
canX.grid(row=0, column=21, columnspan=3, sticky=EW)

#labelXNum = Label(dFrame, text="#")
#labelXNum.grid(row=1, column=21, sticky=E)

numX = ttk.Entry(dFrame, width = 2, justify=CENTER)
numX.insert(0,"0")
numX.grid(row = 1, column=21, pady=8)

labelXSize = Label(dFrame, text="d", width=1, background="#1b1f1a", foreground="white")
labelXSize.grid(row=1, column=22) #, sticky=E)

sizeX = ttk.Entry(dFrame, width = 2, justify=CENTER)
sizeX.insert(0,"0")
sizeX.grid(row = 1, column=23, pady=3)

### End of dice
line = ttk.Separator(root, orient='horizontal').place(y=155, relwidth=1.0)


rollBtn = Button(root, text="Roll!", command=roll)
rollBtn.place(x=10, y=170)

zeroBtn = Button(root, text="Reset", command=zeroDice, width=10)
zeroBtn.place(x=765, y=170, anchor=NE)

outFrame = Frame(root, width=755, height=200)
outFrame.place(x=10, y=210)
output = Text(outFrame, height=1, width=1)
output.place(relwidth=1.0, relheight=1.0)
output.insert(END, "Assign the number of dice to roll above, then click \"Roll\"!\n")

totFrame = Frame(root, width = 100, height = 20)
totFrame.place(x=10, y=420)
totText = Text(totFrame, height=1, width=1)
totText.place(relwidth=1.0, relheight=1.0)

#define dictionary of Entry objects
d = {4: num4, 6: num6, 8:num8, 10:num10, 12:num12, 20:num20, 100:num100, 1:numX}

def mod(op, num):
	oldNum = int(d[num].get())
	#print("oldNum: " + str(oldNum))
	if op == "plus":
		if oldNum >= 20:
			newNum = 20
		else:
			newNum = oldNum + 1
		#endif
	else:
		if oldNum <= 0:
			newNum = 0
		else:
			newNum = oldNum - 1
		#endif
	#endif
	d[num].delete(0, END)
	d[num].insert(0, newNum)
	#endif
#enddef

def mouse_wheel(event, num):
	if event.delta >= 0:
		mod("plus", num)
	else:
		mod("minus", num)
	#endif
#enddef


'''
### Old layout
mFrame = Frame(root)
mFrame.grid(row=1, column=1)

lMode = Label(mFrame, text="Mode Selector:").grid(row=0, column=0)

curMode = ""
modeNormal = Radiobutton(mFrame, text="New Rolls", variable=curMode, value="new")
modeNormal.grid(row=1, column=0)
modeNormal.select()

modeAdd = Radiobutton(mFrame, text="Additive", variable=curMode, value="add")
modeAdd.grid(row=1, column=1)
modeAdd.deselect()

modeLog = Radiobutton(mFrame, text="Log", variable=curMode, value="log")
modeLog.grid(row=1, column=2)
modeLog.deselect()

###End mode/options frame

line = ttk.Separator(root, orient='horizontal').grid(row = 2, columnspan = 15, sticky="ew")

#d4
label4 = Label(text = "[d4]").grid(row=3, column=0, padx=20, sticky="W")

total4 = Text(width = 50, height = 4)
total4.grid(row = 4, column = 1, sticky="S")

options4 = Frame(root, bg="lightblue")
options4.grid(row=3,column=1)
lNum4 = Label(options4,text="Number of dice: ").grid(row=1,column=1)

num4 = Entry(options4, width = 3)
num4.insert(0,"1")
num4.grid(row = 1, column = 2)

def d4():
	total4.delete("1.0", END)
	i = 0
	rand = 0
	if num4.get() != "":
		if int(num4.get()) <= 50:
			while i < int(num4.get()):
				i += 1
				newRoll = random.randint(1,4)
				total4.insert(END, f'Roll {i}: {newRoll}\n')
				rand += newRoll
			#endwhile
		else:
			rand = "My hands aren't big enough for that many dice."
		#endif
	else:
		num4.insert(0,"1") #it looks cleaner than rolling 1 die with this field empty
		rand = random.randint(1,4)
	#endif
	
	total4.insert(1.0, f'Total: {rand}\n\n')
#enddef

btn4 = Button(root, text="Roll!", command=d4, width = 4, height = 2).grid(row = 4, column = 0)

blank = Label(text = "").grid(row=7, column=0)

line = ttk.Separator(root, orient='horizontal').grid(row = 9, columnspan = 15, sticky="ew")

label6 = Label(text="[d6]").grid(row = 12, column = 0)
'''

root.mainloop()