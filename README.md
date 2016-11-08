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
# pure
python3 beatle.py --conf="/etc/beatle/default.conf" --node="8000" --cluster="8000 8001 8002" &
...

# with docker (not working)
docker run --net=host -it zhebrak/beatle --conf="/etc/beatle/default.conf" --node="8000" --cluster="8000 8001 8002"
...
```
