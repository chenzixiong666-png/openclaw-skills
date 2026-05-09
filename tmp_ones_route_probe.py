import urllib.request, json

login={'email':'chenzixiong@wondertechlabs.com','password':'czx123456'}
req=urllib.request.Request('https://ones.cn/api/project/auth/login', data=json.dumps(login).encode('utf-8'), headers={'Content-Type':'application/json'})
resp=json.loads(urllib.request.urlopen(req, timeout=30).read().decode('utf-8','replace'))
token=resp.get('token') or ((resp.get('user') or {}).get('token'))
team=(resp.get('teams') or [{}])[0].get('uuid')
user=(resp.get('user') or {}).get('uuid')

queries=[
    ('components','{ components(limit: 50) { uuid name key } }'),
    ('views','{ views(limit: 50) { uuid name key } }'),
    ('project','{ projects(limit: 200) { uuid name key } }')
]
for name,q in queries:
    try:
        req2=urllib.request.Request(
            f'https://ones.cn/api/project/team/{team}/items/graphql',
            data=json.dumps({'query':q}).encode('utf-8'),
            headers={'Content-Type':'application/json','Ones-User-Id':user,'Ones-Auth-Token':token}
        )
        data2=json.loads(urllib.request.urlopen(req2, timeout=30).read().decode('utf-8','replace'))
        print('===',name,'===')
        print(json.dumps(data2, ensure_ascii=False, indent=2))
    except Exception as e:
        print('===',name,'ERROR===')
        print(repr(e))
