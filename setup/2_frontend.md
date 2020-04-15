## Lambdas

### Development

*   Create a Python virtual environment and install lambda dependencies:
    ```bash
    $ cd lambdas
    $ virtualenv --python python3 venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ npm install
    ```

*   Set lambda environment variables by creating the file `.env.development` with the following variables:
    ```bash
    DEBUG=True
    PRODUCTION=False

    PHOTO_BUCKET_NAME=S3_BUCKET_NAME
    PHOTO_KEY_PREFIX=healthcam/

    DB_HOST=YOUR_DATABASE_HOST
    DB_PORT=YOUR_DATABASE_PORT
    DB_NAME=YOUR_DATABASE_NAME
    DB_USER=YOUR_DATABASE_USER
    DB_PASSWORD=YOUR_DATABASE_PASSWORD
    SAGEMAKER_ENDPOINT=
    ```

*   Start lambdas in development mode:
    ```bash
    $ npm run dev
    ```

### Deployment

To deploy the lambdas, follow the steps above and then run:

*   Start lambdas in development mode:
    ```bash
    $ npm run deploy
    ```


## Website

### Development

In order to start development on this project, follow the steps below:

*   Ensure that the AWS Lambda-based back-end service is running locally on port 8888.

*   Install app dependencies:
    ```bash
    $ cd app
    $ npm install
    ```

*   Start app in development mode:
    ```bash
    $ npm run dev
    ```

    At this point, the app should have been bundled and a development server should have been started on port 8080.


### Deployment

This project is powered by [AWS Amplify](https://aws-amplify.github.io/) and requires you to sign up for an AWS account if you choose to deploy using that service.

*   Ensure that the AWS Lambda-based back-end has been deployed.

*   Create the file `.env.development.local` in the `./app/` folder and set the endpoint URL to the base URL to which the Lambda service has been deployed:

    ```
    VUE_APP_API_URL=https://your-lambda-url.execute-api.us-east-1.amazonaws.com/dev
    ```

*   Configure your AWS Amplify project:
    ```bash
    $ cd app
    $ npm install -g @aws-amplify/cli
    $ amplify configure
    ```

*   Publish the HealthCam app on AWS Amplify:
    ```bash
    $ amplify publish
    ```

If the deployment has been successful, a publicly accessible URL will be displayed and HealthCam is now up and running. :-)

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