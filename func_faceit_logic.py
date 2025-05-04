import requests
import pandas as pd

def extract_player_ids(nicknames, api_key):
    """
    Given a list of nicknames, return a dict {nickname: player_id}
    """
    player_ids = {}
    print("\nFetching player IDs...")
    for nickname in nicknames:
        try:
            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            player_id_url = f"https://open.faceit.com/data/v4/search/players?nickname={nickname}"
            response = requests.get(player_id_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data["items"]:  # Check if player was found
                    player_id = data["items"][0]['player_id']
                    player_ids[nickname] = player_id
                else:
                    player_ids[nickname] = None
            else:
                player_ids[nickname] = None
        except Exception:
            player_ids[nickname] = None
    return player_ids

def get_players_cs2_elo(api_key, player_ids):
    """
    Fetches CS2 Elo for multiple players using their player IDs.
    Continues processing even if some players are not found or have missing data.
    
    :param api_key: FACEIT API key
    :param player_ids: Dictionary of {nickname: player_id}
    :return: Pandas DataFrame with player stats
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }

    results = []
    
    for nickname, player_id in player_ids.items():
        try:
            if not player_id:
                results.append({
                    "nickname": nickname,
                    "elo": None,
                    "error_reason": "Player not found"
                })
                continue

            # Use the player ID to get stats
            player_stats_url = f'https://open.faceit.com/data/v4/players/{player_id}'
            response = requests.get(player_stats_url, headers=headers)

            if response.status_code == 200:
                player_data = response.json()
                games = player_data.get('games', {})
                
                if 'cs2' in games:
                    elo = games['cs2'].get('faceit_elo')
                    results.append({
                        "nickname": nickname,
                        "elo": elo,
                        "error_reason": None
                    })
                else:
                    results.append({
                        "nickname": nickname,
                        "elo": None,
                        "error_reason": "No CS2 stats found"
                    })
            else:
                results.append({
                    "nickname": nickname,
                    "elo": None,
                    "error_reason": f"Failed to get stats (Status: {response.status_code})"
                })
        except Exception:
            results.append({
                "nickname": nickname,
                "elo": None,
                "error_reason": "Unexpected error occurred"
            })

    return pd.DataFrame(results)

def get_player_stats_aggregate(player_ids, api_key):
    # Returns a dict: {nickname: (winrate, kd, adr, hs_percent, games_found)}, games_data
    stats = {}
    games_data = {}
    for nickname, player_id in player_ids.items():
        if not player_id:
            stats[nickname] = ('Not found', 'Not found', 'Not found', 'Not found', 0)
            continue
        try:
            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            stats_url = f"https://open.faceit.com/data/v4/players/{player_id}/games/cs2/stats?limit=100"
            response = requests.get(stats_url, headers=headers)
            if response.status_code == 200:
                stats_data = response.json()
                games_data[nickname] = stats_data
                matches = stats_data.get('items', [])
                games_found = len(matches)
                if games_found == 0:
                    stats[nickname] = ('Not found', 'Not found', 'Not found', 'Not found', 0)
                    continue
                # Aggregate stats
                total_kills = 0
                total_deaths = 0
                win_sum = 0
                total_adr = 0.0
                total_hs_percent = 0.0
                valid_adr_games = 0
                valid_hs_games = 0
                for match in matches:
                    stats_match = match.get('stats', {})
                    total_kills += int(stats_match.get('Kills', 0))
                    total_deaths += int(stats_match.get('Deaths', 0))
                    # Result is stored as 1 (win) or 0 (loss)
                    try:
                        win_sum += int(stats_match.get('Result', 0))
                    except Exception:
                        pass
                    # ADR
                    try:
                        adr = float(stats_match.get('ADR', 0))
                        total_adr += adr
                        valid_adr_games += 1
                    except Exception:
                        pass
                    # HS%
                    try:
                        hs = float(stats_match.get('Headshots %', 0))
                        total_hs_percent += hs
                        valid_hs_games += 1
                    except Exception:
                        pass
                kd = round(total_kills / max(1, total_deaths), 2)
                winrate = f"{round((win_sum / games_found) * 100, 1)}%"
                adr = round(total_adr / max(1, valid_adr_games), 1) if valid_adr_games > 0 else 'Not found'
                hs_percent = f"{round(total_hs_percent / max(1, valid_hs_games), 1)}%" if valid_hs_games > 0 else 'Not found'
                stats[nickname] = (winrate, kd, adr, hs_percent, games_found)
            else:
                stats[nickname] = ('Not found', 'Not found', 'Not found', 'Not found', 0)
        except Exception:
            stats[nickname] = ('Not found', 'Not found', 'Not found', 'Not found', 0)
    return stats, games_data