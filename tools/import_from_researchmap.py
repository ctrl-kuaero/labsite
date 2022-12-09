import requests,json,sys,os, time
import toml
from urllib.parse import urlparse
from pprint import pprint
import re

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

members = ['maruta','fujimoto_kenji']

inlab = {
    'maruta': {
        'since':'2017-06-01',
        'until':'9999-99-99'
    },
    'fujimoto_kenji': {
        'since':'2012-10-01',
        'until':'9999-99-99'
    },
}

#download json files from researchmap
url = "https://api.researchmap.jp/"
itemslist = ["published_papers","research_projects","misc","presentations","books_etc"]
jsonfiles={}
for name in members:
  jsonfiles[name]={}
  for it in itemslist:
    r1 = requests.get(url+name+'/'+it)
    jsonfiles[name][it]=json.loads(r1.text)


items = {}
overlap = 0
try:
    for member in jsonfiles:
        for category in jsonfiles[member]:
            for i in jsonfiles[member][category]['items']:
                if 'publication_date' in i:
                    if inlab[member]['since'] < i['publication_date'] and inlab[member]['until'] > i['publication_date']:
                        i['inlab'] = True
                    else:
                        i['inlab'] = False

                if i.get('identifiers') != None:
                    item_id = json.dumps(i.get('identifiers'))
                else:
                    if i.get('paper_title') != None:                   
                        item_id = json.dumps(i.get('paper_title'))
                    elif i.get('research_project_title') != None:
                        item_id = json.dumps(i.get('research_project_title'))
                    elif i.get('presentation_title') != None:
                        item_id = json.dumps(i.get('presentation_title'))
                    elif i.get('book_title') != None:
                        item_id = json.dumps(i.get('book_title'))
                    else:
                        raise Exception("Can't determine ID")
                    item_id += i.get('publication_date') 
                if item_id in items:
                    if i.get('inlab',False):
                        items[item_id]['inlab'] = True
                    overlap += 1
                    #pprint(item_id)
                    #pprint({'old': items[item_id], 'new': i})
                items[item_id] = i
                
except Exception as e:
    pprint(i)
    raise(e)
print('Found {} overlaps.'.format(overlap))


# 変換

records = []
for i in items.values():
    record = {}
    try:
        if i.get('@type') == 'misc':
            record['ja_booktitle'] = i['publication_name'].get('ja')
            record['en_booktitle'] = i['publication_name'].get('en')
            record['publication_date'] = i['publication_date'].replace('-','')
            record['publication_date'] = record['publication_date'] + "0"*(8 - len(record['publication_date']))
            if i.get('misc_type') == 'summary_national_conference':
                record['type'] = 'domestic_conference'
            elif i.get('misc_type') == 'introduction_scientific_journal':
                record['type'] = 'explanation_journal'
            elif i.get('misc_type') == 'summary_international_conference':
                record['type'] = 'summary_international_conference'
            elif i.get('misc_type') == 'technical_report':
                record['type'] = 'technical_report'
            elif i.get('misc_type') == 'meeting_report':
                record['type'] = 'meeting_report'
            elif i.get('misc_type') == 'others':
                record['type'] = 'others'
            else:
                pprint(i)
                raise Exception('can not identify type (unknown misc_type)')
        elif i.get('@type') == 'published_papers':
            record['publication_date'] = i['publication_date'].replace('-','')
            record['publication_date'] = record['publication_date'] + "0"*(8 - len(record['publication_date']))
            record['ja_booktitle'] = i['publication_name'].get('ja')
            record['en_booktitle'] = i['publication_name'].get('en')
            if i.get('published_paper_type') == 'scientific_journal':
                record['type'] = 'journal'
            elif i.get('published_paper_type') == 'international_conference_proceedings':
                record['type'] = 'international_conference'
            elif i.get('published_paper_type') == 'summary_international_conference':
                record['type'] = 'summary_international_conference'
            elif i.get('published_paper_type') == 'symposium':
                record['type'] = 'papers_symposium'
            elif i.get('published_paper_type') == 'in_book':
                record['type'] = 'in_book'
            else:
                pprint(i)
                raise Exception('can not identify type(unknown_published_paper_type)')
        elif i.get('@type') == 'presentations':
            # 依頼講演など．とりあえず無視
            continue
        elif i.get('@type') == 'books_etc':
            record['publication_date'] = i['publication_date'].replace('-','')
            record['publication_date'] = record['publication_date'] + "0"*(8 - len(record['publication_date']))        
            record['type'] = 'book'
            record['book_owner_role'] = i['book_owner_role']
            if 'book_owner_range' in i:
                record['en_book_owner_range'] = i['book_owner_range'].get('en', i['book_owner_range'].get('ja'))
                record['ja_book_owner_range'] = i['book_owner_range'].get('ja', i['book_owner_range'].get('en'))
        elif i.get('@type') == 'research_projects':
            # 科研費など．とりあえず無視
            continue     
        else:
            raise Exception('can not identify @type')

        if 'jpn' in i.get('languages',[]):
            record['lang'] = 'ja'

        record['volume'] = i.get('volume')
        record['number'] = i.get('number')
        record['page_begin'] = i.get('starting_page')
        record['page_end'] = i.get('ending_page')
        record['reviewed'] = i.get('referee')
        record['invited'] = i.get('invited')
        
        if 'publisher' in i:
            record['en_publisher'] = i['publisher'].get('en', i['publisher'].get('ja'))
            record['ja_publisher'] = i['publisher'].get('ja', i['publisher'].get('en'))

        # タイトル
        if 'paper_title' in i:
            record['en_title'] = i['paper_title'].get('en')
            record['ja_title'] = i['paper_title'].get('ja')
        elif 'book_title' in i:
            record['en_title'] = i['book_title'].get('en')
            record['ja_title'] = i['book_title'].get('ja')
        else:
            raise Exception('can not identify title')

        if record['ja_title'] == None and record['en_title'] == None:
            raise Exception('can not identify title')
        if record['ja_title'] == None:
            record['ja_title'] = record['en_title']
        if record['en_title'] == None:
            record['en_title'] = record['ja_title']
            
        # 著者
        en_authors_list = i['authors'].get('en',[])
        en_authors = [a['name'] for a in en_authors_list]
        record['en_author'] = ', '.join(en_authors)

        ja_authors_list = i['authors'].get('ja',[])
        ja_authors = [a['name'] for a in ja_authors_list]
        if len(ja_authors) == 0:
            ja_authors = en_authors
        record['ja_author'] = ', '.join(ja_authors)
        
        ids = {}

        for idtype,idval in i.get('identifiers',{}).items():
            idstr = idval[0]+""
            if idtype == "doi":
                ids[idtype] = {
                    'label': "DOI",
                    'id': idstr,
                    "url": "https://doi.org/"+idstr
                }
            elif idtype == "cinii_na_id":
                ids[idtype] = {
                    'label': "CiNii",
                    'id': idstr,
                    "url": "https://ci.nii.ac.jp/naid/"+idstr
                }
            elif idtype == "cinii_nc_id":
                ids[idtype] = {
                    'label': "CiNii",
                    'id': idstr,
                    "url": "https://ci.nii.ac.jp/ncid/"+idstr
                }
            elif idtype == "cinii_cr_id":
                ids[idtype] = {
                    'label': "CiNii",
                    'id': idstr,
                    "url": "https://cir.nii.ac.jp/crid/"+idstr
                }                
            elif idtype == "j_global_id":
                ids[idtype] = {
                    'label': "J-GLOBAL ID",
                    'id': idstr,
                    "url": "http://jglobal.jst.go.jp/detail?JGLOBAL_ID="+idstr
                }
            elif idtype == "issn":
                ids[idtype] = {
                    'label': "ISSN",
                    'id': idstr,
                }
            elif idtype == "isbn":
                ids[idtype] = {
                    'label': "ISBN",
                    'id': idstr,
                }
            elif idtype == "e_issn":
                ids[idtype] = {
                    'label': "e-ISSN",
                    'id': idstr,
                }
            elif idtype == "dblp_id":
                ids[idtype] = {
                    'label': "DBLP",
                    'id': idstr,
                    'url': 'https://dblp.uni-trier.de/rec/'+idstr
                }    
            elif idtype == "arxiv_id":
                ids[idtype] = {
                    'label': "arXiv",
                    'id': idstr.split(':')[1],
                    "url": "http://arxiv.org/abs/"+idstr
                }                  
            elif idtype == "scopus_id":
                # Scopus ID はとりあえず無視（文献のIDに対応するページが不明）
                continue
            elif idtype == "wos_id":
                # Web of Science ID はとりあえず無視（文献のIDに対応するページが不明）
                continue
            else:
                raise Exception('Unknown id type: '+idtype)      

        for info in i.get('see_also',[]):
            id_parsed = urlparse(info['@id'])
            fragments = id_parsed.path.split('/')
            if info['label'] == 'arxiv':
                ids['arxiv_id'] = {
                    'label': "arXiv",
                    'id': id_parsed.path.split(':')[1],
                    "url": info['@id']
                }  
            elif info['label'] == 'DBLP':
                ids['DBLP'] = {
                    'label': "DBLP",
                    'id': '/'.join(fragments[2:]),
                    "url": info['@id']
                } 
            elif id_parsed.hostname == 'doi.org':
                if 'doi' in ids:
                    continue
                else:
                    ids['doi'] = {
                        'label': "DOI",
                        'id': '/'.join(fragments[1:]),
                        "url": info['@id']
                    } 
 
            elif info['label'] == 'web_of_science':
                # Web of Science ID はとりあえず無視
                continue
            elif id_parsed.hostname == 'ci.nii.ac.jp' or id_parsed.hostname == 'cir.nii.ac.jp':
                if fragments[1] == 'naid':
                    ids['cinii_na_id'] = {
                        'label': "CiNii",
                        'id': fragments[2],
                        "url": info['@id']
                    }
                elif fragments[1] == 'ncid':
                    ids['cinii_nc_id'] = {
                        'label': "CiNii",
                        'id': fragments[2],
                        "url": info['@id']
                    }
                elif fragments[1] == 'crid':
                    ids['cinii_cr_id'] = {
                        'label': "CiNii",
                        'id': fragments[2],
                        "url": info['@id']
                    }
                else:
                   raise Exception('unknown cinii URL: '+info['@id']) 
            elif info["label"] == 'j_global':
                if 'j_global_id' in ids:
                    continue
                else:
                    raise Exception('j_global exists in see_also but not in identifier')
            elif info['label'] == 'url':
                if id_parsed.hostname == 'arxiv.org':
                    if not ('arxiv_id' in ids):
                        ids['arxiv_id'] = {
                            'label': "arXiv",
                            'id': fragments[2],
                            "url": info['@id']
                        }
                elif id_parsed.hostname == 'jglobal.jst.go.jp':
                    m = re.search(r'(\d{18})',info['@id'])
                    print(m)
                    if m:
                        ids['j_global_id'] = {
                            'label': "J-GLOBAL ID",
                            'id': m.group(0),
                            "url": info['@id']
                        }
                else:
                    ids['url'] = {
                        'label': "URL",
                        'id': info['@id'],
                        "url": info['@id']
                    }
            else:
                pprint(i)
                raise Exception('unknown see_also type: '+info['label'])
        if len(ids)>0:
            record["ids"] = ids
        record['outside_kuaero'] = not i.get('inlab')
    except Exception as e:
        pprint(i)
        raise(e)
    records += [record]


# 出力

toml.dump({'record':records}, open('data/publications/autogen_from_researchmap.toml', mode='w', encoding='utf-8'))


