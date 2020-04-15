
![HealthCam](healthcam.png)

![HealthCam](https://img.shields.io/badge/app-healthcam-8e24aa.svg?style=for-the-badge) &nbsp;
![HealthCam Version](https://img.shields.io/badge/version-1.0-05A5CC.svg?style=for-the-badge) &nbsp;
![HealthCam Status](https://img.shields.io/badge/status-live-00B20E.svg?style=for-the-badge)


# HealthCam App

This part of the repository is representing the front-end of the HealthCam app and is based on Vue and Vuetify.


## Development

In order to start development on this project, follow the steps below:

*   Ensure that the AWS Lambda-based back-end service is running locally on port 8888. You can find instructions in the `./lambdas` folder in this repository.

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


## Deployment

This project is powered by [AWS Amplify](https://aws-amplify.github.io/) and requires you to sign up for an AWS account if you choose to deploy using that service.

*   Ensure that the AWS Lambda-based back-end has been deployed. You can find instructions in the `./lambdas` folder in this repository.

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
