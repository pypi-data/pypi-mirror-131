![PyPI - Python Version](https://img.shields.io/pypi/pyversions/formal-sqlcommenter)

# Formal sqlcommenter

Formal sqlcommenter is a plugin that enables your ORMs to augment SQL statement before execution, with a comment containing the end-user id of a request.
Sqlcommenter is typically useful for back-office application that needs to implement role access management.

 * [Psycopg2](#psycopg2)

## Local Install

```shell
pip3 install --user formal-sqlcommenter
```

## Usage

### Psycopg2

Use the provided cursor factory to generate database cursors. All queries executed with such cursors will have the SQL comment prepended to them.

```python
import psycopg2
from formal.sqlcommenter.psycopg2.extension import CommenterCursorFactory

cursor_factory = CommenterCursorFactory()
conn = psycopg2.connect(..., cursor_factory=cursor_factory)
cursor = conn.cursor()
cursor.execute('SELECT * from ...', '1234') # comment will be added before execution
```

which will produce a backend log such as when viewed on Postgresql
```shell
2019-05-28 02:33:25.287 PDT [57302] LOG:  statement: SELECT * FROM
polls_question *--formal_role_id: 1234 */
```

