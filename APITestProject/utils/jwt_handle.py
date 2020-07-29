import rest_framework_jwt

def jwt_response_payload_handler(token, user=None, requset=None):
	return {
		'user_id': user.id,
		'username': user.username,
		'token': token
	}