from azure.identity import DeviceCodeCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.item.messages.messages_request_builder import MessagesRequestBuilder
import os
import base64
import asyncio
import re
from datetime import date, datetime
from azure.core.credentials import AccessToken

token_save_path = "token_info.txt"

save_dir = f'C:\\Users\\rum\\OneDrive - RAR Açucar, S.A\\Documents\\1_Projetos\\4_Indicadores\\Pedidos\\Job Z_LISTAGEM_ORDENS, Step 1\\buffer'
if not os.path.exists(save_dir):
	os.makedirs(save_dir)

client_id = "########"
tenant_id = "########"
scopes = ["User.Read", "Mail.Read", "Mail.ReadWrite"]

class RawAccessTokenProvider:
	"""
	A simple credential provider that returns a raw access token for use with Azure SDK clients.
	"""

	def __init__(self, access_token: str, expires_on: int) -> None:
		self._access_token = access_token
		self._expires_on = expires_on

	def get_token(self, *scopes, **kwargs) -> AccessToken:
		return AccessToken(self._access_token, self._expires_on)

def get_access_token():
	if os.path.exists(token_save_path):
		with open(token_save_path, "r") as token_file:
			lines = token_file.readlines()
			access_token = lines[0].strip().split(": ")[1]
			expiration_date = lines[1].strip().split(": ")[1]

		expiration_date_cleaned = expiration_date.replace(" UTC", "")
		expiration_date_timestamp = int(datetime.strptime(expiration_date_cleaned, '%Y-%m-%d %H:%M:%S').timestamp())

		if expiration_date_timestamp > datetime.utcnow().timestamp() + 300:
			return access_token, expiration_date_timestamp

	return None, None

async def get_mail():
	try:
		mail = await asyncio.wait_for(
			client.me.messages.get(request_configuration=request_configuration),
			timeout=60
		)
		for email in mail.value:
			if (re.search(r'.*########', email.subject) and email.sender.email_address.address == "###@#####.###"):
				print(email.subject)
				print(email.created_date_time)
				email_id = email.id
				attachments_result = await asyncio.wait_for(
					client.me.messages.by_message_id(email_id).attachments.get(),
					timeout=60
				)
				attachment_name = attachments_result.value[0].name.split('.')
				attachment_contentBytes = attachments_result.value[0].content_bytes
				attachment_content = base64.b64decode(attachment_contentBytes)
				day = email.created_date_time.day
				month = email.created_date_time.month
				year = email.created_date_time.year
				hour = email.created_date_time.hour
				if (hour != 23):
					print("email not saved")
					continue
				minute = email.created_date_time.minute
				second = email.created_date_time.second
				with open(f"{save_dir}\\{attachment_name[0]}_{day}-{month}-{year}_{hour}-{minute}-{second}.htm", 'wb') as file:
					file.write(attachment_content)
				print("email saved")
	except asyncio.TimeoutError:
		print("The operation timed out.")
	except Exception as e:
		print(f"An error occurred: {e}")

# Get the access token
access_token, expires_on = get_access_token()

if access_token:
	credentials = RawAccessTokenProvider(access_token, expires_on)

else:
	# Obtain a new token
	credentials = DeviceCodeCredential(client_id=client_id, tenant_id=tenant_id)
	token = credentials.get_token(*scopes)
	access_token = token.token
	expires_on = token.expires_on

	# Convert expiration date to a readable format
	expiration_date = datetime.utcfromtimestamp(expires_on).strftime('%Y-%m-%d %H:%M:%S')

	# Save the token and expiration date
	with open(token_save_path, "w") as token_file:
		token_file.write(f"Access Token: {access_token}\n")
		token_file.write(f"Expires On: {expiration_date} UTC\n")

	credentials = RawAccessTokenProvider(access_token, expires_on)

# Create the GraphServiceClient with the credentials
client = GraphServiceClient(credentials=credentials)

if (date.today().weekday() == 0):
	query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
		select=["sender", "subject", "attachments", "receivedDateTime", "sentDateTime", "createdDateTime"], top=10
	)
else:
	query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
		select=["sender", "subject", "attachments", "receivedDateTime", "sentDateTime", "createdDateTime"], top=16
	)
request_configuration = MessagesRequestBuilder.MessagesRequestBuilderGetRequestConfiguration(
	query_parameters=query_params
)

# Run the async function to get emails
asyncio.run(get_mail())

print("HTML files saved in buffer successfully!")
