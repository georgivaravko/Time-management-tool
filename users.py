import db
from werkzeug.security import generate_password_hash, check_password_hash

def get_profile_picture(user_id):
    sql = "SELECT profile_picture FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    if result and result[0]["profile_picture"]:
        return result[0]["profile_picture"]
    return None

def update_profile_picture(user_id, profile_picture):
    sql = "UPDATE users SET profile_picture = ? WHERE id = ?"
    db.execute(sql, [profile_picture, user_id])

def get_user(user_id):
    sql = """SELECT id, username, profile_picture IS NOT NULL has_image
             FROM users
             WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None


def get_users_plans(user_id):
    sql = """SELECT id, plan
        FROM plans
        WHERE user_id = ? ORDER BY hours_per_week DESC"""
    return db.query(sql, [user_id])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None