import json
from send_core.models import Function


params = {
    "input": [
        {
            "type": "text",
            "name": "number",
            "value": "",
            "descript": "学号"
        },
        {
            "type": "password",
            "name": "password",
            "value": "",
            "descript": "信息门户密码"
        },
        {
            "type": "text",
            "name": "JSESSIONID",
            "value": "",
            "descript": "exam的JSESSIONID, 如果为将通过password获取"
        }
    ],
}
params = json.dumps(params, ensure_ascii=False)
Function.objects.create(name='uestc_grade', author='lc4t', title='uestc成绩跟踪', descript='将新成绩发送到邮箱', status=True, params=params, ajax=False)
