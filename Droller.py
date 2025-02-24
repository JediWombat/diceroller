from tkinter import *
from tkinter import ttk
import random
import gc as gc
import os, sys, platform
from PIL import ImageTk, Image
from idlelib.tooltip import Hovertip

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

class ScrollFrame(Frame):
	def __init__(self, parent):
		super().__init__(parent) # create a frame (self)

		self.canvas = Canvas(self, borderwidth=0, background="#ffffff")	#place canvas on self
		self.viewPort = Frame(self.canvas, background="#ffffff")			#place a frame on the canvas, this frame will hold the child widgets 
		self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)	#place a scrollbar on self 
		self.canvas.configure(yscrollcommand=self.vsb.set)					#attach scrollbar action to scroll of canvas

		self.vsb.pack(side="right", fill="y")								#pack scrollbar to right of self
		self.canvas.pack(side="left", fill="both", expand=True)				#pack canvas to left of self and expand to fil
		self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw", tags="self.viewPort") #add view port frame to canvas

		self.viewPort.bind("<Configure>", self.onFrameConfigure)			#bind an event whenever the size of the viewPort frame changes.
		self.canvas.bind("<Configure>", self.onCanvasConfigure)				#bind an event whenever the size of the canvas frame changes.
			
		self.viewPort.bind('<Enter>', self.onEnter)							# bind wheel events when the cursor enters the control
		self.viewPort.bind('<Leave>', self.onLeave)							# unbind wheel events when the cursorl leaves the control

		self.onFrameConfigure(None)											#perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

	def onFrameConfigure(self, event):											  
		'''Reset the scroll region to encompass the inner frame'''
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))			#whenever the size of the frame changes, alter the scroll region respectively.

	def onCanvasConfigure(self, event):
		'''Reset the canvas window to encompass inner frame when required'''
		canvas_width = event.width
		self.canvas.itemconfig(self.canvas_window, width = canvas_width)	#whenever the size of the canvas changes alter the window region respectively.

	def onMouseWheel(self, event):											# cross platform scroll wheel event
		if platform.system() == 'Windows':
			self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")
		elif platform.system() == 'Darwin':
			self.canvas.yview_scroll(int(-1 * event.delta), "units")
		else:
			if event.num == 4:
				self.canvas.yview_scroll( -1, "units" )
			elif event.num == 5:
				self.canvas.yview_scroll( 1, "units" )
	
	def onEnter(self, event):												# bind wheel events when the cursor enters the control
		if platform.system() == 'Linux':
			self.canvas.bind_all("<Button-4>", self.onMouseWheel)
			self.canvas.bind_all("<Button-5>", self.onMouseWheel)
		else:
			self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

	def onLeave(self, event):												# unbind wheel events when the cursorl leaves the control
		if platform.system() == 'Linux':
			self.canvas.unbind_all("<Button-4>")
			self.canvas.unbind_all("<Button-5>")
		else:
			self.canvas.unbind_all("<MouseWheel>")
		#endif
	#endDef
#endclass

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

def incMod(event, num): #increment/decrement modifier
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

	macFile = open("macros.ini", "r")
	macContents = macFile.readlines()
	for macro in macContents:
		macName = macro.split(',')[0]
		if macName == name:
			output.delete("1.0", END)
			output.insert(END, f'There is already a macro saved named {name}.\n\nMacros must have a unique name.')
			return
		#endif
	#endfor
	for die in 4, 6, 8, 10, 12, 20, 100, 1:
		size=0
		num=d[die].get()
		mod=m[die].cget("text")
		if die == 1:
			size=d[2].get()
		#endif
		if num == "0":
			continue
		else:
			if macString == "":
				macString=f'{name},'
			#endif
			if size != 0:
				macString+=f'{str(num)},{str(die)},{str(size)},{str(mod)},'
			else:
				macString+=f'{str(num)},{str(die)},{str(mod)},'
			#endif
		#endif
	#endFor
	#print(f'Saving macro: {macString}')
	macString = macString[:-1]
	macFile = open("macros.ini","a")
	macFile.write(f'{macString}\n')
	macFile.close()
	output.delete("1.0", END)
	output.insert(END, f'Macro \"{name}\" was saved successfully.')
#enddef

nameFrame = Frame(root, width=700, height=20, bg="#1b1f1a")
nameFrame.place(x=0, y=210)
nameLbl = Label(nameFrame, text="Roll Name:", bg="#3b3f3a", fg="white", borderwidth=2, relief=SUNKEN)
nameLbl.grid(row=0, column=0, padx=10)
nameEntry = Entry(nameFrame)
nameEntry.grid(row=0, column=1)
saveMac = Button(nameFrame, text="Save macro", command=saveMacro)
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
	==Macros==\n\
Setup the dice however you want them, enter a name in the name field, and click \"Save\"\nto save that set of rolls.\n\
Click the \"Macros\" button to view a list of your saved rolls.\n\n\
	==Making it go==\n\
Click \"Roll!\" to roll the dice as you've defined them.\nClick \"Reset\" to set all dice, modifiers, and other inputs back to zero.\nNote that the custom die size is not reset.")
	helpTxt.place(x=0, y=0, relwidth=1.0)
#endDef

helpBtn = Button(root, text="Usage Help", command=showHelp)
helpBtn.place(x=765, y=540, anchor=SE)

def macWdwCloseHandler():
	macWdw.update()
	global macWdwX, macWdwY
	macWdwX=macWdw.winfo_x()
	macWdwY=macWdw.winfo_y()
	macWdw.destroy()
#endDef

def showMacWdw(x, y):
	print(f'x:{x}, y:{y}, macWdwX:{macWdwX}, macWdwY:{macWdwY}')
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
	
	if x==0 and y==0: #this means we haven't closed the macro window before.
		root.update()
		rootX = root.winfo_x()
		rootY = root.winfo_y()
		macWdw.geometry("%dx%d+%d+%d" % (675, 400, rootX+800, rootY+300))
	else: #if we have, we'll put it back where it was.
		macWdw.geometry("%dx%d+%d+%d" % (675, 400, x, y))
	#endif
	macWdw.configure(bg="#1b1f1a", borderwidth=1, relief=RIDGE)
	macWdw.resizable("false","false")

	macWdw.protocol("WM_DELETE_WINDOW", macWdwCloseHandler)

	#macWdwCloseBtn = Button(macWdw, text="Close", command= lambda: macWdw.destroy())
	#macWdwCloseBtn.place(x=625, y=5, anchor=NW)

	macFile = open("macros.ini","r")
	global macLoadImg, macRollImg, macDelImg #these have to be defined here or they'll be garbage collected from the showMac() function?
	macLoadImg = PhotoImage(file="up-arrow.png")
	macRollImg = PhotoImage(file="up-arrow.png")
	macDelImg = PhotoImage(file="up-arrow.png")
	i=0
	macFrame = ScrollFrame(macWdw)#, width=350, borderwidth=1, relief=RAISED, bg="#505050")
	macFrame.place(x=5, y=5)
	for curMacString in macFile:
		curMacList = curMacString.split(',')
		showMac(curMacList, i, macFrame, macLoadImg, macRollImg, macDelImg)
		i+=2
	#endfor

	line = ttk.Separator(macWdw, orient='horizontal').place(y=300, relwidth=1.0)
	macHelp = Text(macWdw, height=4, width=70, bg="#1b1f1a", borderwidth=0, fg="white", font=("Arial Narrow", "12"))
	macHelp.place(y=310, relwidth=0.9)
	macHelp.insert("1.0", "Saved macros are shown here. Button functions are as follows:\n\
-   Load: Load the saved dice values and roll name into the main window.\n\
-   Roll: As above, but immediately perform a roll of the saved dice.\n\
-   Delete: Orders you a fresh Cosmopolitan...")
#endDef

macWdwX=macWdwY=0
macroBtn = Button(root, text="Macros", command= lambda: showMacWdw(macWdwX,macWdwY))
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
		m[macSize].config(text=f'{macMod.strip('\n')}') #the final mod in the macro ends in a newline in macros.ini; this was putting the newline into the mod field without strip().
	#endWhile
#endDef

def delMac(macName):
	macFile = open("macros.ini","r")
	macContents = macFile.readlines()
	macFile.close()

	macFile = open("macros.ini", "w")
	for macro in macContents:
		targetMacName = macro.split(',')[0]
		if targetMacName != macName:
			macFile.write(macro)
		#endif
	#endfor
	macFile.close()
	macWdw.update()
	macWdwX=macWdw.winfo_x()
	macWdwY=macWdw.winfo_y()
	macWdw.destroy()
	showMacWdw(macWdwX, macWdwY)

#endDef

def showMac(macro, row, frameRef, macLoadImg, macRollImg, macDelImg):
	macName = Label(frameRef.viewPort, text=f'{macro[0]}')
	macName.grid(row=row, column=0, sticky=EW, padx=10, pady=3)
	macDice = Entry(frameRef.viewPort, width=0)
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
	macDice.grid(row=row, column=1, padx=5, sticky=EW)

	macLoadLbl = Label(frameRef.viewPort, image=macLoadImg, bg="white")
	macLoadLbl.grid(row=row, column=2, padx=2)
	macLoadTip = Hovertip(macLoadLbl, "Load this macro into the main window", hover_delay=400)

	macLoadLbl.bind("<Button-1>", lambda event: loadMac(macro))

	macRollLbl = Label(frameRef.viewPort, image=macRollImg, bg="white")
	macRollLbl.grid(row=row, column=3, padx=2)
	macRollTip = Hovertip(macRollLbl, "Load this macro into the main window, and roll it.", hover_delay=400)

	macRollLbl.bind("<Button-1>", lambda event: loadMacAndRoll(macro))

	macDelLbl = Label(frameRef.viewPort, image=macDelImg, bg="white")
	macDelLbl.grid(row=row, column=4, padx=2, pady=2)
	macDelTip = Hovertip(macDelLbl, "Nobody knows what this button does.", hover_delay=400)

	macDelLbl.bind("<Button-1>", lambda event: delMac(macName.cget("text")))

	line = ttk.Separator(frameRef.viewPort, orient='horizontal').grid(row=row+1, column=0, columnspan=5, sticky=EW)
#endDef

def loadMacAndRoll(macro):
	loadMac(macro)
	roll()
#endDef

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