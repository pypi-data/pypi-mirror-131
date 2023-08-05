## Hello from Fluree jsii for Python

```python
from flureenjs.core import FlureeConn
import pprint

pp = pprint.PrettyPrinter(indent=4)

fluree_conn = FlureeConn(url="http://localhost:8090")
query = {"select": ["*"], "from": "_user"}
results = fluree_conn.query(query)
pp.pprint(results)

transaction = [
    {
        "_id": "_user",
        "username": "jonathan",
    }
]

transaction_results = fluree_conn.transact(transaction, "main/test")
pp.pprint(transaction_results)

query = {"select": ["*"], "from": "_user"}
results = fluree_conn.query(query)
pp.pprint(results)
```
