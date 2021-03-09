# Run this file with a DATABASE_URL environment variable
# or it will default to a local SQLite database
# read the engine.py file for more detail
#
#     DATABASE_URL=postgres://user:password@localhost/databasename ./run.py

python allusfm2sql.py
python text2sql.py
python notes2sql.py
python words2sql.py
python lexicon2sql.py
python glosses2sql.py
python questions2sql.py
python ../project_lexicon/manage.py migrate
python create_indexes.py
# This command is last so it can fail if the db already is up and running
python ../project_lexicon/manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('demo', 'demo@somerandomemailthing.com', 'demo')"