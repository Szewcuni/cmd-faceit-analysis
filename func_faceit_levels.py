from colorama import init, Fore 

init()

def get_elo_color(elo):
    if elo is None:
        return Fore.RED
    if elo >= 2001:  
        return Fore.RED
    elif elo >= 1531: 
        return Fore.YELLOW
    elif elo >= 901:  
        return Fore.LIGHTYELLOW_EX
    elif elo >= 501:  
        return Fore.GREEN
    elif elo >= 0: 
        return Fore.WHITE
    else:              
        return Fore.WHITE

def get_faceit_level(elo):
    if elo is None:
        return "Not Found"
    if elo >= 2000: return 10
    elif elo >= 1750: return 9
    elif elo >= 1530: return 8
    elif elo >= 1350: return 7
    elif elo >= 1200: return 6
    elif elo >= 1050: return 5
    elif elo >= 900: return 4
    elif elo >= 750: return 3
    elif elo >= 500: return 2
    else: return "Not Found"
