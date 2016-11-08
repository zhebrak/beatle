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
python3 beatle.py --conf="/etc/beatle/default.conf" --node="8001" --cluster="8000 8001 8002" &
python3 beatle.py --conf="/etc/beatle/default.conf" --node="8002" --cluster="8000 8001 8002" &

# with docker
docker run --net=host -v /etc/beatle:/conf -id zhebrak/beatle --conf="/conf/default.conf" --node="8000" --cluster="8000 8001 8002"
docker run --net=host -v /etc/beatle:/conf -id zhebrak/beatle --conf="/conf/default.conf" --node="8001" --cluster="8000 8001 8002"
docker run --net=host -v /etc/beatle:/conf -id zhebrak/beatle --conf="/conf/default.conf" --node="8002" --cluster="8000 8001 8002"

```
