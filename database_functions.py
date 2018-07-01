import MySQLdb


def connect(url, user, password, database):
    """
    Connects to the database and returns the database object
    """
    db = MySQLdb.connect(host=url, user=user, passwd=password, db=database)
    return db


def get_all_polls():

    sql_result = "SELECT poll_id, created, team_id, user_name, " + \
                "question, answers, channel_to_poll_id, published, " + \
                "closed FROM poll ORDER BY poll_id DESC;"

    db = connect(db_url, db_user, db_password, db_name)
    cursor = db.cursor()

    cursor.execute(sql_result)
    for (poll_id, created, team_id, user_name, question, answers,
         channel_to_poll_id, published, closed) in cursor:
        str = ""
    return 0


def cancel_poll_record(db_url, db_user, db_password, db_name, poll_id):
    """
    Deletes the poll record if it has not been published,
    published records cannot be deleted
    """
    db = connect(db_url, db_user, db_password, db_name)
    cursor = db.cursor()

    sql_delete_poll = "DELETE FROM poll WHERE poll_id = " + \
        str(poll_id) + " AND published = 0"
    sql_delete_poll_result = "DELETE FROM poll_result WHERE poll_id = " + \
        str(poll_id)

    rows_affected = 0
    try:
        cursor.execute(sql_delete_poll)
        db.commit()
        rows_affected = cursor.rowcount

        if rows_affected > 0:
            cursor.execute(sql_delete_poll_result)
            db.commit()
            rows_affected = rows_affected + cursor.rowcount
    except:
        rows_affected = 0

    db.close()
    return rows_affected


def create_poll_record(db_url, db_user, db_password, db_name,
                       team_id, channel_id, token, user_id, user_name,
                       question, answers, channel_to_poll_id):
    """
    Inserts new poll record and if successful returns the poll_id
    value of the new record
    """
    db = connect(db_url, db_user, db_password, db_name)
    cursor = db.cursor()

    sql_insert = "INSERT INTO poll (team_id, channel_id, token, " + \
                 "user_id, user_name, question, answers, channel_to_poll_id) " + \
                 "VALUES ('" + team_id + "', '" + channel_id + "', '" + \
                 token + "', '" + user_id + "', '" + user_name + "', '" + \
                 question + "', '" + answers + "', '" + channel_to_poll_id + "')"

    sql_fetch = 'SELECT MAX(poll_id) FROM poll WHERE user_id = "' + user_id + '"'

    out = 0
    try:
        cursor.execute(sql_insert)
        db.commit()
        cursor.execute(sql_fetch)
        out = cursor.fetchone()[0]
    except:
        out = 0

    db.close()
    return out


def create_poll_result_record(db_url, db_user, db_password, db_name, poll_id, answer):
    """
    Inserts new poll_result record and if successful returns the
    poll_result_id value of the new record
    """
    db = connect(db_url, db_user, db_password, db_name)
    cursor = db.cursor()

    sql_insert = 'INSERT INTO poll_result (poll_id, answer, votes) ' + \
        'VALUES (' + str(poll_id) + ', "' + answer + '", 0)'

    sql_fetch = 'SELECT MAX(poll_result_id) FROM poll_result WHERE poll_id = ' + str(poll_id)

    out = 0
    try:
        cursor.execute(sql_insert)
        db.commit()
        cursor.execute(sql_fetch)
        out = cursor.fetchone()[0]
    except:
        out = 0

    db.close()
    return out
