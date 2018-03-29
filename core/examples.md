# register new node

- curl -X POST http://localhost:5000/node-register

- POST data 

```s
{
	"node_address": "192.168.55.12",
	"node_port": 5000,
	"is_confirm": 1
}
```

# submit transaction

- POST 

```
{
	"author": "Sa Pham Dang",
	"title": "Up and running Kubernetes",
	"doc_hash": "9hkE44yyc8AkvvW0RVM8m48=",
	"s3_url": "https://s3.aws.com/9hkE44yyc8AkvvW0RVM8m48="
}
```
# query all pending transactions

# query confirm node