# AutoResponder
Python App to auto respond to email when you are on Vacation.

Visit https://console.developers.google.com, create a new project, enable the Gmail API, and download the credentials.json file for the project.

Install the required Python libraries by running the following command in your terminal:

```pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client```

Update the `SENDER_EMAIL` constant with your email address.

This app uses the Gmail API to retrieve unread emails and extract the sender's email address from the headers. It then sends an auto-response email using the Gmail API. The **'token.json'** file is used to store the user's credentials, and the **'credentials.json'** file contains the application's credentials.
