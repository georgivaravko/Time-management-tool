import db

def add_plans(plan, hours_per_week, info, user_id):
    sql = "INSERT INTO plans (plan, hours_per_week, info, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [plan, hours_per_week, info, user_id])

def get_plans():
    sql = """SELECT id, plan FROM plans ORDER BY hours_per_week DESC"""

    return db.query(sql)

def get_plan(plan_id):
    sql = """SELECT users.username,
        users.id AS user_id,
        plans.id AS plan_id,
        plans.plan,
        plans.hours_per_week,
        plans.info
        FROM users, plans
        WHERE plans.user_id = users.id
        AND plans.id = ?"""
    result = db.query(sql, [plan_id])
    return result[0] if result else None

def update_plan(plan_id, plan, hours_per_week, info):
    sql ="""UPDATE plans SET plan = ?,
        hours_per_week = ?,
        info = ?
        WHERE id = ?"""
    db.execute(sql, [plan, hours_per_week, info, plan_id])

def delete_plan(plan_id):
    sql ="DELETE FROM plans WHERE id = ?"
    db.execute(sql, [plan_id])

def search(query):
    sql = """SELECT id, plan
        FROM plans
        WHERE plan LIKE ? OR info LIKE ?
        ORDER BY hours_per_week DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])