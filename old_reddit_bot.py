import praw
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from termcolor import colored as c
from get_user_info import get_reddit_credentials
from dotenv import load_dotenv

load_dotenv()

(
  client_id, 
  client_secret, 
  user_agent, 
  refresh_token
) = get_reddit_credentials()

# Your Reddit credentials
CLIENT_ID = client_id
CLIENT_SECRET = client_secret
REFRESH_TOKEN = refresh_token
USER_AGENT = user_agent

# Your Email Credentials
sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')
email_recipient = os.getenv('EMAIL_RECIPIENT')

# Name of Subreddit you're working with. No "r/" in name. AskReddit is good for testing
subreddit_name = 'AskReddit'

reddit = praw.Reddit(
	client_id=CLIENT_ID,
	client_secret=CLIENT_SECRET,
	refresh_token=REFRESH_TOKEN,
	user_agent=USER_AGENT
)


subreddit = reddit.subreddit(subreddit_name)

def send_email(title):

	subject = f"Someone posted in r/{subreddit_name}!"

	body = (
		f'The title of the post is "{title}".\n\n\n' + 
		"This was sent from you're deployed reddit bot."
	)

	message = MIMEMultipart()
	message["From"] = sender_email
	message["To"] = email_recipient
	message["Subject"] = subject

	message.attach(MIMEText(body, "plain"))

	try:
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.starttls()
		server.login(sender_email, sender_password)
		text = message.as_string()
		server.sendmail(sender_email, email_recipient, text)
		server.quit()
		print("Email sent successfully!")
	except Exception as e:
		print(f"Failed to send email. Error: {e}")

def main():
	print(f"Monitoring new posts in r/{subreddit_name}...")

	for submission in subreddit.stream.submissions(skip_existing=True):
		print(f"\nSomeone made a post titled: {c(submission.title, 'blue')}")
		send_email(submission.title)


if __name__ == "__main__":

	# Do NOT change this line
	if subreddit_name == 'NAME_OF_SUBREDDIT':
		print(c(f"Change the value of the \"subreddit_name\" variable", 'blue'))
		exit(0)

	main()
