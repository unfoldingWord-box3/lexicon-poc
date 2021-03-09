'''
To use a different database backend to store the data, 
set an ENV variable that points to the database of your choice

For instance:

    DATABASE_URL=postgres://username:password@localhost/dbname

where you provide the username, password, and database name as you
defined them in your database.

If no valid DATABASE_URL env variable is found, an sqlite database will be used
as a fallback. 
'''

import os
from sqlalchemy import create_engine

try:
    config = os.environ['DATABASE_URL']  #TODO change and check if postgresql and postgres both work
    engine = create_engine(config, echo=False)
    # check if you can connect
    with engine.connect() as connection:
        pass
except:
    print('USING SQLITE')
    print()
    engine = create_engine('sqlite:///../project_lexicon/alignment.db', echo=False)