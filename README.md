# Python Blockchain

### Commands
To create a new transaction to a block `POST`
```
/transactions/new 
```
To tell our server to mine a new block `GET`
```
/mine
```
To return the full Blockchain `GET`
```
/chain
```

#### Nodes
To accept a list of new nodes in the form of URLs
```
/nodes/register
```
Example for body `POST`:
```
{
	"nodes": "192.168.15.69:5001"
}
```
To implement our Consensus Algorithm, which resolves any conflicts—to ensure a node has the correct chain. `GET`:
```
/nodes/resolve
```

---
### Requests
This is what the request for a transaction will look like. It’s what the user sends to the server:
```
{
 "sender": "my address",
 "recipient": "someone else's address",
 "amount": 5
}
```

---
### Database
Necessary setup a postgres database, with `db.ini` with credentials:
```
[postgresql]
host=localhost
database=db_name
user=example_user
password=example_pass
```

---
### Docker
Necessary build the personalized images from `Dockerfile`
```
docker build -t "blockchain:v3" .
docker build -t "block_nginx" nginx/Dockerfile
```
