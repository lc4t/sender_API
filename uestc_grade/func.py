from send_core.models import Task, Function, Log
from django.utils.timezone import now
from uestc_grade.models import Account, Grade
from uestc_grade.uestc_grade_get import uestc
import datetime
import json


def plus():
    functions = Function.objects.filter(name='uestc_grade')
    function = functions[0]
    function.count += 1
    function.save()


def get_my_task():
    functions = Function.objects.filter(name='uestc_grade', status=True)
    if len(functions) == 1:
        function = functions[0]
        tasks = Task.objects.filter(function=function)
        if len(tasks) > 0:
            return tasks
        else:
            return []
    else:
        return []


def check_one(taskid):
    task = Task.objects.filter(id=taskid)[0]
    params = json.loads(task.params)
    username = params.get('input')[0].get('value')
    password = params.get('input')[1].get('value')
    cookie = params.get('input')[2].get('value')
    accounts = Account.objects.filter(task=task)
    if len(accounts) == 0:
        account = Account.objects.create(belongs=task.person, username=username, password=password, task=task, cookie=cookie)
    else:
        account = accounts[0]

    if account.cookie != '':
        cookie = account.cookie
    else:
        account.cookie = cookie
        account.save()
    u = uestc()
    cookie_dict = {
        'JSESSIONID': cookie,
    }
    status = False
    if u.login_cookies(cookie_dict):
        status = True
        Log.objects.create(task=task, text='cookie login success')
    else:
        check = u.login_password(username, password)
        if check == False:
            Log.objects.create(task=task, text='cookie login failed')
            failed(task)
            status = False
        else:
            status = True
            Log.objects.create(task=task, text='password login success, save cookie')
            cookie_dict = json.loads(check)
            account.cookie = cookie_dict.get('JSESSIONID')
            account.save()
    new_message = []
    if status:
        success(task)
        grade_list = u.get_courses(pretty=True)
        # text = json.dumps(grade_list, ensure_ascii=False, indent=4)
        # if len(Log.objects.filter(task=task, text=text)) == 0:
        #     Log.objects.create(task=task, text=text)
        # else:
        #     Log.objects.create(task=task, text='same data')
        for g in grade_list:
            academisc = g.get('academisc')
            semester = g.get('semester')
            courseCode = g.get('courseCode')
            number = g.get('number')
            courseName = g.get('courseName')
            courseType = g.get('courseType')
            credit = g.get('credit')
            totalGrade = str(g.get('totalGrade'))
            makeupGrade = str(g.get('makeupGrade'))
            finalGrade = str(g.get('finalGrade'))
            gradePoint = str(g.get('gradePoint'))
            exists_grades = Grade.objects.filter(account=account, number=number, academisc=academisc, semester=semester)
            exists_num = len(exists_grades)

            if exists_num == 0 or exists_num > 1:   # 喵喵喵????????
                Grade.objects.create(account=account, academisc=academisc, semester=semester,
                                     courseCode=courseCode, number=number,
                                     courseName=courseName, courseType=courseType,
                                     credit=credit, totalGrade=totalGrade,
                                     makeupGrade=makeupGrade, finalGrade=finalGrade,
                                     gradePoint=gradePoint)
                new_message.append(g)
            elif exists_num == 1:
                grade = exists_grades[0]
                if grade.totalGrade == totalGrade and grade.makeupGrade == makeupGrade and grade.finalGrade == finalGrade and grade.gradePoint == gradePoint:
                    continue
                else:
                    grade.totalGrade = totalGrade
                    grade.makeupGrade = makeupGrade
                    grade.finalGrade = finalGrade
                    grade.gradePoint = gradePoint
                    grade.save()
                    new_message.append(g)
    if len(new_message) > 0:
        LOG.objects.create(task=task, text=json.dumps(new_message, ensure_ascii=False, indent=4))
    return new_message


def failed(task):
    task.last_exec = now()
    task.check += 1
    task.next_exec = now() + datetime.timedelta(minutes= 30 * check)
    task.failed += 1
    if 1 <= task.check <= 4:
        task.status = 'failed %d time' % task.check
    else:
        task.status = 'stop'
    task.save()


def success(task):
    task.status = 'running'
    task.success += 1
    task.check = 0
    task.last_exec = now()
    task.next_exec = now() + datetime.timedelta(minutes=30)
    task.save()
