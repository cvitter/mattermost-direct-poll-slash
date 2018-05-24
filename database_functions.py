import MySQLdb

def connect( url, user, password, database ):
    """
    Connects to the database and returns the database object
    """
    db = MySQLdb.connect( host = url, user = user, passwd = password, db=database)
    return db


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


poll_id = createPollRecord( "52.173.76.156", "dpuser", "dp_!4312+", "directpoll", 
                            "team-id", "channel-id", "token", "user-id", "user-name", "Question?", "Answer, Answer, Answer", "" )

print "Poll ID: " + str( poll_id )

poll_result_id = createPollResultRecord( "52.173.76.156", "dpuser", "dp_!4312+", "directpoll", poll_id, "Answer!")

print "Poll Result ID: " + str( poll_result_id )
