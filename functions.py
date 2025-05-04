import os
import time
import math
import re
import readchar
from colorama import Fore, Style
from func_faceit_logic import get_players_cs2_elo
from func_faceit_levels import get_elo_color, get_faceit_level

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def strip_ansi(text):
    # Remove ANSI escape sequences for width calculation
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text)

def display_welcome():
    clear_screen()
    print("""
██████████████████████████████████████████████████████████████████████████████████████████████          
██                                                                                          ██  
██   ███████  █████   ██████ ███████ ██ ████████     ████████ ███████  █████  ███    ███    ██   
██   ██      ██   ██ ██      ██      ██    ██           ██    ██      ██   ██ ████  ████    ██                                                                                             
██   █████   ███████ ██      █████   ██    ██           ██    █████   ███████ ██ ████ ██    ██                                                                                      
██   ██      ██   ██ ██      ██      ██    ██           ██    ██      ██   ██ ██  ██  ██    ██                                                                                     
██   ██      ██   ██  ██████ ███████ ██    ██           ██    ███████ ██   ██ ██      ██    ██                                                                                     
██                                                                                          ██  
██                                                                                          ██        
██            █████  ███    ██  █████  ██     ██    ██ ██████  ██████  █████                ██                                                                            
██           ██   ██ ████   ██ ██   ██ ██      ██  ██      ██  ██      ██   ██              ██                                                                            
██           ███████ ██ ██  ██ ███████ ██       ████     ██    █████   ██████               ██                                                                            
██           ██   ██ ██  ██ ██ ██   ██ ██        ██    ██      ██      ██   ██              ██                                                                            
██           ██   ██ ██   ████ ██   ██ ███████   ██    ██████  ██████  ██   ██              ██                                                                            
██                                                                                          ██
██                                       BY SZEWCU                                          ██                                                              
██████████████████████████████████████████████████████████████████████████████████████████████
    """)
    time.sleep(2)  # Pause for 2 seconds to let the user see the title

def get_player_list():
    while True:
        print("\nEnter player nicknames separated by commas:")
        user_input = input().strip()
        if not user_input:
            print("Please enter at least one player nickname.")
            continue
        players = [nick.strip() for nick in user_input.split(',')]
        players = [nick for nick in players if nick]
        if not players:
            print("No valid nicknames found. Please try again.")
            continue
        return players

def display_player_stats(player_ids, api_key, stats_agg, games_data):
    elo_data = get_players_cs2_elo(api_key, player_ids)
    # Build pseudo-table rows
    headers = ["Player", "Faceit Level", "ELO", "Winrate", "K/D", "ADR", "HS%", "Games"]
    table = [headers]
    for _, row in elo_data.iterrows():
        nickname = row['nickname'] if row['nickname'] else "-"
        elo = row['elo']
        winrate, kd, adr, hs_percent, games = stats_agg.get(nickname, ('Not found', 'Not found', 'Not found', 'Not found', 0))
        if elo is not None and not (isinstance(elo, float) and math.isnan(elo)):
            level = get_faceit_level(elo)
            color = get_elo_color(elo)
            level_text = f"{color}Level {level}{Style.RESET_ALL}"
            elo_text = f"{color}{int(elo)}{Style.RESET_ALL}"
            table.append([nickname, level_text, elo_text, str(winrate), str(kd), str(adr), str(hs_percent), str(games)])
        else:
            not_found_msg = f"{Fore.RED}--- Not found ---{Style.RESET_ALL}"
            table.append([nickname, not_found_msg, "", str(winrate), str(kd), str(adr), str(hs_percent), str(games)])
    # Calculate max width for each column (without color codes)
    col_widths = [max(len(strip_ansi(str(row[i]))) for row in table) for i in range(len(headers))]
    # Build and print the table
    sep = "=" * (sum(col_widths) + 3 * (len(headers) - 1) + 2)
    print("\n" + sep)
    for i, row in enumerate(table):
        padded = [str(row[j]) + ' ' * (col_widths[j] - len(strip_ansi(str(row[j])))) for j in range(len(headers))]
        print(" " + " | ".join(padded) + " ")
        if i == 0:
            print(sep)
    print(sep)

def interactive_menu(options):
    idx = 0
    menu_lines = len(options) + 2  # +2 for prompt and blank line
    print('\nSelect an option (use arrows and Enter):\n')
    for i, opt in enumerate(options):
        prefix = '>' if i == idx else ' '
        print(f'{prefix} {opt}')
    while True:
        key = readchar.readkey()
        if key == readchar.key.UP:
            idx = (idx - 1) % len(options)
        elif key == readchar.key.DOWN:
            idx = (idx + 1) % len(options)
        elif key == readchar.key.ENTER:
            return idx
        # Move cursor up to redraw menu
        print(f'\033[{menu_lines}A', end='')
        print('Select an option (use arrows and Enter):\n')
        for i, opt in enumerate(options):
            prefix = '>' if i == idx else ' '
            print(f'{prefix} {opt}')