## Elastic GROK

```JSON
FROM logs-*
| EVAL match = GROK(message, '.*"logOnlySecurityData":\s*{.*"behavoirs":\s*{.*"(?<key>[^"]+)":\s*"(?<value>POSITIVE)".*}.*}.*')
| WHERE value == "POSITIVE"
| KEEP key, value
| LIMIT 10
```