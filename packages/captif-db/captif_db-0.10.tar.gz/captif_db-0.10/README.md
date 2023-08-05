
# captif-db

Object relational mapping for the CAPTIF database.

These are low-level methods.

### Initialise database and generate a session object:

```
from captif_db.db import DbSession
DbSession.global_init()
session = DbSession.factory()
```

### Import and use models:

```
from captif_db.db.models import Project
projects = session.query(Project).all()
```
