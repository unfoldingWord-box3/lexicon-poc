# Storage

+ fix: ult does not correctly link to source // error whereby target words are all the same
- fix: prefix to suffix/trailer
- improve store the root, also store parsing
- a data creation script
- store strongs annotation count
? nr_of_target_words, nr_of_source_words
- k-s
- maqqef and prefixes
- store the count for strongs
+ give alignment unique id's
+ activate the admin

# Resources

+ insert translationNotes
- pull translationNotes automatically as well
- insert current lexicon
+ insert translation questions
- insert BDB
- link strongs to source text
- link tw to strongs
- link source to tw? or already done?
- create a Sense model?

# Prototype
- Delete the data/alignment folder
+ django debug toolbar
? Handle languages other than English
? if this were not a poc: use managed django models, rename model fields
? how do you keep track of gaps in aligments, when you remove and/or update an aligment (will it not have a new id?)
? how do you calculate gaps when aligments are in a separate table?
? how do you store the alignment: link every word, or simply link all items to the first? 