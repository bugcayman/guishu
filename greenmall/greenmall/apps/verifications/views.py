from django.shortcuts import render
from rest_framework.views import APIView
from random import randint
from django_redis import get_redis_connection
# Create your views here.
from greenmall.libs.yuntongxun.sms import CCP
from rest_framework.response import Response
import logging

logger = logging.getLogger('django')  # 创建日志输出器

class SMSCodeView(APIView):
    """发送短信验证码"""

    def get(self,request,mobile):
        #1.生成短信验证码

        sms_code = '%06d' % randint(0,999999)
        logger.info(sms_code)
        #2.创建redis
        redis_conn = get_redis_connection('verify_codes')
        #3把验证码存储到redis中
        # redis_conn.setex(key,过期时间,value)
        redis_conn.setex('sms_%s' % mobile ,300,sms_code)
        #4利用荣联运发短信
        CCP().send_template_sms(mobile, [sms_code,5],1)
        #5.相应
        return Response({'massage':'ok'})

