# badrat

We all know LLMs are 100% reliable and can never be wrong, so let's have it check if an HTTP request is potentially malicious or not.

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

curl -s http://localhost:8000/complete?path=../../ -H "Authorization: Bearer Robert'); DROP TABLE students; --" | jq
# {
#   "possibly_dangerous": true,
#   "dangerous_parameters": [
#     {
#       "parameter_path": "headers.authorization",
#       "value": "Bearer Robert'); DROP TABLE students; --"
#     },
#     {
#       "parameter_path": "url.query.path",
#       "value": "../../"
#     }
#   ]
# }
```
