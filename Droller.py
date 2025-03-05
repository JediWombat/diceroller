from tkinter import *
from tkinter import ttk
import gc as gc
import datetime as dt
import time
import os, sys, platform, random
from PIL import ImageTk, Image
from idlelib.tooltip import Hovertip

global mainColour
mainColour="#1b1f1a"
global accentColour
accentColour="#3b3f3a"

global rootW
rootW=775
global rootH
rootH=550

global rollLog
rollLog=""

global dRed
global dGreen
global dBlue

dRed=100
dGreen=220
dBlue=200

#we use these to loop through to apply new colours.
wm = [] #list of widgets with main colour
wa = [] #list of widgets with accent colour

#I'm not really sure what some of this does. What is MEIPASS? It only works when running from an executable, otherwise it bombs, hence the try: block.
def resource_path(relativePath):
	if "png" in relativePath:
		try:
			base_path = sys._MEIPASS #return local path (?) for *.png images, as they're baked into the executable.
		except Exception:
			if getattr(sys, 'frozen', False):
				base_path = os.path.abspath(sys.executable) #return the local path of the .exe if we're running as an executable, to find other files, such as the macros.ini. If running as a script this 
			else:
				base_path = os.path.abspath(".") #if we're running as a script, return the current path of the script itself.
			#endif
		#endtry
	else:
		base_path = os.path.abspath(".")
	#endif
	return os.path.join(base_path, relativePath)
#enddef

#create macro file if it does not exist
try:
	macFile = open(resource_path("macros.ini"), "r")
except IOError:
	macFile = open(resource_path("macros.ini"), "a")
	macFile.close()
#endTry

#replaceN from https://stackoverflow.com/a/46705963/1933916
def replaceN(s, sub, repl, nth):
    find = s.find(sub)
    i = 1
    while find != -1:
        if i == nth:
            s = s[:find]+repl+s[find + len(sub):]
            i = 0
		#endif
        find = s.find(sub, find + len(sub) + 1)
        i += 1
	#endwhile
    return s
#endDef


root = Tk()
root.title("Dice Roller")
root.geometry(f'{rootW}x{rootH}')
root.configure(bg=mainColour)
root.resizable("false","false")
wm.append(root)

#ScrollFrame class from https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01
class ScrollFrame(Frame):
	def __init__(self, parent, width=0, height=0, background="#FFFFFF"):
		self.width=width
		self.height=height
		self.background=background

		super().__init__(parent) # create a frame (self)

		self.canvas = Canvas(self, borderwidth=0, background=self.background, width=self.width, height=self.height)	#place canvas on self
		self.viewPort = Frame(self.canvas, background=self.background)			#place a frame on the canvas, this frame will hold the child widgets 
		self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)	#place a scrollbar on self 
		self.canvas.configure(yscrollcommand=self.vsb.set)					#attach scrollbar action to scroll of canvas

		self.vsb.pack(side="right", fill="y")								#pack scrollbar to right of self
		self.canvas.pack(side="left", fill="both", expand=True)				#pack canvas to left of self and expand to fill
		self.canvas_window = self.canvas.create_window((0,0), window=self.viewPort, anchor="nw", tags="self.viewPort") #add view port frame to canvas

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
		canvas_height = self.canvas.winfo_height()
		rows_height = self.canvas.bbox("all")[3]

		if rows_height > canvas_height:
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
		overwrite(d[die], "0")
		overwrite(m[die], "+0")
	#endfor
	nameEntry.delete(0, END)
	totText.delete("1.0", END)
	overwrite(output, "All dice and modifiers reset to zero.")
#enddef

def roll():
	output.delete(1.0, END)
	rollTotal = 0
	if nameEntry.get() != "":
		vowels = ['a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U'] #grandma is impotent
		if nameEntry.get()[:1] in vowels:
			output.insert(END, f'==You made an {nameEntry.get()} roll==\n\n')
		else:
			output.insert(END, f'==You made a {nameEntry.get()} roll==\n\n')
		#endif
	else:
		output.insert(END, f'==You made an unnamed roll==\n\n')
	#endif
	diceRolled=0
	for die in 4, 6, 8, 10, 12, 20, 100, 1:
		i=0
		sub = 0
		numRolls = d[die].get()
		modi = int(m[die].cget("text"))

		if numRolls != "":
			if int(numRolls) <= 0:
				overwrite(d[die], "0")
			#endif
			if int(numRolls) > 20:
				overwrite(d[die], "20")
			#endif
			if numRolls != "0":
				if die == 1:
					if int(sizeX.get()) == 0:
						output.insert(END, f'You asked to roll {numX.get()}d0. I can\'t roll a zero-sided die.')
						break
					elif int(sizeX.get()) > 1000:
						overwrite(output, f'You asked to roll {numX.get()}d{sizeX.get()}. The maximum size for the custom die is 1000.')
						overwrite(totText, "")
						return
					else:
						output.insert(END, f'[{numRolls}d{int(sizeX.get())}')
					#endif
				else:
					output.insert(END, f'[{numRolls}d{die}')
				#endif
				if modi > 0:
					output.insert(END, f' +{modi}]\nRolls: ')
				elif modi < 0:
					output.insert(END, f' {modi}]\nRolls: ')
				else:
					output.insert(END, "]\nRolls: ")
				#endif
			#endif
			while i < int(numRolls):
				diceRolled+=1
				i += 1
				if die == 1:
					newRoll = random.randint(1,int(sizeX.get()))
				else:
					newRoll = random.randint(1,die)
				#endif
				output.insert(END, f'{newRoll}')
				sub += newRoll

				if i == int(numRolls): #we've finished rolling this die
					output.insert(END, "\n")
					output.insert(END, f'Rolled total: {sub}\n')

					if modi != 0:
						if modi > 30:
							m[die].config(text="+30")
							modi = 30
						elif modi < -30:
							m[die].config(text="-30")
							modi = -30
						#endif

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
	overwrite(totText, f'Total: {rollTotal}')
	#endfor
	if diceRolled==0:
		overwrite(output, "No dice were selected to roll.")
	elif logging.get()==1:
		timestamp=time.strftime("%H:%M:%S", time.localtime(time.time()))
		global rollLog
		numLines=int(output.index(END).split('.')[0])
		lastRoll=output.get("1.0", f'{numLines - 2}.0').strip('=')
		rollLog+=f'=={timestamp}, {lastRoll}\n================\n\n'
		#rollLog+="\n\n================\n"
#enddef

def incMod(event, num): #increment/decrement modifier
	curVal = int(m[num].cget("text")) #get current modifier value
	newVal = curVal + 1 if event.num == 1 or event.delta > 0 else curVal - 1 #increment if left-clicked or scrolled up, otherwise decrement
	if newVal > 30 or newVal < -30:
		return
	#endif
	m[num].config(text=(f"+" if newVal >= 0 else "") + str(newVal)) #prepend a "+" for a positive number, then cast it to a string and put it in the box
#enddef

def overwrite(field, string):
	if isinstance(field, ttk.Entry) or isinstance(field, Entry):
		field.delete(0, END)
		field.insert(END, string)
	elif isinstance(field, Text):
		field.delete("1.0", END)
		field.insert(END, string)
	elif isinstance(field, Label):
		field.config(text=string)
	#endif
#endDef

#images need to exist outside setupDie() to avoid being removed by GC.
img4 = ImageTk.PhotoImage(Image.open(resource_path("d4.png")).resize((75,75)))
img6 = ImageTk.PhotoImage(Image.open(resource_path("d6.png")).resize((75,75)))
img8 = ImageTk.PhotoImage(Image.open(resource_path("d8.png")).resize((75,75)))
img10 = ImageTk.PhotoImage(Image.open(resource_path("d10.png")).resize((75,75)))
img12 = ImageTk.PhotoImage(Image.open(resource_path("d12.png")).resize((75,75)))
img20 = ImageTk.PhotoImage(Image.open(resource_path("d20.png")).resize((75,75)))
img100 = ImageTk.PhotoImage(Image.open(resource_path("d100.png")).resize((75,75)))
imgX = ImageTk.PhotoImage(Image.open(resource_path("d1.png")).resize((75,75)))

#define dictionaries. d is number of rolls per die Entry widgets, m is modifier Label fields, i is PhotoImage instances.
#d = {4: num4, 6: num6, 8:num8, 10:num10, 12:num12, 20:num20, 100:num100, 1:numX, 2:sizeX}
#m = {4:modLbl4, 6:modLbl6, 8:modLbl8, 10:modLbl10, 12:modLbl12, 20:modLbl20, 100:modLbl100, 1:modLblX}
d = {}
m = {}
c = {}
i = {4:img4, 6:img6, 8:img8, 10:img10, 12:img12, 20:img20, 100:img100, 1:imgX}

#Style code for Entry widget background, from https://stackoverflow.com/questions/17635905/ttk-entry-background-colour
global estyle
estyle = ttk.Style()
estyle.element_create("plain.field", "from", "clam")
estyle.layout("EntryStyle.TEntry",
                   [('Entry.plain.field', {'children': [(
                       'Entry.background', {'children': [(
                           'Entry.padding', {'children': [(
                               'Entry.textarea', {'sticky': 'nswe'})],
                      'sticky': 'nswe'})], 'sticky': 'nswe'})],
                      'border':'2', 'sticky': 'nswe'})])
estyle.configure("EntryStyle.TEntry",
                 background=accentColour, 
                 foreground="white",
                 fieldbackground=accentColour)


def setupDie(dieSize, columnIndex):
	#img = ImageTk.PhotoImage(Image.open(resource_path("d4.png")).resize((75,75)))
	canv = Canvas(dFrame, width=75, height=75, bg=accentColour, bd=0, highlightthickness=0)
	wa.append(canv)

	canv.create_image(0, 0, image=i[dieSize], anchor=NW)
	canv.bind("<Button-1>", lambda event, mode="plus": mod(mode, dieSize))
	canv.bind("<Button-2>", lambda event, mode="minus": mod(mode, dieSize))
	canv.bind("<Button-3>", lambda event, mode="minus": mod(mode, dieSize))
	canv.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "num", dieSize))
	canv.grid(row=0, column=columnIndex, columnspan=2, sticky=EW)

	c[dieSize] = canv

	d[dieSize] = ttk.Entry(dFrame, width = 8, justify=CENTER, style="EntryStyle.TEntry")
	d[dieSize].insert(0,"0")
	d[dieSize].grid(row=1, column=columnIndex, columnspan=2, pady=8)

	m[dieSize] = Label(dFrame, width=3, text="+0", justify=CENTER, background=accentColour, foreground="white", borderwidth=2, relief="ridge", font=(12))
	m[dieSize].bind("<Button-1>", lambda event: incMod(event, dieSize))
	m[dieSize].bind("<Button-2>", lambda event: incMod(event, dieSize))
	m[dieSize].bind("<Button-3>", lambda event: incMod(event, dieSize))
	m[dieSize].bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "mod", dieSize))
	m[dieSize].grid(row=2, column=columnIndex, columnspan=2)
	wa.append(m[dieSize])
#endDef

###Start actually creating things on root() now.

#frame to hold the die rollers
dFrame = Frame(root, bg=mainColour)
dFrame.place(anchor=NW, x=10, y=10)
wm.append(dFrame)

columnIndex=0
for die in 4, 6, 8, 10, 12, 20, 100:
	setupDie(die, columnIndex)
	line = ttk.Separator(dFrame, orient='vertical').grid(row = 0, column=columnIndex+2, rowspan=20, sticky="ns", padx=10)
	columnIndex+=3
#endfor

#XdY has to be configured manually because it's different to the other dice
imgX = ImageTk.PhotoImage(Image.open(resource_path("d1.png")).resize((75,75)))

canX = Canvas(dFrame, width=75, height=75, bg=accentColour, bd=0, highlightthickness=0)
canX.create_image(0, 0, image=imgX, anchor=NW)
wa.append(canX)

canX.bind("<Button-1>", lambda event, mode="plus": mod(mode, 1))
canX.bind("<Button-2>", lambda event, mode="minus": mod(mode, 1))
canX.bind("<Button-3>", lambda event, mode="minus": mod(mode, 1))
canX.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "num", 1))
canX.grid(row=0, column=21, columnspan=3, sticky=EW)

numX = ttk.Entry(dFrame, width = 3, justify=CENTER, style="EntryStyle.TEntry")
numX.insert(0,"0")
numX.grid(row = 1, column=21, pady=8)
wa.append(numX)

labelXSize = Label(dFrame, text="d", width=1, background=mainColour, foreground="white")
labelXSize.grid(row=1, column=22) #, sticky=E)
wm.append(labelXSize)

sizeX = ttk.Entry(dFrame, width = 3, justify=CENTER, style="EntryStyle.TEntry")
sizeX.insert(0,"0")
sizeX.grid(row = 1, column=23, pady=3)
wa.append(sizeX)

modLblX = Label(dFrame, width=3, text="+0", justify=CENTER, background=accentColour, foreground="white", borderwidth=2, relief="ridge", font=(12))
modLblX.bind("<Button-1>", lambda event: incMod(event, 1))
modLblX.bind("<Button-2>", lambda event: incMod(event, 1))
modLblX.bind("<Button-3>", lambda event: incMod(event, 1))
modLblX.bind("<MouseWheel>", lambda event: mouse_wheel_handler(event, "mod", 1))
modLblX.grid(row=2, column=21, columnspan=3)
wa.append(modLblX)

d[1]=numX
d[2]=sizeX
m[1]=modLblX
c[1] = canX

### End of dice setup

line = ttk.Separator(root, orient='horizontal').place(y=155, relwidth=1.0)

#testBtn = Button(root, text="dick", command= setMain).place(x=50, y=170)

rollBtn = Button(root, text="Roll!", command=roll)
rollBtn.place(x=10, y=170)

def removeFromList(deadObj, list):
	newList = []
	for obj in list:
		if obj != deadObj:
			newList.append(obj)
		#endif
	#endFor
	return newList
#endDef

def cleanupLists(list):
	newList = []
	for obj in list:
		idList = []
		for obj2 in newList:
			idList.append(id(obj2))
		#endfor
		if id(obj) not in idList:
			newList.append(obj)
		#endif
	#endFor
	return newList
#endDef

def addToList(item, list):
	idList = []
	for obj in list:
		idList.append(id(obj))
	#endfor
	if id(item) not in idList:
		list.append(item)
	#endif
	return list
#endDef

def colour():
	global dRed, dGreen, dBlue, mRed, mGreen, mBlue, aRed, aGreen, aBlue, estyle, mainColour, accentColour, wa, wm
	print(f'=before= wa: {str(len(wa))}, wm: {str(len(wm))}')
	wa = cleanupLists(wa)
	wm = cleanupLists(wm)
	print(f'=after= wa: {str(len(wa))}, wm: {str(len(wm))}\n')

	##colouring dice
	for die in (4, 6, 8, 10, 12, 20, 100, 1):
		imgString = f'd{die}.png'
		img=ImageTk.Image.open(resource_path(imgString)).resize((75,75))
		draw = img.load()
		width, height = img.size
		
		for x in range(width):
			for y in range(height):
				rgb=draw[x,y]
				rgb=str(rgb).strip('()').split(',')
				p=0
				while p < len(rgb):
					rgb[p] = int(rgb[p])
					p+=1
				#endwhile
				if rgb[3] == 255 and rgb[0] > 150 and rgb[1] > 150 and rgb[2] > 150: #the visible and not-black-ish pixels
					draw[x,y] = (int(dRed), int(dGreen), int(dBlue), 255)
				#endIf
			#endFor
		#endFor
		tkimg = ImageTk.PhotoImage(img)
		i[die]=tkimg
		c[die].create_image(0, 0, image=i[die], anchor=NW)
	#endFor

	mainColour='#%02x%02x%02x' % (int(mRed), int(mGreen), int(mBlue))
	accentColour='#%02x%02x%02x' % (int(aRed), int(aGreen), int(aBlue))

	##colouring widgets
	for obj in wm:
		try:
			#print("colouring (main) " + str(obj))
			if isinstance(obj, Checkbutton):
				obj.config(bg=mainColour, activebackground=mainColour)
			else:
				obj.configure(bg=mainColour)
			#endif
		except:
			pass
	#endfor
	for obj in wa:
		try:
			#print("colouring (accent) " + str(obj))
			if isinstance(obj, ttk.Entry):
				estyle.configure("EntryStyle.TEntry", background=accentColour, fieldbackground=accentColour)
				obj.configure(style="EntryStyle.TEntry")
			elif isinstance(obj, Checkbutton):
				obj.configure(selectcolor=accentColour)
			elif isinstance(obj, ScrollFrame):
				obj.configure(background=accentColour)
			else:
				obj.configure(bg=accentColour)
			#endif
		except:
			pass
	#endfor
#endDef

zeroBtn = Button(root, text="Reset", command=zeroDice, width=10)
zeroBtn.place(x=765, y=170, anchor=NE)

def saveMacro():
	macString=""
	name=nameEntry.get()
	if name == "":
		overwrite(output, "You must enter a name to save a macro.")
		return
	#endif
	if len(name) > 15:
		name=name[:15]
	#endif
	#this is also handled by the bindings on nameEntry, but if you're quick you can sneak another character in. This will ignore that extra character.

	macFile = open(resource_path("macros.ini"), "r")
	macContents = macFile.readlines()
	for macro in macContents:
		macName = macro.split(',')[0]
		if macName == name:
			overwrite(output, f'There is already a macro saved named {name}.\n\nMacros must have a unique name.')
			return
		#endif
	#endfor
	macFile.close()
	for die in 4, 6, 8, 10, 12, 20, 100, 1:
		size=0
		num=d[die].get()
		mod=m[die].cget("text")
		if die == 1:
			size=d[2].get()
			if int(size) > 1000:
				overwrite(output, f'You asked to save a macro with a {num}d{size} roll.\n\nThe maximum size for the custom die is 1000.')
				return
			#endif
		#endif
		if num == "0": #skip this die size if we're not rolling it
			continue
		else:
			if macString == "":
				macString=f'{name},'
			#endif
			if size != 0: #if size is set, it's an XdY roll
				macString+=f'{str(num)},{str(die)},{str(size)},{str(mod)},'
			else:
				macString+=f'{str(num)},{str(die)},{str(mod)},'
			#endif
		#endif
	#endFor
	#print(f'Saving macro: {macString}')
	if macString=="":
		overwrite(output, "You must specify at least one die to save a macro.")
		return
	#endif
	macString = macString[:-1]
	macFile = open(resource_path("macros.ini"),"a")
	macFile.write(f'{macString}\n')
	macFile.close()
	overwrite(output, f'Macro \"{name}\" was saved successfully.')
	refreshMacWdw()
#destr

def refreshMacWdw():
	root.update()
	if root.winfo_height() > rootH: #if bigger than starting size we are showing macros already.
		showMacFrame() #this will hide the frame
		root.update()
		showMacFrame() #this will re-open it
	#endif
#endDef

def truncName(event):
	name=nameEntry.get() #get the current macro name
	if len(name) > 15:
		cleanedName=nameEntry.get()[:15] #truncate to 15 chars if currently over
		overwrite(nameEntry, cleanedName)
	#endif
#endDef

nameFrame = Frame(root, width=700, height=20, bg=mainColour)
nameFrame.place(x=0, y=210)
wm.append(nameFrame)
nameLbl = Label(nameFrame, text="Roll Name:", bg=accentColour, fg="white", borderwidth=2, relief=SUNKEN)
nameLbl.grid(row=0, column=0, padx=10)
wa.append(nameLbl)
nameEntry = Entry(nameFrame, bg=accentColour, fg="white")
nameEntry.bind("<KeyRelease>", lambda event: truncName(event))
wa.append(nameEntry)
#nameEntry.bind("<KeyRelease>", truncName())
nameEntry.grid(row=0, column=1)
saveMac = Button(nameFrame, text="Save macro", command=saveMacro)
saveMac.grid(row=0, column=2, padx=20)

outFrame = Frame(root, width=755, height=200)
outFrame.place(x=10, y=245)
output = Text(outFrame, height=1, width=1, bg=accentColour, fg="white")
output.place(relwidth=1.0, relheight=1.0)
wa.append(output)
output.insert(END, "Assign the number of dice to roll above, then click \"Roll\"!\n\nPlease click the  help button below for more usage information.")

totFrame = Frame(root, width = 100, height = 20)
totFrame.place(x=10, y=450, anchor=NW)
totText = Text(totFrame, height=1, width=1, bg=accentColour, fg="white")
totText.place(relwidth=1.0, relheight=1.0)
wa.append(totText)

logging = IntVar()
logChk = Checkbutton(root, text="Log rolls", variable=logging, bg=mainColour, onvalue=1, offvalue=0, fg="white", selectcolor=accentColour, activebackground=mainColour, activeforeground="white", borderwidth=1, relief=GROOVE, padx=5)
logChk.place(x=600, y=450, anchor=NW)
wm.append(logChk)
wa.append(logChk)

def showLogWdw():
	global rollLog
	try:
		global logWdw
		if logWdw.winfo_exists():
			pass
		else:
			logWdw = Toplevel(root)
	except NameError:
		logWdw = Toplevel(root)
	#endtry
	logWdw.title("Log of Completed Rolls")
	root.update()
	rootX = root.winfo_x()
	rootY = root.winfo_y()
	rootH = root.winfo_height()
	rootW = root.winfo_width()

	logWdw.geometry("%dx%d+%d+%d" % (800, 400, (rootX+(rootW/2)-400), rootY+(rootH/2)-200))
	logWdw.configure(bg=mainColour)
	logWdw.resizable("false","true")
	logWdw.update()
	logFrame = Frame(logWdw, bg=mainColour, width=int(logWdw.winfo_width())-10, height=int(logWdw.winfo_height())-10)
	logFrame.place(x=5, y=5, anchor=NW)
	logFrame.update()
	logScrollFrame = ScrollFrame(logFrame, width=logFrame.winfo_width(), height=logFrame.winfo_height())
	logScrollFrame.place(x=0, y=0)

	logText = Text(logScrollFrame.viewPort, bg=accentColour, fg="white", width=90)
	logText.grid(row=0, column=0)
	logText.insert("1.0", rollLog)
#endDef

showLogBtn = Button(root, text="Show Log", command=showLogWdw)
showLogBtn.place(x=697, y=450, anchor=NW)

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
	root.update()
	rootX = root.winfo_x()
	rootY = root.winfo_y()
	rootH = root.winfo_height()
	rootW = root.winfo_width()

	helpWdw.geometry("%dx%d+%d+%d" % (800, 400, (rootX+(rootW/2)-400), rootY+(rootH/2)-200))
	helpWdw.configure(bg=mainColour)
	helpWdw.resizable("false","false")
	
	helpTxt = Text(helpWdw, bg=mainColour, borderwidth=0, fg="white")
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

def loadOpts(): #this function only loads the options into the variables.
	global dRed, dGreen, dBlue
	global mRed, mGreen, mBlue
	global aRed, aGreen, aBlue

	try:
		optsFile = open(resource_path("config.ini"), "r")
	except FileNotFoundError:
		optsFile = open(resource_path("config.ini"), "w")
		optsFile.close()
		loadOpts() #create the file, then re-open this function
		return

	options=optsFile.readlines()
	optsFile.close()
	if options=="":
		dRed="255"
		dGreen="255"
		dBlue="255"

		mRed="27"
		mGreen="31"
		mBlue="26"

		aRed="59"
		aGreen="63"
		aBlue="58"

		return
	#endif
	for optionLine in options:
		option=optionLine.split(",")
		if option[0]=="[dice]":
			dRed=option[1]
			dGreen=option[2]
			dBlue=option[3].strip("\n")
		elif option[0]=="[main]":
			mRed=option[1]
			mGreen=option[2]
			mBlue=option[3].strip("\n")
		elif option[0]=="[accent]":
			aRed=option[1]
			aGreen=option[2]
			aBlue=option[3].strip("\n")
	#endFor
	#colour() #this is needed so when we reset colours, they apply instantly.
	mainColour='#%02x%02x%02x' % (int(mRed), int(mGreen), int(mBlue))
	accentColour='#%02x%02x%02x' % (int(aRed), int(aGreen), int(aBlue))
#endDef

loadOpts()
colour()

def showOptsWdw():
	global dRed, dGreen, dBlue
	global mRed, mGreen, mBlue
	global aRed, aGreen, aBlue

	loadOpts()

	try:
		global optsWdw
		if optsWdw.winfo_exists():
			pass
		else:
			optsWdw = Toplevel(root)
	except NameError:
		optsWdw = Toplevel(root)
	#endtry
	optsWdw.title("Dice Roller Options")
	root.update()
	rootX = root.winfo_x()
	rootY = root.winfo_y()
	rootH = root.winfo_height()
	rootW = root.winfo_width()

	optsWdw.geometry("%dx%d+%d+%d" % (500, 200, (rootX+(rootW/2)-300), rootY+(rootH/2)-80))
	optsWdw.configure(bg=mainColour)
	wm.append(optsWdw)
	optsWdw.resizable("false","false")
	optsWdw.update()

	optsFrame = Frame(optsWdw, bg=mainColour)
	optsFrame.place(x=5, y=5, width=optsWdw.winfo_width()-10, height=optsWdw.winfo_height()-10)
	wm.append(optsFrame)

	dColLbl = Label(optsFrame, text="Colour Options", borderwidth=2, relief=RIDGE, bg=accentColour, fg="white", font=("arial", 14))
	dColLbl.grid(row=0, column=0, columnspan=4, pady=5)
	
	#headings
	RedLbl = Label(optsFrame, text="R", bg=accentColour, fg="white", width=6)
	GreenLbl = Label(optsFrame, text="G", bg=accentColour, fg="white", width=6)
	BlueLbl = Label(optsFrame, text="B", bg=accentColour, fg="white", width=6)
	RedLbl.grid(row=1, column=1, sticky=E, padx=5)
	GreenLbl.grid(row=1, column=2, padx=5)
	BlueLbl.grid(row=1, column=3, padx=5)
	for lbl in (RedLbl, GreenLbl, BlueLbl):
		wa.append(lbl)
	#endfor
	
	#dice colours
	dLbl = Label(optsFrame, text="Dice:", width=10, bg=mainColour, fg="white")
	dLbl.grid(row=2, column=0, pady=5, sticky=W)
	wm.append(dLbl)
	dRedEnt = Entry(optsFrame, width=6)
	dGreenEnt = Entry(optsFrame, width=6)
	dBlueEnt = Entry(optsFrame, width=6)
	dRedEnt.grid(row=2, column=1, padx=5, sticky=E)
	dGreenEnt.grid(row=2, column=2, padx=5)
	dBlueEnt.grid(row=2, column=3, padx=5)
	
	#main app colour
	mLbl = Label(optsFrame, text="App:", width=10, bg=mainColour, fg="white")
	mLbl.grid(row=3, column=0, pady=5, sticky=W)
	wm.append(mLbl)
	mRedEnt = Entry(optsFrame, width=6)
	mGreenEnt = Entry(optsFrame, width=6)
	mBlueEnt = Entry(optsFrame, width=6)
	mRedEnt.grid(row=3, column=1, padx=5, sticky=E)
	mGreenEnt.grid(row=3, column=2, padx=5)
	mBlueEnt.grid(row=3, column=3, padx=5)

	#accent app colour
	aLbl = Label(optsFrame, text="Accent:", width=10, bg=mainColour, fg="white")
	aLbl.grid(row=4, column=0, pady=5, sticky=W)
	wm.append(aLbl)
	aRedEnt = Entry(optsFrame, width=6)
	aGreenEnt = Entry(optsFrame, width=6)
	aBlueEnt = Entry(optsFrame, width=6)
	aRedEnt.grid(row=4, column=1, padx=5, sticky=E)
	aGreenEnt.grid(row=4, column=2, padx=5)
	aBlueEnt.grid(row=4, column=3, padx=5)

	overwrite(dRedEnt, dRed)
	overwrite(dGreenEnt, dGreen)
	overwrite(dBlueEnt, dBlue)

	overwrite(mRedEnt, mRed)
	overwrite(mGreenEnt, mGreen)
	overwrite(mBlueEnt, mBlue)

	overwrite(aRedEnt, aRed)
	overwrite(aGreenEnt, aGreen)
	overwrite(aBlueEnt, aBlue)

	def saveOpts(): #this function only saves the options to file. It calls loadOpts() to load those values back into variables.
		for ent in (dRedEnt, dGreenEnt, dBlueEnt, mRedEnt, mGreenEnt, mBlueEnt, aRedEnt, aGreenEnt, aBlueEnt):
			if int(ent.get()) > 255:
				overwrite(ent, "255")
			elif int(ent.get()) < 0:
				overwrite(ent, "0")
			#endif
		#endFor

		optsFile = open(resource_path("config.ini"), "w")
		dRGB = f'[dice],{dRedEnt.get()},{dGreenEnt.get()},{dBlueEnt.get()}'
		mRGB = f'[main],{mRedEnt.get()},{mGreenEnt.get()},{mBlueEnt.get()}'
		aRGB = f'[accent],{aRedEnt.get()},{aGreenEnt.get()},{aBlueEnt.get()}'

		optsFile.write(dRGB+"\n")
		optsFile.write(mRGB+"\n")
		optsFile.write(aRGB)
		optsFile.close()

		optsOutLbl.config(text="Options saved.")
		loadOpts()
		colour()
	#endDef

	optsWdw.update()
	saveOptsBtn = Button(optsWdw, text="Save", command=saveOpts)
	saveOptsBtn.update()
	saveOptsBtn.place(x=optsWdw.winfo_width()-saveOptsBtn.winfo_width()-10, y=optsWdw.winfo_height()-saveOptsBtn.winfo_height()-10, anchor=SE)

	def loadDefaults():
		for dieEnt in (dRedEnt, dGreenEnt, dBlueEnt):
			overwrite(dieEnt, "255")
		#endFor
		overwrite(mRedEnt, "27")
		overwrite(mGreenEnt, "31")
		overwrite(mBlueEnt, "26")
		overwrite(aRedEnt, "59")
		overwrite(aGreenEnt, "63")
		overwrite(aBlueEnt, "58")

	defaultOptsBtn = Button(optsWdw, text="Load Defaults", command=loadDefaults)
	defaultOptsBtn.update()
	defaultOptsBtn.place(x=saveOptsBtn.winfo_x()-10, y=saveOptsBtn.winfo_y(), anchor=NE)
	defaultOptsBtn.update()

	#line = ttk.Separator(optsWdw, orient='horizontal')
	#line.update()

	optsOutLbl = Label(optsWdw, text="", bg=mainColour, fg="yellow", borderwidth="2", relief=RIDGE)
	optsOutLbl.update()
	optsOutLbl.place(x=defaultOptsBtn.winfo_x(), y=defaultOptsBtn.winfo_y()-(defaultOptsBtn.winfo_height()), width=optsWdw.winfo_width()-defaultOptsBtn.winfo_x()-10)
	wm.append(optsOutLbl)

	loadOpts()
#endDef

optionsBtn = Button(root, text="Options", command=showOptsWdw)
helpBtn.update()
optionsBtnX = helpBtn.winfo_x()-optionsBtn.winfo_width()-5
optionsBtn.place(x=optionsBtnX, y=540, anchor=SE)

'''
#=============
	macroBtn.config(text="Hide Macro Pane")
	rootH=str(root.winfo_height())
	rootW=str(root.winfo_width())
	newH=str(int(rootH) + 300)
	root.geometry(f'{rootW}x{newH}')
	
	#loadOpts()
	#macLoadImg = PhotoImage(file=resource_path("up-arrow.png"))
	#macRollImg = PhotoImage(file=resource_path("up-arrow-dice.png"))
	#macDelImg = PhotoImage(file=resource_path("delete-dice.png"))
	
	macDropDown = Frame(root, bg=mainColour, width=int(rootW)-10, height=295)
	macDropDown.place(x=5, y=rootH)
	line = ttk.Separator(macDropDown, orient='horizontal').place(y=0, relwidth=1.0)
	macFrame = ScrollFrame(macDropDown, width=427, height=295, background=accentColour)
	macFrame.place(x=0, y=2)
	wa = addToList(macFrame.viewPort, wa)
	#wa.append(macFrame.viewPort)
	
	showMacros(macFrame)

	#line = ttk.Separator(macDropDown, orient='vertical').place(x=450, relheight=1.0)
	
	macHelp = Text(macDropDown, height=15, width=34, bg=mainColour, borderwidth=0, fg="white", font=("Arial Narrow", "12"), wrap=WORD)
	macHelp.place(y=2, x=455)
	wm.append(macHelp)
	macHelp.insert("1.0", "==Macro Pane Usage==\n\nYour saved macros are shown on the left, if you have any.\n\n\
  =Load=\nLoad the saved dice values and roll name into the main window.\n\n\
  =Roll=\nAs above, but immediately perform a roll of the saved dice.\n\n\
  =Delete=\nNobody knows what this button does...")
	macHelp.tag_configure("centeredText", justify="center")
	macHelp.tag_add("centeredText", 1.0, END)'''

class macroFrame(ScrollFrame):
	def __init__(ScrollFrame, parent, width, height):
		self.parent = parent
		self.rows = 0
		self.width = width
		self.height = height
		self.macFrame = Frame(parent, bg=accentColour, width=width, height=height).place(x=5, y=5, anchor=NW)

		macLoadImg = PhotoImage(file=resource_path("up-arrow.png"))
		macRollImg = PhotoImage(file=resource_path("up-arrow-dice.png"))
		macDelImg = PhotoImage(file=resource_path("delete-dice.png"))
	#endDef

	def colourMacros(colour):
		self.macFrame.config(bg=colour)
	#endDef

	def showMacros():
		macFile = open(resource_path("macros.ini"),"r")
		for curMacString in macFile:
			addMacro(curMacString)
		#endfor
		macFile.close()		
	#endDef

	def addMacro(macro):
		row=self.rows
		macro = macro.split(",")
		macName = Label(self.macFrame, text=f'{macro[0]}')
		macName.grid(row=row, column=0)

		macDice = Label(macFrame, width=34, fg="white", bg=accentColour, wraplength=300)

		#build macro string from CSV values
		i = 0
		realSize = 0
		macDiceStr = ""
		while i < len(macro) - 1:
			num=macro[i+1]
			size=macro[i+2]
			if size == "1": #to handle saved XdY rolls
				realSize=macro[i+3]
				mod=macro[i+4]
				macDiceStr+=f'{num}d{realSize} {mod}'
				i+=4
			else:
				mod=macro[i+3]
				macDiceStr+=f'{num}d{size} {mod}'
				i+=3
			#endif
			if i < (len(macro) -1):
				macDiceStr+=f', '
			#endif
		#endwhile

		macDiceStr=replaceN(macDiceStr, ",", "\n", 3) #multiline macros to fit in frame
		overwrite(macDice, macDiceStr)
		macDice.grid(row=row, column=1, padx=5, sticky=EW)

		

		macLoadLbl = Label(macFrame, image=macLoadImg, bg="white")
		macLoadLbl.grid(row=row, column=2, padx=2)
		macLoadTip = Hovertip(macLoadLbl, "Load this macro into the main window", hover_delay=400)

		macLoadLbl.bind("<Button-1>", lambda event: loadMac(macro))

		macRollLbl = Label(macFrame, image=macRollImg, bg="white")
		macRollLbl.grid(row=row, column=3, padx=2)
		macRollTip = Hovertip(macRollLbl, "Load this macro into the main window, and roll it.", hover_delay=400)

		macRollLbl.bind("<Button-1>", lambda event: loadMacAndRoll(macro))

		macDelLbl = Label(macFrame, image=macDelImg, bg="white")
		macDelLbl.grid(row=row, column=4, padx=2, pady=2)
		macDelTip = Hovertip(macDelLbl, "Deletes this macro. This is irreversible.", hover_delay=400)

		macDelLbl.bind("<Button-1>", lambda event: delMac(macName.cget("text")))

		line = ttk.Separator(frameRef.viewPort, orient='horizontal').grid(row=row+1, column=0, columnspan=5, sticky=EW)

		self.rows+=2
	#endDef

	#=======================

macFrame = macroFrame(root, width=427, height=295)
macFrame.place(x=5, y=root.winfo_height()+5)

'''
macDropDown = Frame(root, bg=mainColour, width=int(rootW)-10, height=295)
	macDropDown.place(x=5, y=rootH)
	line = ttk.Separator(macDropDown, orient='horizontal').place(y=0, relwidth=1.0)
	macFrame = ScrollFrame(macDropDown, width=427, height=295, background=accentColour)
	macFrame.place(x=0, y=2)

def showMacFrame():
	global macLoadImg, macRollImg, macDelImg, wa, wm, accentColour, mainColour #these have to be defined here or they'll be garbage collected from the showMac() function?
	if root.winfo_height()>600: # a kludge to see if the macros are showing already or not.
		root.geometry("775x550")
		macroBtn.config(text="Show Macro Pane")
		return
	#endif

	macroBtn.config(text="Hide Macro Pane")
	rootH=str(root.winfo_height())
	rootW=str(root.winfo_width())
	newH=str(int(rootH) + 300)
	root.geometry(f'{rootW}x{newH}')
#endDef'''

'''
	def showMacros(macFrame):
		global wa
		row=0
		macFile = open(resource_path("macros.ini"),"r")
		for curMacString in macFile:
			curMacList = curMacString.split(',')
			curMacDisplay = macroDisplay(macFrame, macLoadImg, macRollImg, macDelImg, curMacList, row, accentColour)
			#showMac(curMacList, row, macFrame, macLoadImg, macRollImg, macDelImg, wa)
			row+=2
		#endfor
		macFile.close()
	#endDef

	def showMac(macro, row, frameRef, macLoadImg, macRollImg, macDelImg, wa):
		global mainColour, accentColour
		loadOpts()
		macName = Label(frameRef.viewPort, text=f'{macro[0]}')
		macName.grid(row=row, column=0, sticky=EW, padx=5, pady=3)
		macDice = Label(frameRef.viewPort, width=34, fg="white", bg=accentColour, wraplength=300)
		wa = addToList(macDice, wa)
		i = 0
		realSize = 0
		macDiceStr = ""
		while i < (len(macro) - 1):
			num=i+1
			size=i+2
			if macro[size] == "1": #to handle saved XdY rolls
				realSizeIndex=i+3
				realSize=macro[realSizeIndex]
				mod=i+4
				#macDice.insert(END, f'{macro[num]}d{realSize} {macro[mod]}')
				macDiceStr+=f'{macro[num]}d{realSize} {macro[mod]}'
				i+=4
			else:
				mod=i+3
				#macDice.insert(END, f'{macro[num]}d{macro[size]} {macro[mod]}')
				macDiceStr+=f'{macro[num]}d{macro[size]} {macro[mod]}'
				i+=3
			#endif
			if i < (len(macro) -1):
				#macDice.insert(END, f', ')
				macDiceStr+=f', '
			#endif
		#endwhile
		
		macDiceStr=replaceN(macDiceStr, ",", "\n", 3)
		overwrite(macDice, macDiceStr)
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
		macDelTip = Hovertip(macDelLbl, "Deletes this macro. This is irreversible.", hover_delay=400)

		macDelLbl.bind("<Button-1>", lambda event: delMac(macName.cget("text")))

		line = ttk.Separator(frameRef.viewPort, orient='horizontal').grid(row=row+1, column=0, columnspan=5, sticky=EW)
	
	#endDef


	
	loadOpts()
	macLoadImg = PhotoImage(file=resource_path("up-arrow.png"))
	macRollImg = PhotoImage(file=resource_path("up-arrow-dice.png"))
	macDelImg = PhotoImage(file=resource_path("delete-dice.png"))
	
	macDropDown = Frame(root, bg=mainColour, width=int(rootW)-10, height=295)
	macDropDown.place(x=5, y=rootH)
	line = ttk.Separator(macDropDown, orient='horizontal').place(y=0, relwidth=1.0)
	macFrame = ScrollFrame(macDropDown, width=427, height=295, background=accentColour)
	macFrame.place(x=0, y=2)
	wa = addToList(macFrame.viewPort, wa)
	#wa.append(macFrame.viewPort)
	
	showMacros(macFrame)

	#line = ttk.Separator(macDropDown, orient='vertical').place(x=450, relheight=1.0)
	
	macHelp = Text(macDropDown, height=15, width=34, bg=mainColour, borderwidth=0, fg="white", font=("Arial Narrow", "12"), wrap=WORD)
	macHelp.place(y=2, x=455)
	wm.append(macHelp)
	macHelp.insert("1.0", "==Macro Pane Usage==\n\nYour saved macros are shown on the left, if you have any.\n\n\
  =Load=\nLoad the saved dice values and roll name into the main window.\n\n\
  =Roll=\nAs above, but immediately perform a roll of the saved dice.\n\n\
  =Delete=\nNobody knows what this button does...")
	macHelp.tag_configure("centeredText", justify="center")
	macHelp.tag_add("centeredText", 1.0, END)

	colour()
#endDef'''

macroBtn = Button(root, text="Show Macro Pane", command= showMacFrame)
macroBtn.place(x=10, y=540, anchor=SW)

def loadMac(macro): #loads the dice values from a saved macro into the roller.
	zeroDice()
	macName = macro[0]
	overwrite(output, f'Macro "{macName}" loaded.')
	i=0
	overwrite(nameEntry, macName)
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
		overwrite(d[macSize], macNum)
		if realSize != 0: #realSize is only set if "size" is 1, indicating an XdY roll.
			overwrite(d[2], realSize)
		if int(macMod) > 30:
			macMod="+30"
		elif int(macMod) <-30:
			macmMod="-30"
		#endIf
		m[macSize].config(text=f'{macMod.strip('\n')}') #the final mod in the macro ends in a newline in macros.ini; this was putting the newline into the mod field without strip().
	#endWhile
#endDef

def delMac(macName):
	macFile = open(resource_path("macros.ini"),"r")
	macContents = macFile.readlines()
	macFile.close()

	macFile = open(resource_path("macros.ini"), "w")
	for macro in macContents:
		targetMacName = macro.split(',')[0]
		if targetMacName != macName:
			macFile.write(macro)
		#endif
	#endfor
	macFile.close()
	refreshMacWdw()
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
	overwrite(d[num], newNum)
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