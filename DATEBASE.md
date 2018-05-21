# Direct-Poll Database Setup


1. Log in to your MySQL server as root:

```
mysql -u root -p
```

2. Create a the ``dpuser`` for the Direct-Poll application:

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






