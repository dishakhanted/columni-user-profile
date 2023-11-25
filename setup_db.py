import psycopg2
import os

create_school_table = """
CREATE TABLE IF NOT EXISTS schools(
    schoolID SERIAL PRIMARY KEY,
    schoolName TEXT UNIQUE NOT NULL 
);
"""

create_user_table = """
CREATE TABLE IF NOT EXISTS users(
    userid SERIAL PRIMARY KEY,
    schoolid INT REFERENCES schools(schoolID),
    firstName TEXT,
    lastName TEXT, 
    columbiaemail TEXT UNIQUE,
    password TEXT,
    profilepicture TEXT,
    major TEXT,
    jobtitle TEXT, 
    company TEXT, 
    graduationdate INTEGER,
    userdescription TEXT,
    creationdate TIMESTAMPTZ
);
"""

insert_school = """
INSERT INTO schools (schoolName) VALUES (%s)
"""

schools_data = [
    ("Columbia College",),
    ("SEAS",),
    ("Columbia Business School",),
    ("Graduate School of Arts and Sciences",),
    ("School of General Studies",),
    ("Columbia Law School",),
    ("Mailman School of Public Health",),
    ("Columbia University College of Physicians and Surgeons",),
    ("SIPA",),
    ("Graduate School of Journalism",),
    ("School of the Arts",),
    ("GSAPP",)
]

conn = psycopg2.connect(database = os.environ["PSQL_DATABASE"], #"columni_userdb", 
                        user = os.environ["PSQL_USER"], #"postgres", 
                        host= os.environ["PSQL_HOST"], # 'columni-user-db.cnuwaz8dqxjy.us-east-1.rds.amazonaws.com',
                        password = os.environ["PSQL_PASSWORD"], # "Disha101",
                        port = int(os.environ["PSQL_PORT"]))# 5432)

cur = conn.cursor()
cur.execute(create_school_table)
cur.execute(create_user_table)
conn.commit()
cur.executemany(insert_school, schools_data)
conn.commit()
cur.close()
conn.close()
