# Direct-Poll Database Setup


1. Log in to your MySQL server as root:

```
mysql -u root -p
```

2. Create the ``dpuser`` user for the Direct-Poll application:

```
mysql> create user 'dpuser'@'%' identified by 'dpuser-password';
```
**Important Notes:** 
* ``dpuser-password`` is a terrible password so make yours stronger.
* The ‘%’ means that ``dpuser`` can connect from any machine on the network. It is more secure to use the IP address of the machine that will host the Direct-Poll application so, for example, if you install the application on the machine with IP address 10.10.10.2, you could use the following command:

   ```
   mysql> create user 'dpuser'@'10.10.10.2' identified by 'dpuser-password'; 
   ```

3. Create the Direct-Poll database:

```
mysql> create database directpoll;
```

4. Grant access to the ``dbuser``:

```
mysql> grant all privileges on directpoll.* to 'dpuser'@'%';
```

5. Swith to the ``directpoll`` database:

```
use directpoll;
```

6. Create the ``poll`` table by cutting and pasting the following SQL into the MySQL commandline:

```
CREATE TABLE poll (
	poll_id INT NOT NULL AUTO_INCREMENT, 
	created TIMESTAMP,
	team_id VARCHAR(26),
	channel_id VARCHAR(26),
	token VARCHAR(50),
	user_id VARCHAR(26),
	user_name VARCHAR(26),
	question VARCHAR(1000),
	answers VARCHAR(200),
	channel_to_poll_id VARCHAR(26),
	published BOOLEAN not null default 0, 
	closed BOOLEAN not null default 0,
	PRIMARY KEY (poll_id)
);
```

When the create statement is executed MySQL should return (note that the execution time will vary):

```
Query OK, 0 rows affected (0.14 sec)
```

7. Create the ``poll_result`` table by cutting and pasting the following SQL into the MySQL commandline:

```
CREATE TABLE poll_result (
	poll_result_id INT NOT NULL AUTO_INCREMENT,
	poll_id INT NOT NULL,
	created TIMESTAMP,
	updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	answer VARCHAR(100),
	votes INT NOT NULL DEFAULT 0,
	PRIMARY KEY (poll_result_id)
);
```

When the create statement is executed MySQL should return (note that the execution time will vary):

```
Query OK, 0 rows affected (0.14 sec)
```

8. Create the ``poll_answer`` table by cutting and pasting the following SQL into the MySQL commandline:

```
CREATE TABLE poll_answer (
	poll_answer_id INT NOT NULL AUTO_INCREMENT,
	poll_id INT NOT NULL, 
	created TIMESTAMP,
	updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	user_id VARCHAR(26),
	answer VARCHAR(100),
	PRIMARY KEY (poll_answer_id)
);
```

When the create statement is executed MySQL should return (note that the execution time will vary):

```
Query OK, 0 rows affected (0.14 sec)
```









