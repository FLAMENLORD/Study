
def jwt_response_payload_handler(token, user=None, requset=None):
	return {
		"data": {
			'user_id': user.id, 'username': user.username, 'token': token
		},
		"statusCode": 200

	}
