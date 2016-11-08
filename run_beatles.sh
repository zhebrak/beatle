docker run --net=host -it zhebrak/beatle --conf="/etc/beatle/default.conf" --node="127.0.0.1:8000" --cluster="127.0.0.1:8000 127.0.0.1:8001 127.0.0.1:8002"
docker run --net=host -it zhebrak/beatle --conf="/etc/beatle/default.conf" --node="127.0.0.1:8001" --cluster="127.0.0.1:8000 127.0.0.1:8001 127.0.0.1:8002"
docker run --net=host -it zhebrak/beatle --conf="/etc/beatle/default.conf" --node="127.0.0.1:8002" --cluster="127.0.0.1:8000 127.0.0.1:8001 127.0.0.1:8002"
