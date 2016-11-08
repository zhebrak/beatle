# beatle

Fault-tolerant HTTP request sender with cron schedule.

#### Configuration

```
[<project_name>]
URL: <beatle http endpoint>
KEY: <secret key>
```

[Django client](https://github.com/zhebrak/django-beatle/)


#### Start
```bash
docker run -d beatle --conf="/etc/beatle/default.conf" --node="8000" --cluster="8000 8001 8002"
docker run -d beatle --conf="/etc/beatle/default.conf" --node="8001" --cluster="8000 8001 8002"
docker run -d beatle --conf="/etc/beatle/default.conf" --node="8002" --cluster="8000 8001 8002"
```
