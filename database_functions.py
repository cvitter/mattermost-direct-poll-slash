import MySQLdb

def connect( url, user, password, database ):
    """
    Connects to the database and returns the database object
    """
    db = MySQLdb.connect( host = url, user = user, passwd = password, db=database)
    return db


def getAllPolls():
    
    sqlSelect = "SELECT poll_id, created, team_id, user_name, question, answers, " +\
                "channel_to_poll_id, published, closed FROM poll ORDER BY poll_id DESC;"
                
    db = connect(  dbUrl, dbUser, dbPassword, dbName )
    cursor = db.cursor()
    
    cursor.execute( sqlSelect )
    for ( poll_id, created, team_id, user_name, question, answers, channel_to_poll_id, published, closed ) in cursor:
        str = ""
                    
    return 0


def cancelPollRecord( dbUrl, dbUser, dbPassword, dbName, poll_id ):
    """
    Deletes the poll record if it has not been published, published records cannot be deleted
    """
    db = connect(  dbUrl, dbUser, dbPassword, dbName )
    cursor = db.cursor()
    
    sqlDeletePoll = "DELETE FROM poll WHERE poll_id = " + str( poll_id ) + " AND published = 0"
    sqlDeletePollResult = "DELETE FROM poll_result WHERE poll_id = " + str( poll_id ) 
    
    rows_affected = 0
    try:
        cursor.execute( sqlDeletePoll )
        db.commit()
        rows_affected = cursor.rowcount
        
        if rows_affected > 0:
            cursor.execute( sqlDeletePollResult )
            db.commit()
            rows_affected = rows_affected + cursor.rowcount
    except:
        rows_affected = 0
    
    db.close()
    return rows_affected
    

def createPollRecord( dbUrl, dbUser, dbPassword, dbName, 
                      team_id, channel_id, token, user_id, user_name, question, answers, channel_to_poll_id):
    """
    Inserts new poll record and if successful returns the poll_id value of the new record
    """
    db = connect(  dbUrl, dbUser, dbPassword, dbName )
    cursor = db.cursor()
    
    sqlInsert = 'INSERT INTO poll (team_id, channel_id, token, user_id, user_name, ' + \
        'question, answers, channel_to_poll_id) ' + \
        'VALUES ("' + team_id + '", "' + channel_id + '", "' + token + '", "' + user_id + '",' + \
        ' "' + user_name + '", "' + question + '", "' + answers + '", "' + channel_to_poll_id + '")'
        
    sqlFetch = 'SELECT MAX(poll_id) FROM poll WHERE user_id = "' + user_id + '"'

    out = 0
    try:
        cursor.execute( sqlInsert )
        db.commit()
        cursor.execute( sqlFetch )
        out = cursor.fetchone()[0]
    except:
        out = 0
    
    db.close()
    return out


def createPollResultRecord( dbUrl, dbUser, dbPassword, dbName, poll_id, answer ):
    """
    Inserts new poll_result record and if successful returns the 
    poll_result_id value of the new record
    """
    db = connect(  dbUrl, dbUser, dbPassword, dbName )
    cursor = db.cursor()
    
    sqlInsert = 'INSERT INTO poll_result (poll_id, answer, votes) ' + \
        'VALUES (' + str( poll_id ) + ', "' + answer + '", 0)'
        
    sqlFetch = 'SELECT MAX(poll_result_id) FROM poll_result WHERE poll_id = ' + str( poll_id )

    out = 0
    try:
        cursor.execute( sqlInsert )
        db.commit()
        cursor.execute( sqlFetch )
        out = cursor.fetchone()[0]
    except:
        out = 0
    
    db.close()    
    return out

