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
	poll_id int NOT NULL AUTO_INCREMENT, 
	created TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
	team_id VARCHAR(26),
	channel_id VARCHAR(26),
	token VARCHAR(50),
	user_id VARCHAR(26),
	user_name VARCHAR(26),
	question VARCHAR(1000),
	answers VARCHAR(200),
	channel_to_poll_id VARCHAR(26),
	published boolean not null default 0, 
	closed boolean not null default 0,
	PRIMARY KEY (poll_id)
);
```

When the create statement is executed MySQL should return (not that the execution time will vary):

```
Query OK, 0 rows affected (0.14 sec)
```






