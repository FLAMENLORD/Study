import json
import locale
import os
from datetime import datetime

import logging
import yaml
from httprunner.task import HttpRunner
from httprunner.report import render_html_report
from rest_framework.response import Response

from debugtalks.models import DebugTalks
from configures.models import Configures
from testcases.models import Testcases
from reports.models import Reports

logger = logging.getLogger('mytest')


def datetime_fmt():
	locale.setlocale(locale.LC_CTYPE, 'chinese')
	return '%Y-%m-%d %H:%M:%S'

def create_report(runner, report_name=None):
	time_stamp = int(runner.summary['time']['start_at'])
	start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
	runner.summary['time']['start_datetime'] = start_datetime
	runner.summary['time']['duration'] = round(runner.summary['time']['duration'], 3)
	report_name = report_name if report_name else start_datetime
	runner.summary['html_report_name'] = report_name

	for item in runner.summary['details']:
		try:
			for record in item['records']:
				record['meta_data']['response']['content'] = record['meta_data']['response']['content'].decode('utf-8')
				record['meta_data']['response']['cookies'] = dict(record['meta_data']['response']['cookies'])
				request_body = record['meta_data']['request']['body']
				if isinstance(request_body, bytes):
					record['meta_data']['request']['body'] = request_body.decode('utf-8')
		except Exception as e:
			logger.error(e)
			continue

	summary = json.dumps(runner.summary, ensure_ascii=False)
	report_name = report_name + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
	report_path = runner.gen_html_report(html_report_name=report_name)

	with open(report_path, encoding='utf-8') as stream:
		reports = stream.read()

	test_report = {
		'name': report_name,
		'result': runner.summary.get('success'),
		'success': runner.summary.get('stat').get('successes'),
		'count': runner.summary.get('stat').get('testsRun'),
		'html': reports,
		'summary': summary
	}
	report_obj = Reports.objects.create(**test_report)
	return report_obj.id


def generate_testcase_file(instance, env, testcase_dir_path):
	testcase_list = []
	config = {
		'config': {
			'name': instance.name,
			'requset': {
				'base_url': env.base_url if env else ''
			}
		}
	}
	testcase_list.append(config)

	include = json.loads(instance.include, encoding='utf-8')
	request = json.loads(instance.request, encoding='utf-8')
	interface_name = instance.interface.name
	project_name = instance.interface.project.name
	project_id = instance.interface.project.id

	# 项目路径 生成文件
	testcase_dir_path = os.path.join(testcase_dir_path, project_name)
	if not os.path.exists(testcase_dir_path):
		os.makedirs(testcase_dir_path)
		# 生成debugtalk.py文件，放到项目根目录
		debugtalk_obj = DebugTalks.objects.filter(project=project_id).first()
		debugtalk = debugtalk_obj.debugtalk if debugtalk_obj else ''
		with open(os.path.join(testcase_dir_path, 'debugtalk.py'), 'w', encoding='utf-8') as f:
			f.write(debugtalk)

	# 接口路径 生成文件
	testcase_dir_path = os.path.join(testcase_dir_path, interface_name)
	if not os.path.exists(testcase_dir_path):
		os.makedirs(testcase_dir_path)

	# 处置用例全局配置
	if 'config' in include:
		config_id = include.get('config')
		config_obj = Configures.objects.filter(id=config_id).first()
		if config_obj:
			try:
				config_request = json.loads(config_obj.request, encoding='utf-8')
			except Exception as e:
				logger.error(e)

			config_request['config']['request']['base_url'] = env.base_url if env else ''
			testcase_list[0] = config_request

	# 处理前置用例
	if 'testcases' in include:
		for testcase_id in include.get('testcases'):
			testcase_obj = Testcases.objects.filter(id=testcase_id).first()
			try:
				testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
			except Exception as e:
				logger.error(e)
				continue
			testcase_list.append(testcase_request)

	# 将当前需要执行的用例追加到testcase_list
	testcase_list.append(request)
	with open(os.path.join(testcase_dir_path, instance.name + '.yaml'), 'w', encoding='utf-8') as f:
		yaml.dump(testcase_list, f, allow_unicode=True)


# 运行用例
def run_testcase(instance, testcase_dir_path):
	runner = HttpRunner()
	try:
		runner.run(testcase_dir_path)
	except Exception as e:
		logger.error(e)
		res = {'result': False, 'msg': '用例执行失败'}
		return Response(res, status=400)

	# 创建报告，将记录添加到report表
	report_id = create_report(runner, instance.name)

	# 运行成功，打开报告
	data = {
		'id': report_id
	}
	return Response(data, status=201)
