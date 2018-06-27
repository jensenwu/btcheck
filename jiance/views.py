#-*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
import requests
import json
import random
from bitcoin import *
from django.conf import settings  # 导入配置文件
from django.core.mail import send_mail  # 导入发送邮件的包
# Create your views here.


def Email_send(title,content):
    send_title = title
    send_message = content
    send_obj_list = ['jensen.wu@foxmail.com']  # 收件人列表
    send_html_message = '<h1>包含 html 标签且不希望被转义的内容</h1>'
    send_status = send_mail(send_title, send_message, settings.EMAIL_HOST_USER, send_obj_list, send_html_message)
    print send_status  # 发送状态,可用可不用


def jiance(myAddress,number):
        user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        headers={'User-agent':user_agent}
        url = 'https://blockchain.info/multiaddr?active='+myAddress
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
                content=response.content
                html = json.loads(content)
                #print html
                a= html['wallet']['final_balance']
                b=html['wallet']['total_received']
                if a != 0 or b != 0:
                    Email_send(myAddress,number)
                return {'final_balance':a,'total_received':b}
        else:
                print None
                return None


def random_number():
    number_weishu  = random.randint(3,76)
    sum = ''
    for i in xrange(number_weishu):
        num_ran = random.randint(0,9)
        sum += str(num_ran)
    if long(sum)< 7237005577332262213973186563042994240829374041602535252466099000494570602495:
        return long(sum)
    else:
        random_number()


def get_list(number):
 try:
    b = hex(long(number))
    c = long(b,16)
    c*=16
    add_list = []
    for i in xrange(16):
        add_dict = {}
        add_dict['mySecretKey'] = encode_privkey(c, "wif")
        add_dict['mySecretKey_com'] = encode_privkey(c,'wif_compressed')
        add_dict['myAddress'] = pubtoaddr(privtopub(add_dict['mySecretKey']))
        add_dict['myAddress_com'] = pubtoaddr(privtopub(add_dict['mySecretKey_com']))
        add_dict['blance_my'] = jiance(add_dict['myAddress'],number)
        add_dict['blance_my_com'] = jiance(add_dict['myAddress_com'],number)
        c += 1
        add_list.append(add_dict)
    return add_list
 except Exception,e:
     a = random_number()
     get_list(a)


def index(request):
        if request.method =="POST":
            number1 = request.POST.get("number")
            print number1
            if number1 is not None:
                number = number1
                add_list = get_list(number)
                return render(request, 'index.html',{'add_list':add_list,'number':number})
            else:
                number = random_number()
                add_list = get_list(number)
                return render(request, 'index.html',{'add_list':add_list,'number':number})
        else:

            number = random_number()
            add_list = get_list(number)
            return render(request, 'index.html',{'add_list':add_list,'number':number})


