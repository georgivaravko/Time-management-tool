import db

def add_plans(plan, hours_per_week, info, user_id):
    sql = "INSERT INTO plans (plan, hours_per_week, info, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [plan, hours_per_week, info, user_id])

def get_plans():
    sql = """SELECT id, plan FROM plans ORDER BY hours_per_week DESC"""

    return db.query(sql)

def get_plan(plan_id):
    sql = """SELECT users.username,
    plans.plan,
    plans.hours_per_week,
    plans.info
    FROM users, plans
    WHERE plans.user_id = users.id
    AND plans.id = ?"""
    return db.query(sql, [plan_id])[0]