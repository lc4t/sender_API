import json
from send_core.models import Function


params = {
    "input": [
        {
            "type": "text",
            "name": "url",
            "value": "http://",
            "descript": "完整URL"
        },
        {
            "type": "text",
            "name": "match",
            "value": "",
            "descript": "匹配此正则时通知"
        },
        {
            "type": "text",
            "name": "nmatch",
            "value": "",
            "descript": "不匹配此正则时通知"
        },
        {
            "type": "text",
            "name": "headers",
            "value": "{}",
            "descript": "设置headers，可以为空"
        },
    ],
}
params = json.dumps(params, ensure_ascii=False)
Function.objects.create(name='web_change', author='lc4t', title='web内容变化提醒', descript='当两个正则状态成立时，发送邮件提醒', status=True, params=params, ajax=False)
