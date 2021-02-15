Source.objects.filter(strongs_counts__gte=100)
Source.objects.filter(strongs_count__gte=100)
Source.objects.filter(strongs_count__gte=100).count()
Source.objects.filter(strongs_count__gte=100).count()
Source.objects.filter(strongs_count__gte=100).count()
Source.objects.filter(strongs_count__gte=100)
Source.objects.filter(strongs_count__gte=10).count()
Source.objects.filter(strongs_count__gte=1000).count()
Source.objects.filter(strongs_count__gte=100).count()
Source.objects.filter(strongs_count__gte=100)
sources = Source.objects.filter(strongs_count__gte=100)
sources.values('strongs_no_prefix')
Source.objects.filter(strongs_no_prefix='H0430')
Source.objects.filter(strongs_no_prefix='H0430').count()
strongs = 'H0430'
sources.values('id')
sources.values_list('id')
[itm[0] for itm in sources.values_list('id')]
len([itm[0] for itm in sources.values_list('id')])
sources.count()
case = Source.objects.filter(strongs_no_prefix='H0430')
len([itm[0] for itm in case.values_list('id')])
[itm[0] for itm in case.values_list('id')]
case_ids = [itm[0] for itm in case.values_list('id')]
case_ids
full_ids = []
for id in case_ids:
    for i in range(-5,5):
        full_ids.append(id-i)
len(full_ids)
len(case)
full_ids[:20]
case_ids[:20]
case_ids[:2]
full_ids[:20]
full_ids = []
for id in case_ids:
    for i in range(-5,5):
        full_ids.append(id+i)
case_ids[:2]
full_ids[:20]
full_ids[:25]
full_ids = list(set(full_ids))
len(full_ids)
Source.objects.filter(id__isin=full_ids)
Source.objects.filter(id__in=full_ids)
%time Source.objects.filter(id__in=full_ids)
%time Source.objects.filter(id__in=full_ids)
%time Source.objects.filter(id__in=full_ids)
%time Source.objects.filter(id__in=full_ids)
expanded_case = Source.objects.filter(id__in=full_ids)
expanded_case.count()
len(full_ids)
%time Source.objects.filter(id__in=full_ids).values('id', 'token')
%time Source.objects.filter(id__in=full_ids).values_st('id', 'token')
%time Source.objects.filter(id__in=full_ids).values_list('id', 'token')
dict(Source.objects.filter(id__in=full_ids).values_list('id', 'token'))
source_tokens = dict(Source.objects.filter(id__in=full_ids).values_list('id', 'token'))
case_ids[0]
source_tokens[2]
source_tokens[2]
source_tokens[0:2+4]
source_tokens[0]
''.join([source_tokens[i] for i in range(2-5, 2+5)])
''.join([source_tokens[i] for i in range(2-2, 2+5)])
print(''.join([source_tokens[i] for i in range(2-2, 2+5)]))
case
case.values('alignment_set__target__id')
case.values('alignment__target__id')
case.values('alignment__target_id')
%time case.values('alignment__target_id')
%time case.values('alignment__target')
%time case.values('alignment__target__id')
%time case.values('alignment')
%time case.values('alignment_set')
%time case.values('alignment')
case[0].alignment
x = case[0]
c
x
x.alignment_set
x.alignment_set.all()
%time case.values('alignment__target__id')
%time case.values('alignment__target__id')[-100:]
%time case.values('alignment__target__id')[50:100]
%time case.values('alignment__target__id')[500:600]
%time case.values('alignment__target')[500:600]
%time case.values('alignment_set__target')[500:600]
x = case[1000]
x.alignment_set
x.alignment_set.all()
case[1001].alignment_set.all()
case[2001].alignment_set.all()
case[3001].alignment_set.all()
case[1501].alignment_set.all()
case[1502].alignment_set.all()
case[1503].alignment_set.all()
case[1603].alignment_set.all()
case[103].alignment_set.all()
case[1703].alignment_set.all()
x = case[1703]
x.values('alignment')
case[1703:1704].values('alignment')
case[1703:1705].values('alignment')
case[1703:1705]
source
sources
sources.values('alignment')
sources.values('alignment__target')
sources.filter(alignment__target__isnull=False);values('alignment__target')
sources.filter(alignment__target__isnull=False).values('alignment__target')
sources.filter(alignment__target__isnull=False).values('alignment__target', 'alignment_id')
sources.filter(alignment__target__isnull=False).values('alignment__target', 'alignment__id')
sources.filter(alignment__target__isnull=False).values('alignment__target', 'alignment__index')
sources.filter(alignment__target__isnull=False).values('alignment__target', 'alignment__alg_id')
sources.filter(alignment__target__isnull=False).values('alignment__alg_id')
alg_ids = sources.filter(alignment__target__isnull=False).values('alignment__alg_id')
alg_ids.count()
alg_ids.count()
sources.count()


Source.objects.filter(strongs_no_prefix='H0430', alignment__target__isnull=False).values('id', 'token', 'alignment__alg_id', 'alignment__target__target_token', 'alignment__target__id')


print(Source.objects.filter(strongs_no_prefix='H0430', alignment__target__isnull=False).values('id', 'token', 'alignment__alg_id', 'alignment__target__target_token', 'alignment__target__id', 'alignment__source').query)
''' SELECT "source"."id", "source"."token", "alignment"."alg_id", "target"."target_token", "alignment"."target_id", "alignment"."source_id" 
    FROM "source" 
    INNER JOIN "alignment" ON ("source"."id" = "alignment"."source_id") 
    INNER JOIN "target" ON ("alignment"."target_id" = "target"."id") 
    WHERE ("alignment"."target_id" IS NOT NULL AND "source"."strongs_no_prefix" = H0430)
'''

Alignment.objects.filter(source__strongs_no_prefix='H0430').count()

df = pd.DataFrame(Alignment.objects.filter(source__strongs_no_prefix='H0430').values('id', 'alg_id', 'source', 'source__token', 'source__morph', 'target', 'target__target_token', 'roots', 'source_blocks', 'target_blocks'))


# find other words that are part of the same alignments, but that are not the actual word 
Alignment.objects.filter(alg_id__in=df.alg_id.astype(str).tolist()).exclude(source__strongs_no_prefix='H0430').values('source__token')


result = Source.objects.filter(strongs_no_prefix='H0430', alignment__target__isnull=False).values('id', 'token', 'alignment__alg_id', 'alignment__target__target_token', 'alignment__target__id', 'alignment__source')
source_ids = [itm['alignment__source'] for itm in result]
target_ids = [itm['alignment__target__id'] for itm in result]



from itertools import groupby
import copy

number = 'H0430'
result = Alignment.objects.filter(source__strongs_no_prefix=number).values('id', 'alg_id', 'source', 'source__token', 'source__morph', 'target', 'target__target_token', 'roots', 'source_blocks', 'target_blocks')
source_ids = [itm['source'] for itm in result]
target_ids = [itm['target'] for itm in result]


def expand_window(li, window=5):
    output = []
    for itm in li:
        for i in range(-window,window):
            output.append(itm+i)
    return set(output)

source_ids_w_window = expand_window(source_ids)
target_ids_w_window = expand_window(target_ids)


source_window_tokens = dict(Source.objects.filter(id__in=source_ids_w_window).values_list('id', 'token'))
target_window_tokens = dict(Target.objects.filter(id__in=target_ids_w_window).values_list('id', 'target_token'))


def build_concordance(token_ids, window_tokens, window=5):
    concordance = []
    for i in range(-window, window+1):
        token_id = min(token_ids)
        try:
            idx = token_id+i
            token = window_tokens[idx]
            if idx in token_ids:
                token = '<highlight>' + token + '</highlight>'
            if token:  # some cases are None
                concordance.append(token)
        except:
            continue
    return concordance

# goal: alg_id, source_id, source_blocks, [target_id1, target_id2], [target_blocks1, target_blocks2], source_concordance, target_concordance
# this assumes only a single source_id, even if multiple source words are part of the alignment
condensed_result = []

for idx,grp in groupby(result, lambda datum: datum['alg_id']):
    output = {}
    output['alg_id'] = idx

    for idx,itm in enumerate(grp):
        if idx == 0:
            # for the first item we do some extra's
            output['id'] = itm['id']
            output['alg_id'] = itm['alg_id']
            output['source'] = [itm['source']]  # list because build_concordance needs a list
            output['source_blocks'] = itm['source_blocks']
            output['source__morph'] = itm['source__morph']
            output['target'] = [itm['target']]
            output['target__target_token'] = [itm['target__target_token']]
            output['target_blocks'] = itm['target_blocks']
            output['roots'] = itm['roots']
        else:
            output['target'] = output['target'] + [itm['target']]
            output['target__target_token'] = output['target__target_token'] + [itm['target__target_token']]
    condensed_result.append(output)

# now add concordances
# in the concordance do highlighting

algs_w_concordances = []
for itm in condensed_result:
    itm['source_concordance'] = ''.join(build_concordance(itm['source'], source_window_tokens))
    itm['target_concordance'] = ''.join(build_concordance(itm['target'], target_window_tokens))
    algs_w_concordances.append(itm)


df = pd.DataFrame(algs_w_concordances)
df.to_html()


# goal: now group per sense/target_blocks
senses = groupby(algs_w_concordances, lambda datum: datum['target_blocks'])




condensed_result = []
for idx,grp in groupby(result, lambda datum: datum['alg_id']):
    for itm in grp:
        try:
            assert output
            output['target'] = output['target'].append(itm['target'])
            output['target__target_token'] = output['target__target_token'].append(itm['target__target_token'])
        except: 
            first_iteration = itm
            output = copy.deepcopy(first_iteration)
            output['target'] = [itm['target']]
            output['target__target_token'] = [itm['target__target_token']]
       
    condensed_result.append(output)