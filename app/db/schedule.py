import sqlite3

SELECT_ALL, SELECT_ONE, DELETE, INSERT = map(chr, range(4))

def runSql(query, type, args=None):
    conn = sqlite3.connect('republicabeerbot.db')
    cursor = conn.cursor()

    if type == INSERT or type == DELETE:
        result = cursor.execute(query, args)
    else:
        result = cursor.execute(query)

        if type == SELECT_ALL:
            result = cursor.fetchall()
        elif type == SELECT_ONE:
            result = cursor.fetchone()

    conn.commit()
    conn.close()
    return result

class Schedule:
    @classmethod
    def pushUpdate(cls):
        cls.queue.put("updated")

    def find_all():
        return runSql("SELECT id, time, duration FROM schedules", type=SELECT_ALL)

    def create(schedule):
        args = (schedule["time"], schedule["duration"])
        result = runSql("INSERT INTO schedules (time, duration) VALUES (?, ?)", args=args, type=INSERT)
        Schedule.pushUpdate()
        return result

    def delete_one(id):
        args = ( id, )
        result = runSql("DELETE FROM schedules WHERE id = ? ", args=args, type=DELETE)
        Schedule.pushUpdate()

        return result
