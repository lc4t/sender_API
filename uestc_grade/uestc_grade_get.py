# -*- coding:UTF-8 -*-
__author__ = 'lc4t'

import re
import urllib
import requests
import datetime
from requests.utils import cookiejar_from_dict, dict_from_cookiejar
from bs4 import BeautifulSoup
from optparse import OptionParser
import http.cookiejar
from urllib.parse import urlencode
import time
import lxml
import json


def judgeExistMakeupGrade(gradeList):
    # (list, makeup, offset)
    rtnList = []
    last = -1
    makeup = 0
    offset = 0
    length = len(gradeList)
    for i in range(1, length):
        if re.findall('\d{4}-\d{4}\s\d', gradeList[i]):
            last = i
            break
    if last == -1:  # the last grade.
        rtnList = gradeList
        offset = length
    else:
        rtnList = gradeList[0:last] # 下一个grade头部在中间,index是last
        offset = last

    # fix not have courseid details
    c = rtnList[1]
    c_details = rtnList[2]
    if re.findall('^[A-Za-z\d\.\-\(\)]+$' ,c_details):  # do not need fix details
        pass
    elif c_details == '参加社会实践 完成总结报告':
        rtnList.insert(2, c)
    else:
        rtnList.insert(2, c)
    rtn_length = len(rtnList)
    if rtn_length == 8:
        makeup = 1
    elif rtn_length == 7:
        makeup = 0
    elif rtn_length == 6:
        rtnList.insert(5, rtnList[-1])
    else:
        raise ValueError(gradeList)
    return (rtnList, makeup, offset)

class TermStruct:
    def __init__(self):
        self.__length__ = 0
        self.academicYear = []
        self.term = []
        self.numberOfCourses = []
        self.totalCredit = []
        self.gpa = []
        self.all = []
        self.time = []
    def add(self, Academic_Year, Term, Number_Of_Courses, Total_Credit, GPA):
        self.academicYear.append(Academic_Year)
        self.term.append(Term)
        self.numberOfCourses.append(Number_Of_Courses)
        self.totalCredit.append(Total_Credit)
        self.gpa.append(GPA)
        self.__length__ += 1

    def addList(self,list):
        # print ('----in addList----')
        # print (list)

        self.academicYear.append(list[0])
        self.term.append(list[1])
        self.numberOfCourses.append(list[2])
        self.totalCredit.append(list[3])
        self.gpa.append(list[4])
        self.__length__ += 1
        # print ('----out addList----')

    def addFinal(self,allGPA,time):
        self.all = allGPA
        self.time = time

    def getFinal(self):
        return [self.all,self.time]

    def printAll(self):
        pass
        # for i in range(0,self.__length__,1):
        #     print (self.academicYear[i],end=' ')
        #     print (u"第",end=' ')
        #     print (self.term[i],end=' ')
        #     print (u"学期 共",end=' ')
        #     print (self.numberOfCourses[i],end=' ')
        #     print (u"门课 总学分",end=' ')
        #     print (self.totalCredit[i],end=' ')
        #     print (u"平均绩点",end=' ')
        #     print (self.gpa[i])

    def printFinal(self):
        pass
        # print ('---- in printFinal ----')
        # print (u"总课程数:",self.all[0],end=' ')
        # print (u"总学分:",self.all[1],end=' ')
        # print (u"总评绩点:",self.all[2])
        # print (u"统计时间:",self.time[0])
        # print ('---- out printFinal ----')
        # pass

    def getTerm(self, number):
        return ([self.academicYear[number], self.term[number], self.numberOfCourses[number],
                 self.totalCredit[number], self.gpa[number]])

    def getCourseNumber(self):
        return self.all[0]

    def getCourseAll(self):
        pass


class Coursestruct:
    def __init__(self):
        self.count = 0
        self.academicYear = []
        self.semester = []
        self.courseCode = []
        self.courseNumber = []
        self.courseName = []
        self.courseType = []
        self.courseCredit = []
        self.courseGrade = []
        self.courseFinal = []
        self.courseGPA = []
        self.makeupGrade = []
        self.isMakeup = 0
    def add(self,course, adjuster, makeup = 0):
        course[0] = course[0].encode('ascii').decode()
        self.academicYear.append(course[0][1:10])
        self.semester.append(course[0][-1])
        # print (self.semester)

        course[1] = course[1].encode('ascii')
        self.courseCode.append(course[1])
        try:
            course[2] = course[2].encode('ascii')
        except:
            course.insert(2,course[1].decode().encode('ascii'))
            adjuster = adjuster - 1      # if init course[2] is NULL,there can't encode as 'ascii'

        self.courseNumber.append(course[2])
        self.courseName.append(course[3])

        self.courseType.append(course[4].split(' ')[0])

        self.courseCredit.append(course[4].split(' ')[1])
        # print (course[4][-1])


        if (makeup):
            self.isMakeup = 1
            self.makeupGrade.append(course[6].strip())
        else:
            self.makeupGrade.append('')


        try:
            self.courseGrade.append(int(course[5]))
            self.courseFinal.append(int(course[6 + makeup]))
        except:
            if (re.findall(u'未通过',course[5]) != None):
                self.courseGrade.append(0)
                self.courseFinal.append(0)
            elif (re.findall(u'通过',course[5]) != None):
                self.courseGrade.append(100)
                self.courseFinal.append(100)
            else:
                print (u"发现不知名的成绩..")

        if (self.courseGrade[self.count] >= 85):
            self.courseGPA.append(4)
        elif (self.courseGrade[self.count] < 60):
            self.courseGPA.append(1)
        else:
            self.courseGPA.append('%.1f' % (4 - (85 - self.courseGrade[self.count]) * 0.1))



        self.count += 1
        return adjuster


    def printCourses(self):
        for i in range(0,self.count, 1):
            print (self.academicYear[i],end=' ')
            print (u"第",end=' ')
            print (self.semester[i],end=' ')
            print (u"学期",end=' ')
            # print (self.courseCode[i],)
            # print (self.courseNumber[i],)
            # print (self.courseType,)
            print (" --> ",)
            print (self.courseName[i].encode('utf-8').decode(),end=' ')
            print (self.courseType[i].encode('utf-8').decode())
            # print ("-------------------------------------------> ",)
            print ("----------------------> ",end=' ')
            print (self.courseCredit[i],end=' ')
            print (u"学分",end=' ')
            print (u"总评",end=' ')
            print (self.courseGrade[i],end=' ')
            print (u"最终",end=' ')
            print (self.courseFinal[i],end=' ')
            print (u"单科绩点",self.courseGPA[i],)
            if (self.isMakeup == 1 and self.makeupGrade[i] != '--'):
                print (u"补考成绩 ",end=' ')
                print (self.makeupGrade[i])
            else:
                print ("")
    def getCoursesJSON(self):

        li = []
        for i in range(0,self.count, 1):
            newDict = {'academisc':self.academicYear[i],
                       'semester':self.semester[i],
                       'courseCode':self.courseCode[i].decode(),
                       'number':self.courseNumber[i].decode(),
                       'courseName':self.courseName[i].encode('utf-8').decode(),
                       'courseType':self.courseType[i].encode('utf-8').decode(),
                       'credit':self.courseCredit[i],
                       'totalGrade':self.courseGrade[i],
                       'makeupGrade':self.makeupGrade[i],
                       'finalGrade':self.courseFinal[i],
                       'gradePoint':self.courseGPA[i]}
            li.append(newDict)

        return li


class GradeAnalyzer:

    def __init__(self,html):
        self.soup = BeautifulSoup(html, 'lxml')

        '''
            griddata-even + griddata-odd 交叉排列
            分别放在list内,
            其中even最后一个是在校汇总,odd最后一个是统计时间

        '''
        self.termData = TermStruct()
        self.coursesData = Coursestruct()

    def getTotal(self):
        self.griddata_even = self.soup.select(".griddata-even")
        self.griddata_odd  = self.soup.select(".griddata-odd")
        self.griddata = []
        for i in range(0, len(self.griddata_even), 1):
            self.griddata.append(self.griddata_even[i].get_text())
        for j in range(0, len(self.griddata_odd), 1):
            self.griddata.append(self.griddata_odd[j].get_text())

        for i in range(0,len(self.griddata), 1):
            self.griddata[i] = self.griddata[i].strip('\n').split('\n')
            if (len(self.griddata[i]) < 5):
                continue
            self.termData.addList(self.griddata[i])
        self.termData.printAll()
        self.griddata = []
        if (len(self.griddata_even) > len(self.griddata_odd)):
            ### 1,3,5,7 term
            self.griddata.append(self.griddata_odd[-1].get_text().encode('ascii','ignore').decode().strip('\n').split('\n'))
            self.griddata.append(self.griddata_even[-1].get_text().encode('ascii','ignore').decode().strip('\n').strip(':').split('\n'))
        else:
            ### 2,4,6,8 term
            self.griddata.append(self.griddata_even[-1].get_text().encode('ascii','ignore').decode().strip().split())
            self.griddata.append(self.griddata_odd[-1].get_text().encode('ascii','ignore').decode().strip('\n').strip(':').split('\n'))

        self.termData.addFinal(self.griddata[0],self.griddata[1])
        self.termData.printFinal()

    def getCourses(self):
        self.total = self.termData.getCourseNumber()
        self.gridCourses = self.soup.find(id = re.findall('<tbody id="(grid\d+_data)"', self.soup.prettify())[0]).get_text()

        temp = re.findall('(?u).*',self.gridCourses)
        tempA = []
        for i in range(0,len(temp),1):
            if (temp[i] == ''):
                continue
            else:
                tempA.append(temp[i])


        i = 0
        while(i < len(tempA)):
            checker = judgeExistMakeupGrade(tempA[i:i + 10])
            rtnList = checker[0]
            isMakeup = checker[1]
            offset = checker[2]
            i = self.coursesData.add(rtnList, i, isMakeup)
            i += offset
        return self.coursesData.getCoursesJSON()

class uestc():
    def __init__(self):
        self.r = requests.Session()
        self.loginURL = "http://idas.uestc.edu.cn/authserver/login?service=http://portal.uestc.edu.cn/index.portal"
        self.indexURL = 'http://portal.uestc.edu.cn/index.portal'
        self.urlEAS = "http://eams.uestc.edu.cn/eams/"
        self.urlCurriculumManager = "http://eams.uestc.edu.cn/eams/home!childmenus.action?menu.id=844"
        self.urlMygrade = "http://eams.uestc.edu.cn/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR"
        self.urlCourses = "http://eams.uestc.edu.cn/eams/courseTableForStd!courseTable.action"
        self.headers = {
            'Proxy-Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://portal.uestc.edu.cn/index.portal',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8',
        }

    def login_cookies(self, cookies_dict):
        url = self.urlEAS + 'home.action'
        self.r.cookies = cookiejar_from_dict(cookies_dict, cookiejar=None, overwrite=True)
        login_r = self.r.get(url, headers=self.headers)
        result = login_r.text
        AC = re.findall('href="/eams/security/my.action"',result)
        if AC:
            return json.dumps(cookies_dict)
        else:
            return False


    def login_password(self, username, password):
        self.r.cookies.clear()
        loginURLCaptcha = "http://idas.uestc.edu.cn/authserver/needCaptcha.html?username=%s&_=%s" % (username, str(time.time()))
        visit_r = self.r.get(url=self.loginURL, headers=self.headers)
        check_captcha_r = self.r.get(loginURLCaptcha, headers=self.headers)
        if check_captcha_r.text == 'true':
            print(username + 'need captcha')
            return False
        params_lt = re.findall('name="lt" value="(.*)"/>',visit_r.text)[0]
        post_data = {
            'username': username,
            'password': password,
            'lt': params_lt,
            'dllt': 'userNamePasswordLogin',
            'execution': 'e1s1',
            '_eventId': 'submit',
            'rmShown': '1'
        }
        login_r = self.r.post(url=self.loginURL, data=post_data, headers=self.headers)

        result = login_r.text
        AC = re.findall('https://mail.std.uestc.edu.cn/"><br', result)
        if AC:
            res = self.get_eas()
            return json.dumps({'JSESSIONID': res})
        else:
            return False


    def get_courses(self, pretty = False):
        self.get_index()
        self.get_eas()
        self.get_curriculum_manager()
        raw_grades = self.get_my_grade()
        if pretty:
            grade = GradeAnalyzer(raw_grades)
            grade.getTotal()
            return grade.getCourses()
        else:
            return raw_grades

    #first step to login, this is index page
    def get_index(self):     # login index page
        _ = self.r.get(self.indexURL, headers=self.headers)
        return _.text



    # second step to get course, this is the page after login
    def get_eas(self):    #  click educational administration system
        _ = self.r.get(url=self.urlEAS, headers=self.headers)
        JSESSIONID = _.url.split('=')[-1]
        _ = self.r.get(url=self.urlEAS+'home.action', headers=self.headers)
        return JSESSIONID
        # print(_.cookies)
        # input()
        # exit()
        # return _.text

    def get_curriculum_manager(self):  # table
        _ = self.r.get(url=self.urlCurriculumManager, headers=self.headers)
        return _.text


    def get_my_grade(self):
        _ = self.r.get(url=self.urlMygrade, headers=self.headers)
        return _.text


if __name__ == '__main__':
    u =  uestc()
    print(u.login_password('', ''))
    print(u.login_cookies({"JSESSIONID": "2B0F740A836614C7FC1DD84A57A6F840"}))
    raw_data = u.get_courses(pretty=True)
    print(type(raw_data))
    print(raw_data)
    # g = GradeAnalyzer(raw_data)
