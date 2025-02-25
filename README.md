# diceroller
A simple Python dice rolling GUI for RPG/tabletop dice.

## Changelog
### v0.1
Full set of RPG dice are now added and working, with uniform icons. There is now also a separate frame for the total, the dice output is cleaner and simpler, and there's a reset button to set all dice back to zero.

### v0.2
Added the dX roller to allow dice of custom sizes. Also tidied up some filenames.

### v0.3
Added dice modifiers, i.e. 2d6 +3. Button UI may change in future, but it works for now.

### v0.3.1
Changed the modifier UI to be more useful. Got rid of the Entry fields and just used Labels.

### v0.3.2
Added field to name rolls, help button with better usage information, and cleaned up the colours a little bit.

### v0.4
Added macro functionality, and tidied up some colours.

### v0.4.1
Macro bugfix, general code cleanup.

### v0.4.2
Major bugfix in compiled .exe regarding macro file handling.

## Completed features:

 - ~~Add a dX roller, where the user can specify the size of the die to roll (i.e. some games use a d30).~~
	- Added in v0.2.
 - ~~Add a field for modifiers, so you can roll "XdY +Z" and have the "+Z" shown in the output.~~
	- Added in v0.3.
 - ~~Provide a way for the user to "name" their rolls, i.e. a field where you can enter "attack" or "damage", and then have that show in the output when you roll.~~
	- Added in v0.3.2
 - ~~Allow user-created combinations of dice (macros) to be pre-saved. So you can combine a d20 and 2d6 +4, and roll for attack and damage on a single click. These should also be nameable, as above.~~
	- Added in v0.4

## To-do:
 - Allow saving of rolls into a log, and create a clean way for the user to view that log.
 - Allow colorizing of dice icons (currently no idea if this is even possible).
