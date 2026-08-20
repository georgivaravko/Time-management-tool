import db

def get_user(user_id):
    sql = """SELECT id, username
        FROM users
        WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_users_plans(user_id):
    sql = """SELECT id, plan
        FROM plans
        WHERE user_id = ? ORDER BY hours_per_week DESC"""
    return db.query(sql, [user_id])