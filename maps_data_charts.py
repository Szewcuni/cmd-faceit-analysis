from colorama import Fore, Style

def analyze_games(games_data, selected_players=None, highlight_label=None):
    """
    Display two ASCII bar charts: win ratio per map and games count per map, in a nice ASCII frame.
    If selected_players is None, analyze all players.
    highlight_label: string to display as a highlighted header above the chart.
    Returns the number of lines printed (for clearing later).
    """
    lines_printed = 0
    if selected_players is None:
        selected_players = list(games_data.keys())
    map_stats = {}
    for player in selected_players:
        stats_data = games_data.get(player)
        if not stats_data:
            continue
        matches = stats_data.get('items', [])
        for match in matches:
            map_name = match.get('stats', {}).get('Map', 'Unknown')
            if map_name not in map_stats:
                map_stats[map_name] = {'games': 0, 'wins': 0}
            map_stats[map_name]['games'] += 1
            try:
                map_stats[map_name]['wins'] += int(match.get('stats', {}).get('Result', 0))
            except Exception:
                pass
    if not map_stats:
        print("No map data found for the selected player(s).")
        return 1
    # Prepare data for charts
    winratios = []
    games_counts = []
    for map_name, stats in map_stats.items():
        games = stats['games']
        wins = stats['wins']
        winrate = (wins / games) * 100 if games > 0 else 0
        winratios.append((map_name, winrate))
        games_counts.append((map_name, games))
    # Sort
    winratios.sort(key=lambda x: x[1], reverse=True)
    games_counts.sort(key=lambda x: x[1], reverse=True)
    # Bar chart settings
    max_bar = 30
    max_games = max([g for _, g in games_counts], default=1)
    max_winrate = 100
    # Find max map name length for alignment
    max_map_len = max(len(m[0]) for m in winratios + games_counts)
    # Frame width
    win_chart_width = max_map_len + 3 + max_bar + 2 + 8  # map | bar | percent
    games_chart_width = max_map_len + 3 + max_bar + 2 + 10  # map | bar | games
    # Highlighted header
    if highlight_label:
        print(f"{Fore.YELLOW}=== Analyzing: {highlight_label} ==={Style.RESET_ALL}")
        lines_printed += 1
    # Win ratio chart
    print("\n" + "=" * win_chart_width)
    lines_printed += 2
    print(f"|{'Win Ratio by Map:'.center(win_chart_width-2)}|")
    print("|" + "-" * (win_chart_width-2) + "|")
    lines_printed += 2
    for map_name, winrate in winratios:
        bar_len = int((winrate / max_winrate) * max_bar)
        bar = '█' * bar_len
        line = f" {map_name:<{max_map_len}} | {bar:<{max_bar}} {winrate:5.1f}%"
        print(f"|{line:<{win_chart_width-2}}|")
        lines_printed += 1
    print("=" * win_chart_width)
    lines_printed += 1
    # Games count chart
    print(f"|{'Games Played by Map:'.center(games_chart_width-2)}|")
    print("|" + "-" * (games_chart_width-2) + "|")
    lines_printed += 2
    for map_name, games in games_counts:
        bar_len = int((games / max_games) * max_bar) if max_games > 0 else 0
        bar = '█' * bar_len
        line = f" {map_name:<{max_map_len}} | {bar:<{max_bar}} {games} games"
        print(f"|{line:<{games_chart_width-2}}|")
        lines_printed += 1
    print("=" * games_chart_width)
    lines_printed += 1
    return lines_printed