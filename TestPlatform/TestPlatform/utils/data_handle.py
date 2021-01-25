# key-value
def key_value(test_data):
	restult = []
	if test_data:
		if isinstance(test_data, list):
			for i in test_data:
				key = list(i)[0]
				value = i.get(key)
				restult_data = {
					'key': key,
					'value': value
				}
				restult.append(restult_data)
		elif isinstance(test_data, dict):
			for key, value in test_data.items():
				restult.append({
					"key": key,
					"value": value
				})
	return restult


# key
def key_(test_data):
	restult = []
	if test_data:
		for i in test_data:
			restult_data = {
				'key': i
			}
			restult.append(restult_data)
	return restult


# key-value-param_type
def key_value_paramtype(test_data):
	restult = []
	if test_data:
		if isinstance(test_data, list):
			for i in test_data:
				key = list(i)[0]
				value = i.get(key)
				restult.append({
					"key": key,
					"value": value,
					"param_type": type(value).__name__
				})
		elif isinstance(test_data, dict):
			for key, value in test_data.items():
				restult.append({
					"key": key,
					"value": value,
					"param_type": type(value).__name__
				})
	return restult


def handle_validate(test_data):
	restult = []
	if test_data:
		for i in test_data:
			restult_data = {
				'key': i.get('check'),
				'value': i.get('expected'),
				'comparator': i.get('comparator'),
				'param_type': type(i.get('expected')).__name__,
			}
			restult.append(restult_data)
	return restult

#
# def data_type(data):
# 	if isinstance(data, int):
# 		return 'int'
# 	if isinstance(data, str):
# 		return 'string'
# 	if isinstance(data, float):
# 		return 'float'
# 	if isinstance(data, bool):
# 		return 'boolen'
#
