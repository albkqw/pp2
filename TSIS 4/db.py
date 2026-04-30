import psycopg2


conn = psycopg2.connect(
    host="localhost",
    database="test_db",
    user="postgres",
    password="12345678"
)

cursor = conn.cursor()


def get_or_create_player(username):
    cursor.execute(
        "SELECT id FROM players WHERE username=%s",
        (username,)
    )

    player = cursor.fetchone()

    if player:
        return player[0]

    cursor.execute(
        "INSERT INTO players(username) VALUES(%s) RETURNING id",
        (username,)
    )

    conn.commit()

    return cursor.fetchone()[0]


def save_game(username, score, level):
    player_id = get_or_create_player(username)

    cursor.execute(
        """
        INSERT INTO game_sessions(player_id, score, level_reached)
        VALUES(%s,%s,%s)
        """,
        (player_id, score, level)
    )

    conn.commit()


def get_top_10():
    cursor.execute("""
        SELECT
            p.username,
            MAX(g.score) as best_score,
            MAX(g.level_reached) as best_level,
            MAX(g.played_at) as last_played
        FROM players p
        JOIN game_sessions g
            ON p.id = g.player_id
        GROUP BY p.username
        ORDER BY best_score DESC
        LIMIT 10
    """)

    return cursor.fetchall()


def get_best_score(username):
    cursor.execute("""
        SELECT MAX(g.score)
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        WHERE p.username=%s
    """, (username,))

    result = cursor.fetchone()[0]

    return result if result else 0