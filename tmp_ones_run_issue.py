import json
import urllib.request
import urllib.error

TEAM = '98Q19ZsW'
USER = 'B3pYJW1D'
TOKEN = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1ZGNkZjRlLTBlYWMtNGE1NS00MGY5LTEzOTIxM2JjZmIzNyIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZGVmYXVsdCJdLCJjbGllbnRfaW5mbyI6eyJjbGllbnRfaXAiOiIxMTMuODkuMjQ1LjUzIn0sImV4cCI6MTc5MjY2MDU0OCwiaWF0IjoxNzc3MTA4MjQ4LCJqdGkiOiJlYTdmYzJlNi05YTU2LTQyYjItNzU0Mi1lOGI3YWRlZjQ5YWEiLCJsb2dpbl90aW1lIjoxNzc3MTA4NTQ4NjgyLCJuYmYiOjE3NzcxMDgyNDgsIm9yZ191c2VyX3V1aWQiOiJCM3BZSlcxRCIsIm9yZ191dWlkIjoiVHNQVGFYRDciLCJyZWdpb25fdXVpZCI6ImRlZmF1bHQiLCJzY29wZXMiOlsib3BlbmlkIiwib2ZmbGluZV9hY2Nlc3MiLCJsZWdhY3kiLCJvbmVzOm9yZzpkZWZhdWx0OlRzUFRhWEQ3OkIzcFlKVzFEIl0sInNpZCI6IjI4YjI0MDMwLTkwMzMtNGUyNi01ZGJkLWZiYTJjOWY5ZTIwYiIsInN1YiI6IkJjYmZTM2FmOmRlZmF1bHQ6VHNQVGFYRDc6QjNwWUpXMUQifQ.PGzUFx6yb2gMzUHZ9_G--p1k3qjgbJVAI3AU-Dr5VWGarrOLRBHsqnYzCrSyVouJO10xs8V2Vhgv4hRrCat_MgKs0lzumdVvpa-OEFZv7MLFnHYxk9Lxx4emuOVcaHihaw2yob8tKIOgRxrG7mcjyoELKV4YhWS26H_VQSTTVS5gBb6X81Uyajk4yO2BJOHvoeWpeR6n7eqcEIG3s60Ybw1UVUYMKbKjl8QaQLxINptGzyVcNualiP4xerPn2I-jFSq29Sof6U7X5dc_ZMGW3qBvE3PIhY_MUwC0VGDr27psHxoY7ZO5V66pqR0MNeOJRgUHVJwL9JAzB7qS2kmiSA'
query = '{ tasks(filter: {project_in: ["W1141"]}, limit: 50) { uuid name number } }'
payload = json.dumps({'query': query}).encode()
req = urllib.request.Request(
    f'https://ones.cn/api/project/team/{TEAM}/items/graphql',
    data=payload,
    headers={'Ones-User-Id': USER, 'Ones-Auth-Token': TOKEN, 'Content-Type': 'application/json'}
)
try:
    with urllib.request.urlopen(req, timeout=20) as resp:
        print(resp.read().decode())
except urllib.error.HTTPError as e:
    print(e.read().decode())
    raise
