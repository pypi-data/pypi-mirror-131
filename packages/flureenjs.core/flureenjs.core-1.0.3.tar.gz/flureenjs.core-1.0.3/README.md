## Hello from Fluree jsii for Python

```python
from flureenjs.core import FlureeConn
import pprint

pp = pprint.PrettyPrinter(indent=4)

fluree_conn = FlureeConn(url="http://localhost:8090")


ledger_name = "test111100/test200006"

fluree_conn.new_ledger(ledger_name)

results = fluree_conn.ledger_list()
pp.pprint(results)

query = {"select": ["*"], "from": "_user"}
results = fluree_conn.query(ledger_name, query)
pp.pprint(results)


transaction = [
    {
        "_id": "_user",
        "username": "testyTest",
    }
]

transaction_results = fluree_conn.transact(ledger_name, transaction)
pp.pprint(transaction_results)

query = {"select": ["*"], "from": "_user"}
results = fluree_conn.query(ledger_name, query)
pp.pprint(results)

```
