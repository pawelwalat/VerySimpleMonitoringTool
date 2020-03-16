import sqlite3
import json
import prettytable

MIGRATION_FILE = 'vsmt//dbmigrations.json'

sqls = {'check_migrations_exists': "SELECT count(*) FROM sqlite_master WHERE type ='table' AND upper(name) = 'MIGRATION'",
        'find_last_migration': "SELECT coalesce(max(migration_id),0) FROM migration",
        'add_migration_entry': "INSERT INTO migration VALUES (?,?,?,current_timestamp)",
        'add_sensor': "INSERT INTO sensor (sensor_name, sensor_type, hostname, status, parameters, date_created) values (?,?,?,'ENABLED',?, current_timestamp)",
        'remove_sensor': "DELETE FROM sensor WHERE sensor_name=?",
        'list_sensors': "select * from sensor order by sensor_id"}

def conn(db_filename):
    global sqls
    try:
        conn = sqlite3.connect(db_filename) 
    except sqlite3.Error as e:
        print(e)
        raise
    apply_migrations(conn)
    return conn


def apply_migrations(conn):
    global MIGRATION_FILE
    #check if there is migrations table
    cur = conn.cursor()    
    cur.execute(sqls['check_migrations_exists'])
    last_migration = cur.fetchone()[0]
    #find last applied migration script
    if last_migration > 0:
        cur.execute(sqls['find_last_migration'])
        last_migration = cur.fetchone()[0]
    with open(MIGRATION_FILE) as json_file:
        data = json.load(json_file)
    #apply migrations
    for m in data['migrations']:
        if int(m['id']) > last_migration:        
            conn.execute(m['sql'])
            conn.execute(sqls['add_migration_entry'], (m['id'],m['version'],m['sql'],))
            conn.commit()   
         
def add_sensor(db_filename, sensor_name, sensor_type, sensor_hostname, sensor_paramneters):   
    c = conn(db_filename)
    try:
        c.execute(sqls['add_sensor'],(sensor_name,sensor_type,sensor_hostname,sensor_paramneters,))
        c.commit()
        print('Sensor %s added successfully.' % sensor_name)
    except sqlite3.Error as e:
        if str(e) == 'UNIQUE constraint failed: sensor.sensor_name':
            print('Error adding sensor: Sensor with name %s already exists' % (sensor_name))
        else:
            print('Error adding sensor: '+str(e))
    finally:        
        c.close()

def remove_sensor(db_filename, sensor_name):   
    c = conn(db_filename)
    try:
        rc = c.execute(sqls['remove_sensor'],(sensor_name,)).rowcount
        c.commit()
        if rc > 0:
            print('Sensor %s removed successfully.' % sensor_name)
        else:
            print('Error removing sensor: Sensor with name %s does not exist' %sensor_name)
    except sqlite3.Error as e:
        print('Error removing sensor: '+str(e))
    finally:        
        c.close()

def list_sensors(db_filename):        
    c = conn(db_filename)
    c.row_factory = sqlite3.Row
    cur = c.cursor()    
    cur.execute(sqls['list_sensors'])
    t = prettytable.PrettyTable()
    t.field_names = ["Id", "Sensor Name", "Sensory Type", "Hostname", "Status", "Parameters","Creation date"]
    for row in cur.fetchall():
        t.add_row([row['sensor_id'],row['sensor_name'],row['sensor_type'],row['hostname'],row['status'],row['parameters'], row['date_created']])
    print('List of sensors:')
    print(t)
    c.close()


def get_sensors(c):        
    cur = c.cursor()    
    cur.execute(sqls['list_sensors'])
    row = cur.fetchall()
    return row

def log_sensor(c, sensor_id, status, attributes):
    c.execute("INSERT INTO sensor_log (sensor_id, log_date, status, attributes) values (?,current_timestamp,?,?)",(sensor_id,status,attributes))
    c.commit()
