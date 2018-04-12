# -*- coding: UTF-8 -*-
from django.shortcuts import render
from .exei import run_u, get_late_time
import random
import json
from django.http import HttpResponse
from time import sleep
from datetime import datetime
uid = [253398, 248397]

def main(request):
    #RunTime = str(random.randint(720, 1000))
    RunTime = 5
    if request.method == 'POST':
        choice = request.POST['IMEI']
    #    print(uid[int(choice)-1])
        try:
            last_time = get_late_time(uid[int(choice)-1])
     #       print(last_time)
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')[:10]
     #       print(now)
        except:
            return HttpResponse(json.dumps("0"), content_type='application/json')
        if last_time == now:
        #    print(last_time)
        #    print(now)
            return HttpResponse(json.dumps("2"), content_type='application/json')
        if int(choice) == 1:
            IMEI = 'f55ed0d195f94077b42010a470f68de2'
            RunDist = str(1600 + random.randint(0, 3))  # meters
            RunStep = str(random.randint(1000, 1300))
            # sleep(RunTime)
            # # content = {
            # #     'IMEI': IMEI,
            # # }
            # # print(IMEI)
            # # return render(request, 'online/a.html', content)
            # return HttpResponse(json.dumps("1"), content_type='application/json')
        else:
            IMEI = '61afed5fef034a4ea88121de723bea68'
            RunDist = str(2000 + random.randint(0, 3))  # meters
            RunStep = str(random.randint(1300, 1600))
            # sleep(RunTime)
            # # content = {
            # #     'IMEI': IMEI,
            # # }
            # # print(IMEI)
            # # return render(request, 'online/a.html', content)
            # return HttpResponse(json.dumps("1"), content_type='application/json')
        T = run_u(IMEI, RunStep, RunDist, RunTime)
        if T:
            return HttpResponse(json.dumps("1"), content_type='application/json')
        else:
            return HttpResponse(json.dumps("0"), content_type='application/json')

    else:
        return render(request, 'online/a.html', {'time': RunTime})

