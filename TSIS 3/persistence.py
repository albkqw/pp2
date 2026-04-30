import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "red",
    "difficulty": "medium"
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)

    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        save_leaderboard([])

    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)


def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_score(username, score, distance):
    leaderboard = load_leaderboard()

    existing_player = None

    # ищем игрока
    for player in leaderboard:
        if player["username"] == username:
            existing_player = player
            break

    if existing_player:
        if score > existing_player["score"]:
            existing_player["score"] = score
            existing_player["distance"] = distance
    else:
        leaderboard.append({
            "username": username,
            "score": score,
            "distance": distance
        })

    # Сортируем по очкам от большего к меньшему
    leaderboard = sorted(
        leaderboard,
        key=lambda x: x["score"],
        reverse=True
    )[:10]

    save_leaderboard(leaderboard)