from func_faceit_logic import extract_player_ids,  get_player_stats_aggregate
from colorama import init
from maps_data_charts import analyze_games
from functions import interactive_menu, display_welcome, display_player_stats, get_player_list
# Initialize colorama
init()


def main():
    api_key = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'  # Your API keygit
    display_welcome()
    print("Welcome to the FACEIT Team Analysis Tool!")
    print("This tool will help you analyze team data from FACEIT.")
    players = get_player_list()
    player_ids = extract_player_ids(players, api_key)
    stats_agg, games_data = get_player_stats_aggregate(player_ids, api_key)
    display_player_stats(player_ids, api_key, stats_agg, games_data)
    
    last_chart_lines = 0
    menu_options = ['Analyze all'] + list(games_data.keys()) + ['Exit']
    menu_lines = 2 + len(menu_options)  # 1 for prompt, 1 blank, 1 per option

    while True:
        # Show menu
        choice = interactive_menu(menu_options)

        if choice == len(menu_options) - 1:  # Exit
            print("Exiting... Goodbye!")
            break
        elif choice == 0:
            highlight_label = "ALL PLAYERS"
            last_chart_lines = analyze_games(games_data, highlight_label=highlight_label)
        else:
            highlight_label = menu_options[choice]
            last_chart_lines = analyze_games(games_data, [highlight_label], highlight_label=highlight_label)
        
        input("\nPress Enter to return to the menu...")

        # Clear previous menu + chart area AFTER user presses Enter
        total_clear = menu_lines + last_chart_lines + 3
        if total_clear > 0:
            print(f'\033[{total_clear}A', end='')  # Move cursor up
            for _ in range(total_clear):
                print(' ' * 120)
            print(f'\033[{total_clear}A', end='')  # Move cursor up again

if __name__ == "__main__":
    main()
