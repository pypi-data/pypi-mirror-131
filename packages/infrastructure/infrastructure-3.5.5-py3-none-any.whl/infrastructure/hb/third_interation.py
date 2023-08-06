# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2021-09-16 20:04:50
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2021-12-16 13:55:59
from infrastructure.http_agent.http_request import HttpRequest
from AppCooltestHotWheelsService.fox.models.rf_directory_structure import RFDirectoryStructure
from AppCooltestHotWheelsService.log.serializers.logPushCasesToHtpFBSerializers import LogPushCasesToHtpFBSerializer

class ThirdInteration(object):
	def __init__(self):
		pass

	def add_caseData(self,rfDirectoryOb,env=''):

		if env:
			env = env
		else:
			env = rfDirectoryOb.env

		tempDict = {'partner_id':str(rfDirectoryOb.id),
							 'name':rfDirectoryOb.name,
							 'env':env,
							 'business':rfDirectoryOb.business}
		tempDict['ref_interfaces'] = list(rfDirectoryOb.rf_interface.all().values_list('name',flat=True)) #用例关联接口
		tempDict['tags'] = list(rfDirectoryOb.rf_customTag.all().values_list('name',flat=True))  #用例标签
		tempDict['owner_services'] = list(rfDirectoryOb.rf_service.all().values_list('name',flat=True)) #用例所属服务
		if rfDirectoryOb.single:
			tempDict['classify'] = ['单接口']
		else:
			tempDict['classify'] = ['多接口']
		creator =	rfDirectoryOb.people.all().order_by('-id').values_list('name',flat=True)
		tempDict['partner_create_by'] = creator[0]+'@hellobike.com' if creator else  ''
		tempDict['partner_create_time'] = rfDirectoryOb.add_time.strftime('%Y-%m-%d %H:%M:%S')
		tempDict['partner_update_time'] = rfDirectoryOb.add_time.strftime('%Y-%m-%d %H:%M:%S')

		return tempDict



	def pushCaseToFox(self,url='http://10.111.30.234:8088/fox/partner/interface/PushPartnerCases',full=False,env='uat'):
		temp = []
		update_data = []
		if full:
			
			for loop in RFDirectoryStructure.objects.filter(script_name__isnull=False,valid=True):
				# tempDict = {'partner_id':str(loop[0]),
				# 			 'name':loop[1],
				# 			 'env':loop[2],
				# 			 'business':loop[3]}

				temp.append(self.add_caseData(loop))

			for loop in RFDirectoryStructure.objects.filter(script_name__isnull=False,valid=True,env="uat"):
				temp.append(self.add_caseData(loop,env='fat'))
			mode = 'full'
			

		else:
			#新增
			for loop in RFDirectoryStructure.objects.filter(script_name__isnull=False,valid=True,env=env,new_case=True):
				temp.append(self.add_caseData(loop))
				if env == "uat":
					temp.append(self.add_caseData(loop,env='fat'))
			# 增加更新数据,主要是tag会更新
			for loop in RFDirectoryStructure.objects.filter(script_name__isnull=False,valid=True,env=env,new_case=False):
				update_data.append(self.add_caseData(loop))
				if env == "uat":
					update_data.append(self.add_caseData(loop,env='fat'))

			mode = 'increment'

		delete_data = [str(loop) for loop in list(RFDirectoryStructure.objects.filter(script_name__isnull=False,delete_push=True).values_list('id',flat=True))]


		headers = {'content-type': "application/json;charset=UTF-8"}
		data = {
			"type": "1",
			"mode": mode,
			"add_data": temp,
			"delete_data": delete_data,
			"update_data": update_data
		}
		# print(data)
		response = HttpRequest.post(url,headers=headers,data=data)
		print(response)
		logHtpFB = LogPushCasesToHtpFBSerializer(data={"message":str(response)})
		logHtpFB.is_valid(raise_exception=True)
		logHtpFB.save()

		if response.get('result',{}).get('status',False):
			print('delete')
			RFDirectoryStructure.objects.filter(env=env,valid=True,script_name__isnull=False,new_case=True).update(new_case=False)
			RFDirectoryStructure.objects.filter(delete_push=True).update(delete_push=False)
		return response




