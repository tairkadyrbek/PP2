import psycopg2
from psycopg2 import sql
from datetime import datetime

# Database connection parameters
DB_CONFIG = {
    'dbname': 'snake_game',
    'user': 'postgres',
    'password': 'fsqkwisi2207',
    'host': 'localhost',
}


def get_connection():
    # Create and return a database connection
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None


def init_database():
    # Initialize database tables if they don't exist
    conn = get_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Create players table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            )
        """)
        
        # Create game_sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        conn.commit()
        cursor.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        conn.close()


def get_or_create_player(username):
    # Get player ID or create new player if doesn't exist
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        # Try to get existing player
        cursor.execute("SELECT id FROM players WHERE username = %s", (username,))
        result = cursor.fetchone()
        
        if result:
            player_id = result[0]
        else:
            # Create new player
            cursor.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
            player_id = cursor.fetchone()[0]
            conn.commit()
        
        cursor.close()
        return player_id
    except Exception as e:
        print(f"Error getting/creating player: {e}")
        return None
    finally:
        conn.close()


def save_game_result(username, score, level_reached):
    # Save game result to database
    conn = get_connection()
    if not conn:
        return False
    
    try:
        player_id = get_or_create_player(username)
        if not player_id:
            return False
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO game_sessions (player_id, score, level_reached)
            VALUES (%s, %s, %s)
        """, (player_id, score, level_reached))
        
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Error saving game result: {e}")
        return False
    finally:
        conn.close()


def get_leaderboard(limit=10):
    # Get top scores from database
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.username, gs.score, gs.level_reached, gs.played_at
            FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            ORDER BY gs.score DESC
            LIMIT %s
        """, (limit,))
        
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        return []
    finally:
        conn.close()


def get_personal_best(username):
    # Get player's best score
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT MAX(gs.score)
            FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            WHERE p.username = %s
        """, (username,))
        
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result and result[0] else 0
    except Exception as e:
        print(f"Error fetching personal best: {e}")
        return 0
    finally:
        conn.close()