# Troubleshooting
When you face any issue, first look up that in [Troubleshooting](https://github.com/project-travel-mate/server/blob/master/TROUBLESHOOTING.md), then search for the error online and **only then open up a [new issue](https://github.com/project-travel-mate/server/issues/new)**. 

*If you manage to debug the error and feel that is pretty common error for anyone to face, please add the issue and it's potentional fix to [Troubleshooting](https://github.com/project-travel-mate/server/blob/master/TROUBLESHOOTING.md).*

**Jump Quickly to-**
+ [Database connection failing](#database-connection-failing)

## Database connection failing
```
Exception in thread django-main-thread:
Traceback (most recent call last):
    ...
    conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
psycopg2.OperationalError: could not connect to server: Connection refused
	Is the server running on host "localhost" (127.0.0.1) and accepting
	TCP/IP connections on port 5432?
```
If you're getting the above error, the previous connection to Postgres is probably not closed properly and you need to restart postgres:
+ On Linux 
```
sudo service postgresql stop
sudo service postgresql start
```
+ On MacOS
```
pg_ctl -D /usr/local/var/postgres stop
pg_ctl -D /usr/local/var/postgres start
```
+ On Windows
```
pg_ctl -D "C:\Program Files\PostgreSQL\9.6\data" restart
```