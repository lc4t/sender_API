from send_core.models import Function


params = {
    "input": [
        {
            "type": "text",
            "name": "number",
            "value": "",
            "descript": "快递单号"
        },
        {
            "type": "text",
            "name": "company",
            "value": "",
            "descript": "快递公司，点击按钮查询，默认为auto"
        }
    ],
    "ajax": {
        "text": "查询公司",
    }
}

Function.objects.create(name='express_tracking', author='lc4t', title='快递跟踪提醒', descript='将快递每一步路由更新发送到邮箱', status=True, params=params)
