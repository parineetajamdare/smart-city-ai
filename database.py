import sqlite3


def create_connection():
    return sqlite3.connect("smart_city.db")


def create_users_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def register_user(name, email, phone, password):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users(name,email,phone,password)
        VALUES(?,?,?,?)
        """,
        (name, email, phone, password)
    )

    conn.commit()
    conn.close()


def login_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE email = ? AND password = ?
        """,
        (email, password)
    )

    user = cursor.fetchone()

    conn.close()

    return user

def save_issue(
    complaint_id,
    user_id,
    title,
    description,
    city,
    address,
    status,
    created_at,
    ai_response
):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    INSERT INTO issues
    (
        complaint_id,
        user_id,
        title,
        description,
        city,
        address,
        status,
        created_at,
        ai_response
  )
       VALUES(?,?,?,?,?,?,?,?,?)
        """,
      (
        complaint_id,
        user_id,
        title,
        description,
        city,
        address,
        status,
        created_at,
        ai_response
     )

    )

    conn.commit()
    conn.close()

def create_issues_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint_id TEXT,
    user_id INTEGER,
    title TEXT,
    description TEXT,
    city TEXT,
    address TEXT,
    status TEXT,
    created_at TEXT,
    ai_response TEXT
   )
    """)

    conn.commit()
    conn.close()

def get_user_issues(user_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT complaint_id,
        title,
        description,
        city,
        address,
        status,
        created_at,
        ai_response
        FROM issues
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    issues = cursor.fetchall()

    conn.close()

    return issues

def get_dashboard_stats(user_id):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM issues
        WHERE user_id = ?
        """,
        (user_id,)
    )

    total = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM issues
        WHERE user_id = ?
        AND status = 'Pending'
        """,
        (user_id,)
    )

    pending = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM issues
        WHERE user_id = ?
        AND status = 'Resolved'
        """,
        (user_id,)
    )

    resolved = cursor.fetchone()[0]

    conn.close()

    return total, pending, resolved

create_users_table()
create_issues_table()