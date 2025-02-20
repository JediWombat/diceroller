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
		m[die].config(text="+0")
	#endfor
	nameEntry.delete(0, END)
	output.delete("1.0", END)
	totText.delete("1.0", END)
	output.insert("1.0", "All dice and modifiers reset to zero.")
#enddef

def roll():
	output.delete(1.0, END)
	rollTotal = 0
	if nameEntry.get() != "":
		vowels = ['a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U']
		if nameEntry.get()[:1] in vowels:
			output.insert(END, f'==You made an {nameEntry.get()} roll==\n\n')
		else:
			output.insert(END, f'==You made a {nameEntry.get()} roll==\n\n')
		#endif
	#endif
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
						output.insert(END, f'd[{int(sizeX.get())}]\n\nRolls: ')
					#endif
				else:
					output.insert(END, f'[d{die}]\n\nRolls: ')
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
				modi = 0
				if i == int(d[die].get()):
					output.insert(END, "\n")
					#if die == 1:
					#	output.insert(END, f'Sub-total for rolls d{int(sizeX.get())}: {sub}\n\n')
					#else:
					output.insert(END, f'Rolled total: {sub + modi}\n')
					#endif
					if m[die].cget("text") != "+0":
						modi = int(m[die].cget("text"))
						if modi > 99:
							m[die].config(text="99")
							modi = 99
						elif modi < -99:
							m[die].config(text="-99")
							modi = -99
						#endif
						#mods = m[die].cget("text") #modifier sign
						if modi < 0:
							output.insert(END, f'With {modi} modifier: {sub + modi}\n\n')
						else:
							output.insert(END, f'With +{modi} modifier: {sub + modi}\n\n')
						#endif
						rollTotal += modi
					else:
						output.insert(END, f'\n') #insert a blank line if there's no modifier output
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

'''def incMod(event, num):
	curVal = int(m[num].cget("text"))
	if event.num == 1 or event.delta > 0:
		if curVal + 1 >= 0:
			m[num].config(text="+" + str(curVal + 1))
		else:
			m[num].config(text=str(curVal + 1))
		#endif
	else:
		if curVal - 1 >= 0:
			m[num].config(text="+" + str(curVal - 1))
		else:
			m[num].config(text=str(curVal - 1))
		#endif
	#endif
#enddef'''

def incMod(event, num):
    curVal = int(m[num].cget("text")) #get current modifier value
    newVal = curVal + 1 if event.num == 1 or event.delta > 0 else curVal - 1 #increment if left-clicked or scrolled up, otherwise decrement
    m[num].config(text=(f"+" if newVal >= 0 else "") + str(newVal)) #prepend a "+" for a positive number, then cast it to a string and put it in the box
    #endif
#enddef

#frame to hold the die rollers
dFrame = Frame(root, bg="#1b1f1a")
dFrame.place(anchor=W, x=10, rely=0.15)

#img4 = ImageTk.PhotoImage(Image.open(os.path.abspath("E:\\Creations\\Programs\\Droller\\d4.png")).resize((75,75)))
img4 = ImageTk.PhotoImage(Image.open(resource_path("d4.png")).resize((75,75)))

can4 = Canvas(dFrame, width=75, height=75, bg="#3b3f3a", bd=0, highlightthickness=0)
can4.create_image(0, 0, image=img4, anchor=NW)

can4.bind("<Button-1>", lambda event, mode="plus": mod(mode, 4))
can4.bind("<Button-2>", lambda event, mode="minus": mod(mode, 4))
can4.bind("<Button-3>", lambda event, mode="minus": mod(mode, 4))
can4.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "num", 4))
can4.grid(row=0, column=0, columnspan=2, sticky=EW, padx=0)

num4 = ttk.Entry(dFrame, width = 8, justify=CENTER)
num4.insert(0,"0")
num4.grid(row=1, column=0, columnspan=2, pady=8)

modLbl4 = Label(dFrame, width=3, text="+0", justify=CENTER, background="#3b3f3a", foreground="white", borderwidth=2, relief="ridge", font=(12))
modLbl4.bind("<Button-1>", lambda event: incMod(event, 4))
modLbl4.bind("<Button-2>", lambda event: incMod(event, 4))
modLbl4.bind("<Button-3>", lambda event: incMod(event, 4))
modLbl4.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "mod", 4))
modLbl4.grid(row=2, column=0, columnspan=2)

line = ttk.Separator(dFrame, orient='vertical').grid(row = 0, column=2, rowspan=20, sticky="ns", padx=10)

img6 = ImageTk.PhotoImage(Image.open(resource_path("d6.png")).resize((75,75)))

can6 = Canvas(dFrame, width=75, height=75, bg="#3b3f3a", bd=0, highlightthickness=0)
can6.create_image(0, 0, image=img6, anchor=NW)

can6.bind("<Button-1>", lambda event, mode="plus": mod(mode, 6))
can6.bind("<Button-2>", lambda event, mode="minus": mod(mode, 6))
can6.bind("<Button-3>", lambda event, mode="minus": mod(mode, 6))
can6.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "num", 6))
can6.grid(row=0, column=3, columnspan=2, sticky=EW)

num6 = ttk.Entry(dFrame, width = 8, justify=CENTER)
num6.insert(0,"0")
num6.grid(row = 1, column=3, columnspan=2, pady=8)

modLbl6 = Label(dFrame, width=3, text="+0", justify=CENTER, background="#3b3f3a", foreground="white", borderwidth=2, relief="ridge", font=(12))
modLbl6.bind("<Button-1>", lambda event: incMod(event, 6))
modLbl6.bind("<Button-2>", lambda event: incMod(event, 6))
modLbl6.bind("<Button-3>", lambda event: incMod(event, 6))
modLbl6.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "mod", 6))
modLbl6.grid(row=2, column=3, columnspan=2)

line = ttk.Separator(dFrame, orient='vertical').grid(row = 0, column=5, rowspan=20, sticky="ns", padx=10)

img8 = ImageTk.PhotoImage(Image.open(resource_path("d8.png")).resize((75,75)))

can8 = Canvas(dFrame, width=75, height=75, bg="#3b3f3a", bd=0, highlightthickness=0)
can8.create_image(0, 0, image=img8, anchor=NW)

can8.bind("<Button-1>", lambda event, mode="plus": mod(mode, 8))
can8.bind("<Button-2>", lambda event, mode="minus": mod(mode, 8))
can8.bind("<Button-3>", lambda event, mode="minus": mod(mode, 8))
can8.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "num", 8))
can8.grid(row=0, column=6, columnspan=2, sticky=EW)

num8 = ttk.Entry(dFrame, width = 8, justify=CENTER)
num8.insert(0,"0")
num8.grid(row = 1, column=6, columnspan=2, pady=8)

modLbl8 = Label(dFrame, width=3, text="+0", justify=CENTER, background="#3b3f3a", foreground="white", borderwidth=2, relief="ridge", font=(12))
modLbl8.bind("<Button-1>", lambda event: incMod(event, 8))
modLbl8.bind("<Button-2>", lambda event: incMod(event, 8))
modLbl8.bind("<Button-3>", lambda event: incMod(event, 8))
modLbl8.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "mod", 8))
modLbl8.grid(row=2, column=6, columnspan=2)

line = ttk.Separator(dFrame, orient='vertical').grid(row = 0, column=8, rowspan=20, sticky="ns", padx=10)

img10 = ImageTk.PhotoImage(Image.open(resource_path("d10.png")).resize((75,75)))

can10 = Canvas(dFrame, width=75, height=75, bg="#3b3f3a", bd=0, highlightthickness=0)
can10.create_image(0, 0, image=img10, anchor=NW)

can10.bind("<Button-1>", lambda event, mode="plus": mod(mode, 10))
can10.bind("<Button-2>", lambda event, mode="minus": mod(mode, 10))
can10.bind("<Button-3>", lambda event, mode="minus": mod(mode, 10))
can10.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "num", 10))
can10.grid(row=0, column=9, columnspan=2, sticky=EW)

num10 = ttk.Entry(dFrame, width = 8, justify=CENTER)
num10.insert(0,"0")
num10.grid(row = 1, column=9, columnspan=2, pady=8)

modLbl10 = Label(dFrame, width=3, text="+0", justify=CENTER, background="#3b3f3a", foreground="white", borderwidth=2, relief="ridge", font=(12))
modLbl10.bind("<Button-1>", lambda event: incMod(event, 10))
modLbl10.bind("<Button-2>", lambda event: incMod(event, 10))
modLbl10.bind("<Button-3>", lambda event: incMod(event, 10))
modLbl10.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "mod", 10))
modLbl10.grid(row=2, column=9, columnspan=2)

line = ttk.Separator(dFrame, orient='vertical').grid(row = 0, column=11, rowspan=20, sticky="ns", padx=10)

img12 = ImageTk.PhotoImage(Image.open(resource_path("d12.png")).resize((75,75)))

can12 = Canvas(dFrame, width=75, height=75, bg="#3b3f3a", bd=0, highlightthickness=0)
can12.create_image(0, 0, image=img12, anchor=NW)

can12.bind("<Button-1>", lambda event, mode="plus": mod(mode, 12))
can12.bind("<Button-2>", lambda event, mode="minus": mod(mode, 12))
can12.bind("<Button-3>", lambda event, mode="minus": mod(mode, 12))
can12.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "num", 12))
can12.grid(row=0, column=12, columnspan=2, sticky=EW)

num12 = ttk.Entry(dFrame, width = 8, justify=CENTER)
num12.insert(0,"0")
num12.grid(row = 1, column=12, columnspan=2, pady=8)

modLbl12 = Label(dFrame, width=3, text="+0", justify=CENTER, background="#3b3f3a", foreground="white", borderwidth=2, relief="ridge", font=(12))
modLbl12.bind("<Button-1>", lambda event: incMod(event, 12))
modLbl12.bind("<Button-2>", lambda event: incMod(event, 12))
modLbl12.bind("<Button-3>", lambda event: incMod(event, 12))
modLbl12.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "mod", 12))
modLbl12.grid(row=2, column=12, columnspan=2)

line = ttk.Separator(dFrame, orient='vertical').grid(row = 0, column=14, rowspan=20, sticky="ns", padx=10)

img20 = ImageTk.PhotoImage(Image.open(resource_path("d20.png")).resize((75,75)))

can20 = Canvas(dFrame, width=75, height=75, bg="#3b3f3a", bd=0, highlightthickness=0)
can20.create_image(0, 0, image=img20, anchor=NW)

can20.bind("<Button-1>", lambda event, mode="plus": mod(mode, 20))
can20.bind("<Button-2>", lambda event, mode="minus": mod(mode, 20))
can20.bind("<Button-3>", lambda event, mode="minus": mod(mode, 20))
can20.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "num", 20))
can20.grid(row=0, column=15, columnspan=2, sticky=EW)

num20 = ttk.Entry(dFrame, width = 8, justify=CENTER)
num20.insert(0,"0")
num20.grid(row = 1, column=15, columnspan=2, pady=8)

modLbl20 = Label(dFrame, width=3, text="+0", justify=CENTER, background="#3b3f3a", foreground="white", borderwidth=2, relief="ridge", font=(12))
modLbl20.bind("<Button-1>", lambda event: incMod(event, 20))
modLbl20.bind("<Button-2>", lambda event: incMod(event, 20))
modLbl20.bind("<Button-3>", lambda event: incMod(event, 20))
modLbl20.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "mod", 20))
modLbl20.grid(row=2, column=15, columnspan=2)

line = ttk.Separator(dFrame, orient='vertical').grid(row = 0, column=17, rowspan=20, sticky="ns", padx=10)

img100 = ImageTk.PhotoImage(Image.open(resource_path("d100.png")).resize((75,75)))

can100 = Canvas(dFrame, width=75, height=75, bg="#3b3f3a", bd=0, highlightthickness=0)
can100.create_image(0, 0, image=img100, anchor=NW)

can100.bind("<Button-1>", lambda event, mode="plus": mod(mode, 100))
can100.bind("<Button-2>", lambda event, mode="minus": mod(mode, 100))
can100.bind("<Button-3>", lambda event, mode="minus": mod(mode, 100))
can100.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "num", 100))
can100.grid(row=0, column=18, columnspan=2, sticky=EW)

num100 = ttk.Entry(dFrame, width = 8, justify=CENTER)
num100.insert(0,"0")
num100.grid(row = 1, column=18, columnspan=2, pady=8)

modLbl100 = Label(dFrame, width=3, text="+0", justify=CENTER, background="#3b3f3a", foreground="white", borderwidth=2, relief="ridge", font=(12))
modLbl100.bind("<Button-1>", lambda event: incMod(event, 100))
modLbl100.bind("<Button-2>", lambda event: incMod(event, 100))
modLbl100.bind("<Button-3>", lambda event: incMod(event, 100))
modLbl100.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "mod", 100))
modLbl100.grid(row=2, column=18, columnspan=2)

line = ttk.Separator(dFrame, orient='vertical').grid(row = 0, column=20, rowspan=20, sticky="ns", padx=10)

imgX = ImageTk.PhotoImage(Image.open(resource_path("dx.png")).resize((75,75)))

canX = Canvas(dFrame, width=75, height=75, bg="#3b3f3a", bd=0, highlightthickness=0)
canX.create_image(0, 0, image=imgX, anchor=NW)

canX.bind("<Button-1>", lambda event, mode="plus": mod(mode, 1))
canX.bind("<Button-2>", lambda event, mode="minus": mod(mode, 1))
canX.bind("<Button-3>", lambda event, mode="minus": mod(mode, 1))
canX.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "num", 1))
canX.grid(row=0, column=21, columnspan=3, sticky=EW)

numX = ttk.Entry(dFrame, width = 2, justify=CENTER)
numX.insert(0,"0")
numX.grid(row = 1, column=21, pady=8)

labelXSize = Label(dFrame, text="d", width=1, background="#1b1f1a", foreground="white")
labelXSize.grid(row=1, column=22) #, sticky=E)

sizeX = ttk.Entry(dFrame, width = 2, justify=CENTER)
sizeX.insert(0,"0")
sizeX.grid(row = 1, column=23, pady=3)

modLblX = Label(dFrame, width=3, text="+0", justify=CENTER, background="#3b3f3a", foreground="white", borderwidth=2, relief="ridge", font=(12))
modLblX.bind("<Button-1>", lambda event: incMod(event, 1))
modLblX.bind("<Button-2>", lambda event: incMod(event, 1))
modLblX.bind("<Button-3>", lambda event: incMod(event, 1))
modLblX.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "mod", 1))
modLblX.grid(row=2, column=21, columnspan=3)
### End of dice

line = ttk.Separator(root, orient='horizontal').place(y=155, relwidth=1.0)

rollBtn = Button(root, text="Roll!", command=roll)
rollBtn.place(x=10, y=170)

zeroBtn = Button(root, text="Reset", command=zeroDice, width=10)
zeroBtn.place(x=765, y=170, anchor=NE)

def saveMacro():
	macString=""
	name=nameEntry.get()
	if name == "":
		output.delete("1.0", END)
		output.insert(END, "You must enter a name to save a macro.")
		return
	#endif
	for die in 4, 6, 8, 10, 12, 20, 100, 1:
		num=d[die].get()
		mod=m[die].cget("text")
		
		if num == "0":
			continue
		else:
			if macString == "":
				macString=f'{name},'
			#endif
			macString+=f'{str(num)},{str(die)},{str(mod)},'
		#emdif
	#endFor
	macString = macString[:-1]
	macFile = open("macros.ini","r+")
	macFile.write(macString)
#enddef

nameFrame = Frame(root, width=700, height=20, bg="#1b1f1a")
nameFrame.place(x=0, y=210)
nameLbl = Label(nameFrame, text="Name this roll?", bg="#3b3f3a", fg="white", borderwidth=2, relief=SUNKEN)
nameLbl.grid(row=0, column=0, padx=10)
nameEntry = Entry(nameFrame)
nameEntry.grid(row=0, column=1)
saveMac = Button(nameFrame, text="Save as macro", command=saveMacro)
saveMac.grid(row=0, column=2, padx=20)

outFrame = Frame(root, width=755, height=200)
outFrame.place(x=10, y=245)
output = Text(outFrame, height=1, width=1)
output.place(relwidth=1.0, relheight=1.0)
output.insert(END, "Assign the number of dice to roll above, then click \"Roll\"!\n\nPlease click the  help button below for more usage information.")

totFrame = Frame(root, width = 100, height = 20)
totFrame.place(x=10, y=465)
totText = Text(totFrame, height=1, width=1)
totText.place(relwidth=1.0, relheight=1.0)

def showHelp():
	try:
		global helpWdw
		if helpWdw.winfo_exists():
			pass
		else:
			helpWdw = Toplevel(root)
	except NameError:
		helpWdw = Toplevel(root)
	#endtry
	helpWdw.title("Dice Roller Usage Instructions")
	helpWdw.geometry("800x400")
	helpWdw.configure(bg="#1b1f1a")
	helpWdw.resizable("false","false")
	
	helpTxt = Text(helpWdw, bg="#1b1f1a", borderwidth=0, fg="white")
	helpTxt.insert(END, "Welcome to Dice Roller!\n\n\
	==Rolling Dice==\n\
You can assign the number of a given die to roll by clicking on it:\nLMB to increment, RMB to decrement. You can also scroll while hovering over a die.\n\
For the custom size die, set the number of rolls, and the size of the die.\n\n\
	==Modifiers==\n\
Modifiers are controlled by clicking on the modifier box:\nLMB to increment, RMB to decrement.\n\
You can also scroll while hovering on the multiplier.\n\n\
	==Naming Rolls==\n\
You can enter anything you like in the name field, and it'll be shown as the name of the roll in the output.\nThis isn't super useful in this version, but in future\nwe'll be adding more functionality around this.\n\n\
	==Making it go==\n\
Click \"Roll!\" to roll the dice as you've defined them.\nClick \"Reset\" to set all dice, modifiers, and other inputs back to zero.\nNote that the custom die size is not reset.")
	helpTxt.place(x=0, y=0, relwidth=1.0)
#endDef

helpBtn = Button(root, text="Usage Help", command=showHelp)
helpBtn.place(x=765, y=540, anchor=SE)

def showMacWdw():
	try:
		global macWdw
		if macWdw.winfo_exists():
			pass
		else:
			macWdw = Toplevel(root)
	except NameError:
		macWdw = Toplevel(root)
	#endtry
	macWdw.title("Dice Roller Macro Editor")
	macWdw.geometry("1000x600")
	macWdw.configure(bg="#1b1f1a")
	macWdw.resizable("false","false")

	macFile = open("macros.ini","r")
	i=0
	macFrame = Frame(macWdw, width=400, borderwidth=1, relief=RAISED, bg="#505050")
	macFrame.grid(row=0, column=0)
	for curMacString in macFile:
		curMacList = curMacString.split(',')
		showMac(curMacList, i, macFrame)
		print(i)
		i+=1
	#endfor

macroBtn = Button(root, text="Macros", command=showMacWdw)
macroBtn.place(x=10, y=540, anchor=SW)

#define dictionary of Entry objects
d = {4: num4, 6: num6, 8:num8, 10:num10, 12:num12, 20:num20, 100:num100, 1:numX, 2:sizeX}

m = {4:modLbl4, 6:modLbl6, 8:modLbl8, 10:modLbl10, 12:modLbl12, 20:modLbl20, 100:modLbl100, 1:modLblX}

def loadMac(macro):
	zeroDice()
	macName = macro[0]
	output.delete("1.0", END)
	output.insert(END, f'Macro "{macName}" loaded.')
	i=0
	nameEntry.delete(0, END)
	nameEntry.insert(END, macName)
	while i < (len(macro) - 1):
		realSize=0
		num=i+1
		macNum = macro[num]
		num=i+2
		macSize = int(macro[num])
		if macSize == 1:
			num=i+3
			realSize = macro[num]
			num=i+4
			macMod = macro[num]
			i+=4
		else:
			num=i+3
			macMod = macro[num]
			i+=3
		#endif
		d[macSize].delete(0, END)
		d[macSize].insert(0, macNum)
		if realSize != 0: #realSize is only set if "size" is 1, indicating an XdY roll.
			d[2].delete(0, END)
			d[2].insert(0, realSize)
		m[macSize].config(text=f'{macMod}')
	#endWhile
#endDef

def showMac(macro, row, frame):
	macName = Label(frame, text=[macro[0]])
	macName.grid(row=row, column=0, sticky=W)
	macDice = Entry(frame, width=0)
	i = 0
	realSize = 0
	while i < (len(macro) - 1):
		num=i+1
		size=i+2
		if macro[size] == "1": #to handle saved XdY rolls
			realSizeIndex=i+3
			realSize=macro[realSizeIndex]
			mod=i+4
			macDice.insert(END, f'{macro[num]}d{realSize} {macro[mod]}')
			i+=4
		else:
			mod=i+3
			macDice.insert(END, f'{macro[num]}d{macro[size]} {macro[mod]}')
			i+=3
		#endif
		if i < (len(macro) -1):
			macDice.insert(END, f', ')
		#endif
	#endwhile
	macDice.grid(row=row, column=1, padx=5)
	macLoadBtn = Button(frame, text="Load", command= lambda: loadMac(macro))
	macLoadBtn.grid(row=row, column=3)

	macRollBtn = Button(frame, text="Roll", command= lambda: (loadMac(macro), roll()))
	macRollBtn.grid(row=row, column=4)
#endDef


#testMac = ["Longsword", 1, 20, "+3", 1, 8, "+5"]
#loadMac(testMac)

def mod(op, num):
	oldNum = int(d[num].get())
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

def mouse_wheel_handler(event, target, num):
	if target == "num":
		if event.delta >= 0:
			mod("plus", num)
		else:
			mod("minus", num)
		#endif
	elif target == "mod":
		incMod(event, num)
	#endif
#enddef

root.mainloop()