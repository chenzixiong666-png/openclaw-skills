import json, re, urllib.request
from collections import defaultdict

EMAIL = 'chenzixiong@wondertechlabs.com'
PASSWORD = 'czx123456'
PROJECT_UUID = '13N7SZZESPof4VrY'
TEAM_WEB_KEY = 'J8koxmN0'
KEEP_TYPES = {'固件缺陷','RN缺陷','需求缺陷','后台缺陷'}
EXCLUDE_STATUS = {'回归通过','关闭','非bug'}


def post_json(url, payload, headers=None, timeout=40):
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type':'application/json', **(headers or {})})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode('utf-8', 'replace'))


def login():
    data = post_json('https://ones.cn/api/project/auth/login', {'email': EMAIL, 'password': PASSWORD})
    return {
        'token': data.get('token') or ((data.get('user') or {}).get('token')),
        'user': (data.get('user') or {}).get('uuid'),
        'team': (data.get('teams') or [{}])[0].get('uuid')
    }


def gql(team, user, token, query):
    return post_json(f'https://ones.cn/api/project/team/{team}/items/graphql', {'query': query}, headers={'Ones-User-Id': user, 'Ones-Auth-Token': token})


def shorten(title):
    title = title or ''
    title = re.sub(r'--\s*feedback[:：]?\s*\d+', '', title, flags=re.I).strip()
    module = '未标注模块'
    m = re.match(r'^【([^】]+)】', title)
    if m:
        module = m.group(1).strip()
        title = re.sub(r'^【[^】]+】', '', title).strip()
    title = title.replace('（预期', '，预期').replace('（', '，').replace('）', '')
    title = re.sub(r'\s+', '', title)
    title = title.strip('，。；;')
    return module, title


auth = login()
query = '{ tasks(filter: {project_in: ["%s"]}, limit: 500) { uuid key number name status { name } priority { value } issueType { name } } }' % PROJECT_UUID
resp = gql(auth['team'], auth['user'], auth['token'], query)
tasks = (((resp or {}).get('data') or {}).get('tasks')) or []

result = defaultdict(list)
counts = defaultdict(int)
for t in tasks:
    issue_type = ((t.get('issueType') or {}).get('name')) or ''
    status = ((t.get('status') or {}).get('name')) or ''
    if issue_type not in KEEP_TYPES:
        continue
    if status in EXCLUDE_STATUS:
        continue
    module, short = shorten(t.get('name') or '')
    counts[issue_type] += 1
    url = f'https://ones.cn/project/#/team/{TEAM_WEB_KEY}/project/{PROJECT_UUID}/task/{t.get("uuid")}'
    result[issue_type].append({
        'module': module,
        'text': f'{short}【{status}】【{((t.get("priority") or {}).get("value") or "未标记")}】',
        'url': url,
        'number': t.get('number'),
        'uuid': t.get('uuid')
    })

for k in result:
    result[k].sort(key=lambda x: (x['module'], x['number'] or 0))

print(json.dumps({'counts': counts, 'items': result}, ensure_ascii=False, indent=2))
