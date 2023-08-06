# Overview

This package is a very simple client for accessing a GraphQL knowledge graph as a HTTP GET request wrapper.

# Usage

Create a client:

```
from pykg import KGClient
kg = KGClient(
  host = 'localhost',
  port = 6543,
  user = 'user',
  password = 'password',
  domain = 'my_kg')
```

Perform a string based query:
```
kg.query("{ assets { name } }")
```

Perform a query, but suppress output:
```
result = kg.query("{ assets { name } }", pretty_print=False)
print(len(result['assets']))
```