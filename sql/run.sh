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