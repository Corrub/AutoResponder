# AutoResponder
Python App to auto respond to email when you are on Vacation.

You need `credentials.json` file for the program to run. To get your credentials follow below steps

Visit https://console.developers.google.com > Create a new project > Go to credentials section > Select create credentials > OAuth 2.0 Client IDs > Application Type > Web Application > Give it any name > Add http://localhost:8080 to your redirect uri > Click Create 

Enable the Gmail API, and download the `credentials.json` file and place it in the project root directory.

Install the required Python libraries by running the following command in your terminal:

```pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client```

Update the `SENDER_EMAIL` constant with your email address.

NOTE: You have to create label named **Auto Replied** in your gmail account

This app uses the Gmail API to retrieve unread emails and extract the sender's email address from the headers. It then sends an auto-response email using the Gmail API. The **'token.json'** file is used to store the user's credentials, and the **'credentials.json'** file contains the application's credentials.
