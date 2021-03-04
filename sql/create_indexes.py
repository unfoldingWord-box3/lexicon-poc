from sqlalchemy import create_engine
engine = create_engine('sqlite:///../project_lexicon/alignment.db', echo=False)

print(engine.execute("SELECT * FROM target LIMIT 10").fetchall())

try:
    engine.execute('''CREATE INDEX ix_alignment_index ON alignment ("index")''')
except:
    print('This index might already exist')
try:
    engine.execute('''CREATE INDEX ix_source_id ON source ("id")''')
except:
    print('This index might already exist')
try:
    engine.execute('''CREATE INDEX ix_source_strongs ON source ("strongs")''')
except:
    print('This index might already exist')
try:
    engine.execute('''CREATE INDEX ix_source_lemma ON source ("lemma")''')
except:
    print('This index might already exist')
try:
    engine.execute('''CREATE INDEX ix_source_strongs_no_prefix ON source ("strongs_no_prefix")''')
except:
    print('This index might already exist')
try:
    engine.execute('''CREATE INDEX ix_source_token ON source ("token")''')
except:
    print('This index might already exist')
try:
    engine.execute('''CREATE INDEX ix_source_ref ON source ("book", "chapter", "verse")''')
except:
    print('This index might already exist')


try:
    engine.execute('''CREATE INDEX ix_target_id ON target ("id")''')
except:
    print('This index might already exist')
try:
    engine.execute('''CREATE INDEX ix_target_token ON target ("target_token")''')
except:
    print('This index might already exist')
try:
    engine.execute('''CREATE INDEX ix_target_ref ON target ("book", "chapter", "verse")''')
except:
    print('This index might already exist')


try:
    engine.execute('''CREATE INDEX ix_alignment_id ON alignment ("id")''')
except:
    print('This index might already exist')
try:
    engine.execute('''CREATE INDEX ix_alignment_target ON alignment ("target_id")''')
except:
    print('This index might already exist')
try:
    engine.execute('''CREATE INDEX ix_alignment_source ON alignment ("source_id")''')
except:
    print('This index might already exist')
try:
    engine.execute('''CREATE INDEX ix_source_and_target ON target ("source_id", "target_id")''')
except:
    print('This index might already exist')



try:
    engine.execute('''CREATE INDEX ix_strongs_m2m_number ON strongs_m2m ("number")''')
except:
    print('This index might already exist')


try:
    engine.execute('''CREATE INDEX ix_notes_noteID ON notes ("noteID")''')
except:
    print('This index might already exist')
try:
    engine.execute('''CREATE INDEX ix_notesM2M_notes ON notesM2M ("notes_id")''')
except:
    print('This index might already exist')
try:
    engine.execute('''CREATE INDEX ix_notesM2M_source ON notesM2M ("source_id")''')
except:
    print('This index might already exist')
