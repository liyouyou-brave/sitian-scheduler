import mysql.connector

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'rainy',
    password = '@Sql2024',
    database = 'sitian_db'
)

cursor = conn.cursor()

# create site_info table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS site (
        site_id BIGINT primary key,
        sitename CHAR(32),
        site_lon DOUBLE,
        site_lat DOUBLE,
        site_alt DOUBLE,
        timestamp DOUBLE
    )
""")

# create telescope_info table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS telescope (
        tel_id BIGINT primary key,
        telescop CHAR(32),
        site_id BIGINT,
        tel_des CHAR(200),
        status INT,
        timestamp DOUBLE,
        foreign key (site_id) references site(site_id)
    )
""")

# create target_info table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS target (
        targ_id BIGINT primary key,
        targname CHAR(32),
        ra_targ DOUBLE,
        dec_targ DOUBLE,
        status INT,
        timestamp DOUBLE
    )
""")

# create task_info table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS task (
        task_id BIGINT primary key,
        targ_id BIGINT,
        tel_id BIGINT,
        site_id BIGINT,
        status INT,
        task_des CHAR(200),
        obstime DOUBLE,
        timestamp DOUBLE,
        foreign key (targ_id) references target(targ_id),
        foreign key (tel_id) references telescope(tel_id)
    )
""")

conn.commit()
cursor.close()
conn.close()
print("Create tables successfully!")