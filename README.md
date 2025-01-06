# badrat

We all know LLMs are 100% reliable and can never be wrong, so let's have it check if an HTTP request is potentially malicious or not.

## Development

Make sure `GROQ_API_KEY` is set, and then:

```sh
# In one shell
make fastapi-dev

# In another shell
make baml-dev
```

Now you can send requests to check how malicious they are:
```sh
curl -s http://localhost:8000/slim?path=../../ | jq
# {
#   "possibly_dangerous": true
# }

curl -s http://localhost:8000/complete?path=../../ | jq
# {
#   "possibly_dangerous": true,
#   "dangerous_parameters": [
#     {
#       "parameter_path": "url.query.path",
#       "value": "../../"
#     }
#   ]
# }
```
