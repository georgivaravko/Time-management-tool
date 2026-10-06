import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def get_classes(plan_id):
    sql = "SELECT title, value FROM plan_classes WHERE plan_id = ?"
    return db.query(sql, [plan_id])

def add_plans(plan, hours_per_week, info, user_id, classes):
    sql = "INSERT INTO plans (plan, hours_per_week, info, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [plan, hours_per_week, info, user_id])

    plan_id = db.last_insert_id()

    sql = "INSERT INTO plan_classes (plan_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [plan_id, title, value])


def get_plans():
    sql = """SELECT id, plan FROM plans ORDER BY hours_per_week DESC"""

    return db.query(sql)

def get_users_plans(user_id):
    sql = """SELECT id, plan FROM plans WHERE plans.user_id = ? ORDER BY hours_per_week DESC"""

    return db.query(sql, [user_id])

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

def update_plan(plan_id, plan, hours_per_week, info, classes):
    sql ="""UPDATE plans SET plan = ?,
        hours_per_week = ?,
        info = ?
        WHERE id = ?"""
    db.execute(sql, [plan, hours_per_week, info, plan_id])

    sql = "DELETE FROM plan_classes WHERE plan_id = ?"
    db.execute(sql, [plan_id])

    sql = "DELETE FROM plan_classes WHERE plan_id = ?"
    db.execute(sql, [plan_id])

    sql = "INSERT INTO plan_classes (plan_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [plan_id, title, value])

def delete_plan(plan_id):
    sql = "DELETE FROM plan_classes WHERE plan_id = ?"
    db.execute(sql, [plan_id])
    sql ="DELETE FROM plans WHERE id = ?"
    db.execute(sql, [plan_id])

def search(query):
    sql = """SELECT id, plan
        FROM plans
        WHERE plan LIKE ? OR info LIKE ?
        ORDER BY hours_per_week DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])

def like(plan_id, user_id):
    sql = "SELECT * FROM likes WHERE plan_id = ? and user_id = ?"
    result = db.query(sql, [plan_id, user_id])
    print(result)
    if not result:
        sql = "INSERT INTO likes (plan_id, user_id) VALUES (?, ?)"
        db.execute(sql, [plan_id, user_id])
    else:
        sql = "DELETE FROM likes WHERE user_id = ? AND plan_id = ?"
        db.execute(sql, [user_id, plan_id])

def likes(plan_id):
    sql = "SELECT COUNT(id) AS count FROM likes WHERE plan_id = ?"
    result = db.query(sql, [plan_id])
    if result:
        return result[0]["count"]
    #return 0