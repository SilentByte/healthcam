# Doesn't actually belong here. We'll shuffle repo stuff around later.

# Create RDS DB
```
aws rds create-db-instance 
--engine postgres \
--db-instance-identifier PUT_A_NAME_IN_HERE \
--allocated-storage 20 \
--db-instance-class db.t2.micro \
--publicly-accessible 
--master-username PUT_USERNAME_HERE \
--master-user-password PUT_PASSWORD_HERE \
--backup-retention-period 3

```
Check your database with  ```aws rds describe-db-instances --region us-east-1| grep 'DBInstanceIdentifier":' -A 7``` and wait until the field ```DBInstanceStatus``` becomes "available".

After this you should be able to connect to this publicly accessible data, I suggest [dbeaver](https://dbeaver.io/download/) if you don't already have a favourite SQL tool.

Make sure to record your Endpoint and username/password for later steps

# Create S3 Bucket





# Serverless deploy

# References 
[Launch RDS with AWS CLI](https://www.mydatahack.com/how-to-launch-postgres-rds-with-aws-command-line-interface-cli/)