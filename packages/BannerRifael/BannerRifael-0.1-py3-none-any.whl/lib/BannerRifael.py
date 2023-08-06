from pyfiglet import *
from termcolor import colored
from random import choice
from time import sleep

def createBanner(msg, color):
		
	
	font = ['slant', "3-d", "3x5", "5lineoblique",
	        "alphabet", "banner3-D", "doh", "isometric1", "letters",
	        "alligator", "dotmatrix", "bubble", "bulbhead", "digital"]
	
	random_choice = choice(font)
	
	
	valid_color = ('red', 'green', 'yellow', 'blue', 'cyan', 'white')
	
	if color not in valid_color:
	    print("\n No color ",color)
	    color = "white"
	    sleep(2)
	    print("\n")
	
	ascii_art = figlet_format(msg, font=random_choice)
	
	colored_ascii = colored(ascii_art, color)
	
	print(colored_ascii)
	
