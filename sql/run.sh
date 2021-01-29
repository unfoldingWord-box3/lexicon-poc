python allusfm2sql.py
python target2sql.py
python notes2sql.py
python words2sql.py
python lexicon2sql.py
python ../project_lexicon/add_roots.py
python ../project_lexicon/manage.py migrate
python ../project_lexicon/manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('demo', 'demo@somerandomemailthing.com', 'demo')"