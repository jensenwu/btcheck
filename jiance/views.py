#-*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
import requests
import json
import random
from bitcoin import *
# Create your views here.


def jiance(myAddress):
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
        add_dict['blance_my'] = jiance(add_dict['myAddress'])
        add_dict['blance_my_com'] = jiance(add_dict['myAddress_com'])
        c += 1
        add_list.append(add_dict)
    return add_list

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

