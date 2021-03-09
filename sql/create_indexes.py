from engine import engine

print('Testing the connection:')
print(engine.execute("SELECT * FROM target LIMIT 10").fetchall())
print()

try:
    name = 'ix_source_id'
    engine.execute('''CREATE INDEX ix_source_id ON source ("id")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_source_strongs'
    engine.execute('''CREATE INDEX ix_source_strongs ON source ("strongs")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_source_lemma'
    engine.execute('''CREATE INDEX ix_source_lemma ON source ("lemma")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_source_strongs_no_prefix'
    engine.execute('''CREATE INDEX ix_source_strongs_no_prefix ON source ("strongs_no_prefix")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_source_token'
    engine.execute('''CREATE INDEX ix_source_token ON source ("token")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_source_ref'
    engine.execute('''CREATE INDEX ix_source_ref ON source ("book", "chapter", "verse")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))


try:
    name = 'ix_target_id'
    engine.execute('''CREATE INDEX ix_target_id ON target ("id")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_target_token'
    engine.execute('''CREATE INDEX ix_target_token ON target ("target_token")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_target_ref'
    engine.execute('''CREATE INDEX ix_target_ref ON target ("book", "chapter", "verse")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))


try:
    name = 'ix_alignment_index'
    engine.execute('''CREATE INDEX ix_alignment_index ON alignment ("index")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_alignment_id'
    engine.execute('''CREATE INDEX ix_alignment_id ON alignment ("id")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_alignment_target'
    engine.execute('''CREATE INDEX ix_alignment_target ON alignment ("target_id")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_alignment_source'
    engine.execute('''CREATE INDEX ix_alignment_source ON alignment ("source_id")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_alignment_source_and_target'
    engine.execute('''CREATE INDEX ix_alignment_source_and_target ON alignment ("source_id", "target_id")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))


try:
    name = 'ix_strongs_m2m_number'
    engine.execute('''CREATE INDEX ix_strongs_m2m_number ON strongs_m2m ("number")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))


try:
    name = 'ix_notes_noteID'
    engine.execute('''CREATE INDEX ix_notes_noteID ON notes ("noteID")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_notes_supportreference'
    engine.execute('''CREATE INDEX ix_notes_supportreference ON notes ("supportReference")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_notes_source'
    engine.execute('''CREATE INDEX ix_notes_source ON notes ("source")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_notes_ref'
    engine.execute('''CREATE INDEX ix_notes_ref ON notes ("book", "chapter", "verse")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))


try:
    name = 'ix_notesM2M_notes'
    engine.execute('''CREATE INDEX ix_notesM2M_notes ON NotesM2M ("index")''')  #TODO make naming consistent
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_notesM2M_source'
    engine.execute('''CREATE INDEX ix_notesM2M_source ON NotesM2M ("source")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))


try:
    name = 'ix_question'
    engine.execute('''CREATE INDEX ix_question ON question ("index")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_question_ref'
    engine.execute('''CREATE INDEX ix_question_ref ON question ("book", "chapter", "verse")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))



try:
    name = 'ix_lexicon_strongs'
    engine.execute('''CREATE INDEX ix_lexicon_strongs ON lexicon ("strongs")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_lexicon_lemma'
    engine.execute('''CREATE INDEX ix_lexicon_lemma ON lexicon ("lemma")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))


try:
    name = 'ix_words_id'
    engine.execute('''CREATE INDEX ix_words_id ON tw ("id")''')  #TODO make naming consistent with models
except:
    print('The index {} might already exist or failed'.format(name.upper()))


try:
    name = 'ix_glosses_index'
    engine.execute('''CREATE INDEX ix_glosses_index ON glosses ("index")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_glosses_strongs'
    engine.execute('''CREATE INDEX ix_glosses_strongs ON glosses ("strongs")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))
try:
    name = 'ix_glosses_lemma'
    engine.execute('''CREATE INDEX ix_glosses_lemma ON glosses ("lemma")''')
except:
    print('The index {} might already exist or failed'.format(name.upper()))