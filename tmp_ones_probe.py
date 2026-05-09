import urllib.request, json

login_payload = {'email':'chenzixiong@wondertechlabs.com','password':'czx123456'}
req = urllib.request.Request(
    'https://ones.cn/api/project/auth/login',
    data=json.dumps(login_payload).encode('utf-8'),
    headers={'Content-Type':'application/json'}
)
resp = json.loads(urllib.request.urlopen(req, timeout=30).read().decode('utf-8','replace'))
token = resp.get('token') or ((resp.get('user') or {}).get('token'))
team = resp.get('teams',[{}])[0].get('uuid')
user = (resp.get('user') or {}).get('uuid')
print(json.dumps({'team':team,'user':user,'token_present':bool(token)}, ensure_ascii=False))
q = '{ tasks(filter: {project_in: ["13N7SZZESPof4VrY"]}, limit: 5) { uuid number name key status { name } issueType { name } } }'
req2 = urllib.request.Request(
    f'https://ones.cn/api/project/team/{team}/items/graphql',
    data=json.dumps({'query':q}).encode('utf-8'),
    headers={'Content-Type':'application/json','Ones-User-Id':user,'Ones-Auth-Token':token}
)
resp2 = json.loads(urllib.request.urlopen(req2, timeout=30).read().decode('utf-8','replace'))
print(json.dumps(resp2, ensure_ascii=False, indent=2))
