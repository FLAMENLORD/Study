# 获取文件流，返回给前端
# 创建一个生成器，获取文件流，每次获取的是字节数据


def get_file_content(filename, read_size):
	with open(filename, encoding='utf-8') as file:
		while True:
			content = file.read(read_size)
			if not content:
				break
			yield content