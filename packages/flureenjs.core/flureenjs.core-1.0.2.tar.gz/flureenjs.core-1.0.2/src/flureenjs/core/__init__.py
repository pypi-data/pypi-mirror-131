'''
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
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *


class FlureeConn(metaclass=jsii.JSIIMeta, jsii_type="fluree-jsii.FlureeConn"):
    '''
    :stability: experimental
    '''

    def __init__(self, *, url: builtins.str) -> None:
        '''
        :param url: 

        :stability: experimental
        '''
        props = FlureeProps(url=url)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="connect")
    def connect(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.ainvoke(self, "connect", []))

    @jsii.member(jsii_name="getDb")
    def get_db(self, ledger: builtins.str) -> typing.Any:
        '''
        :param ledger: -

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.ainvoke(self, "getDb", [ledger]))

    @jsii.member(jsii_name="ledgerList")
    def ledger_list(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.ainvoke(self, "ledgerList", []))

    @jsii.member(jsii_name="newLedger")
    def new_ledger(self, name: builtins.str) -> typing.Any:
        '''
        :param name: -

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.ainvoke(self, "newLedger", [name]))

    @jsii.member(jsii_name="query")
    def query(self, ledger: builtins.str, query: typing.Any) -> typing.Any:
        '''
        :param ledger: -
        :param query: -

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.ainvoke(self, "query", [ledger, query]))

    @jsii.member(jsii_name="transact")
    def transact(
        self,
        ledger: builtins.str,
        transaction: typing.Sequence[typing.Any],
    ) -> typing.Any:
        '''
        :param ledger: -
        :param transaction: -

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.ainvoke(self, "transact", [ledger, transaction]))

    @jsii.member(jsii_name="waitUntilReady")
    def wait_until_ready(self, name: builtins.str) -> typing.Any:
        '''
        :param name: -

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.ainvoke(self, "waitUntilReady", [name]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="conn")
    def conn(self) -> typing.Mapping[typing.Any, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.get(self, "conn"))

    @conn.setter
    def conn(self, value: typing.Mapping[typing.Any, typing.Any]) -> None:
        jsii.set(self, "conn", value)


@jsii.data_type(
    jsii_type="fluree-jsii.FlureeProps",
    jsii_struct_bases=[],
    name_mapping={"url": "url"},
)
class FlureeProps:
    def __init__(self, *, url: builtins.str) -> None:
        '''
        :param url: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "url": url,
        }

    @builtins.property
    def url(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FlureeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "FlureeConn",
    "FlureeProps",
]

publication.publish()
