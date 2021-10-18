# Human-in-the-loop consensus

## About
The software contained in this repository provides a proof-of-concept application to enable blockchain consensus via email messaging. It represents a student project undertaken by Zachary K. Stewart at QUT in Semester 2 of 2021.

## Software Prerequisites
The software was tested and developed using Python 3.7.4, but is likely to work with any Python 3.X version. It relies upon several Python packages, including:

* tkinter (including ttk 8.6)
* bs4 (BeautifulSoup4)
* pyperclip
* google-api-python-client

## API Prerequisites
The software makes use of the Gmail API to read email messages from your account. To set this up locally, you will need a Google account and a Gmail address. Next, access the Google Cloud Platform console and start a new project. Access the APIs and Services options for your new project and click the "OAuth consent screen" option. Do the following:

1. Set user type to "External" > Click "Create".
2. Set the app name, support email, and developer contact email > Click "Save and Continue".
3. Click "Add or Remove Scopes" > Scroll down to "Manually add scopes" > Enter `https://www.googleapis.com/auth/gmail.readonly` > Click "Add to Table" > Click "Update".
4. You should now have a Gmail scope added which gives permission to "View your email messages and settings" within your "Restricted Scopes" > Click "Save and Continue".
5. Click "Save and Continue" without doing anything to "Test Users".
6. You should now see a summary page which you don't need to touch.
7. Click "Credentials" in the sidebar of the Google Cloud Platform console screen.
8. Click "Create Credentials" at the top of the screen > In the dropdown menu, select "OAuth Client ID".
9. In "Application type", select "Desktop App" > Specify a name to describe this project > Click "Create".
10. You should see a pop up display with "Download JSON" available. Click this, and save the file as "credentials.json" to the same location as the `app.py` file of this repository.
11. Alternatively, if you closed out of the pop up and you're still in the "Credentials" part of the console, then under the "OAuth 2.0 Client IDs" section you should locate your Desktop application and under its "Actions" column click the download button which will launch the pop up again.

Note that, at some point during the program's operations when you first call the Gmail API, you'll have a browser window open automatically requesting confirmation that you want to give the program access to your Gmail email messages. Just "Continue" all of this - you're only giving yourself permission to read your own messages which is fine.

## Running program
After installing the Python prerequisites and setting up the "credentials.json" file, you should just need to bring up a command prompt (or "terminal") and navigate to the directory where `app.py` is. Calling `python app.py` will launch a graphical interface of the software application.

## How to use
As illustration, we'll go through a typical use case of the program where you are the Leader i.e., you want to make a Request for others to respond to which will then be stored within the blockchain. To begin:

1. Launch the program via `python app.py`.
2. Click the "Make a Request" tab at the top left of the screen.
3. Write the Request you wish to make of your business stakeholders ("Recipients"). Click the "Copy Request" button when you're done, and you'll have a formatted Request message to paste (Ctrl + V, or right click > "Paste")
4. Open up your Gmail email client and format an email you wish to send to your recipients. Set your recipients, CCers, and subject to whatever you wish.
5. Write anything you want in your email - then, at some place in your email message and on a new line, paste the formatted Request message. Send the email.
6. Once you have all your replies received, click the "Check Responses" tab at the top center of the screen.
7. Type in a text query (>= 5 characters) to search for the email you originally sent to the recipients which included the formatted Request message. Click "Search".
8. After a brief wait, any results will be displayed in a table with the subject, sender address, and date of email. Click the email you sent with the formatted Request message, or click "Go Back" if you need to specify a different query text.
9. If you clicked the wrong email, you'll see a message suggesting this and you'll need to click the "Go Back" button. If you clicked the right email, you'll see the details of the email as well as the details of the Request you made. For each Recipient tabulated, you'll need to do the following:
9.1. Click a Recipient which has "No" listed for whether it has been processed or not.
9.2. Type in text query (>= 5 characters) that will enable you to find the email you received from that Recipient which contains their Response. Click "Search".
9.3. Click the result in the table which corresponds to their email containing the relevant Response (note that only results from the recipient will be shown here).
9.4. If you clicked the wrong email, you'll see a message at the bottom of the screen suggesting this. If you clicked the right email, it will direct you back to the screen where your Recipients are tabulated, and they will be noted as "Yes" in the Processed column.
10. Once you've found the Response email for all your recipients, the program will show you a screen with the formatted Bundle message for you to send to all your recipients one last time. Click the "Copy Bundle" button at the bottom of the screen.
11. Like before when sending the Request, open your Gmail client again and send an email which contains the formatted Bundle message somewhere within the message.

After all this, you'll have officially made a Request, performed consensus with the Recipient Responses, and formed a Bundle.

The last step is to commit this Bundle to your blockchain. This is facilicated with a rudimentary blockchain that you can access by clicking the "Commit Bundle" tab at the top right of the screen. Here, simply paste the Bundle message and then click "Commit Bundle". If the Bundle is valid, you'll receive a message to say that it has been committed; otherwise, you'll receive an error message at the bottom of the screen indicating what has likely gone wrong.

Note that the above description for committing a Bundle applies as much to the Leader as it does to the Recipients who receive the Bundle message from the Leader.

## Known bugs
Once you've gone through the whole program flow of performing consensus and making a Bundle, the "Check Responses" tab will be empty. To fix this, you will need to launch the program again. Sorry - I'm not versed enough in tkinter to identify the problem.

## Other details
The local blockchain is, as mentioned, very rudimentary. It exists as a pickled file called `local_chain.pkl` within the file directory where `app.py` resides. Little attention is paid to the implementation of this beyond minor cryptography to ensure that the Request message contents and date match the Request ID in the formatted Request message. The purpose of the application here is to demonstrate how consensus can be performed by a human with a simple helper program. The details of a "real" blockchain implementation can be found in other project.

I'd also like to credit rdbende of https://github.com/rdbende/Azure-ttk-theme for creating the ttk theme which I used to make the program look a lot less drab.

## Contact
The original author of this program can be contacted at zkstewart1@gmail.com. Thanks for looking at this repository!