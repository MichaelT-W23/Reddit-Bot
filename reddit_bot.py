import praw
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from botocore.exceptions import ClientError
from termcolor import colored as c
import boto3 
import json


print(c("YOU PROBABLY MEANT TO RUN 'python3 old_reddit_bot.py'", 'cyan'))


def get_secret(secret_name):
	
	region_name = "us-east-1"
	
	session = boto3.session.Session()
	
	client = session.client(
		service_name='secretsmanager',
		region_name=region_name
	)
	
	try:
		get_secret_value_response = client.get_secret_value(
			SecretId=secret_name
		)
	except ClientError as e:
		raise e
	
	secret = get_secret_value_response['SecretString']
	secret_dict = json.loads(secret)
	
	return secret_dict

try:
    aws_secrets = get_secret("my-aws-keys")
except ClientError:
	print(c("You don't have a an AWS key", 'red'))

aws_access_key_id = aws_secrets['AWS_ACCESS_KEY_ID']
aws_secret_access_key = aws_secrets['AWS_SECRET_ACCESS_KEY']


session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name="us-east-1"
)

# Get application secrets
secrets = get_secret("reddit-bot-keys")

# Your Reddit credentials
CLIENT_ID = secrets['CLIENT_ID']
CLIENT_SECRET = secrets['CLIENT_SECRET']
REFRESH_TOKEN = secrets['REFRESH_TOKEN']
USER_AGENT = secrets['USER_AGENT']

# Your Email Credentials
sender_email = secrets['SENDER_EMAIL']
sender_password = secrets['SENDER_PASSWORD']
email_recipient = secrets['EMAIL_RECIPIENT']

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
