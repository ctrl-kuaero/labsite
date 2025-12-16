import requests, json, sys, os, time
import toml
from urllib.parse import urlparse, parse_qs
from pprint import pprint
import re
from datetime import datetime

members = ['maruta','fujimoto_kenji','KanaShikada']

inlab = {
    'KanaShikada': {
        'since':'2025-04-01',
        'until':'9999-99-99'
    },    
    'maruta': {
        'since':'2017-06-01',
        'until':'9999-99-99'
    },
    'fujimoto_kenji': {
        'since':'2012-10-01',
        'until':'9999-99-99'
    },
}

def fetch_all_items(base_url, name, item_type):
    """
    Fetch all items of a specific type for a member, handling pagination.
    
    Args:
        base_url (str): Base URL for the API
        name (str): Member name
        item_type (str): Type of item to fetch
        
    Returns:
        dict: Combined JSON response with all items
    """
    print(f"Fetching {item_type} for {name}...")
    
    # Initial request
    url = f"{base_url}{name}/{item_type}"
    all_items = []
    page_count = 1
    
    while url:
        print(f"  Fetching page {page_count}...")
        response = requests.get(url)
        
        # Check if request was successful
        if response.status_code != 200:
            print(f"Error fetching {url}: {response.status_code}")
            break
            
        # Parse the current page data
        data = json.loads(response.text)
        
        # Add items from current page to our collection
        if 'items' in data:
            all_items.extend(data['items'])
            print(f"  Found {len(data['items'])} items on page {page_count}")
        
        # Check for next page in Link header
        next_url = None
        if 'Link' in response.headers:
            links = response.headers['Link'].split(',')
            for link in links:
                if 'rel="next"' in link:
                    # Extract URL from link
                    next_url = link.split(';')[0].strip('<>').strip()
                    break
        
        # If no next URL found in headers, try to construct it from the response data
        if not next_url and 'totalResults' in data and 'itemsPerPage' in data:
            total = data['totalResults']
            per_page = data['itemsPerPage']
            current_start = 0
            
            # If we have a start parameter in the current URL, extract it
            if '?' in url:
                query_params = parse_qs(urlparse(url).query)
                if 'start' in query_params:
                    current_start = int(query_params['start'][0])
            
            # Calculate next start position
            next_start = current_start + per_page
            
            # If there are more items to fetch
            if next_start < total:
                # Construct next URL
                if '?' in url:
                    base_part = url.split('?')[0]
                    next_url = f"{base_part}?start={next_start}&limit={per_page}"
                else:
                    next_url = f"{url}?start={next_start}&limit={per_page}"
        
        # Update URL for next iteration or exit loop if no more pages
        url = next_url
        page_count += 1
    
    # Construct a response object similar to the original API response
    combined_response = {
        'items': all_items
    }
    
    print(f"Total {len(all_items)} {item_type} items fetched for {name}")
    return combined_response

# Download JSON files from researchmap
url = "https://api.researchmap.jp/"
itemslist = ["published_papers", "research_projects", "misc", "presentations", "books_etc"]
jsonfiles = {}

for name in members:
    jsonfiles[name] = {}
    for it in itemslist:
        jsonfiles[name][it] = fetch_all_items(url, name, it)


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
errors = []  # エラーが発生したアイテムを収集するリスト
warnings = []  # 警告が発生したアイテムを収集するリスト

def get_item_identifier(item):
    """アイテムの識別情報を取得する"""
    identifier = {
        '@id': item.get('@id'),
        '@type': item.get('@type'),
    }
    # タイトルを取得
    if 'paper_title' in item:
        identifier['title'] = item['paper_title'].get('ja') or item['paper_title'].get('en')
    elif 'book_title' in item:
        identifier['title'] = item['book_title'].get('ja') or item['book_title'].get('en')
    elif 'presentation_title' in item:
        identifier['title'] = item['presentation_title'].get('ja') or item['presentation_title'].get('en')
    elif 'research_project_title' in item:
        identifier['title'] = item['research_project_title'].get('ja') or item['research_project_title'].get('en')
    
    identifier['publication_date'] = item.get('publication_date')
    return identifier

for i in items.values():
    record = {}
    try:
        if i.get('@type') == 'misc':
            record['ja_booktitle'] = i['publication_name'].get('ja')
            record['en_booktitle'] = i['publication_name'].get('en')
            record['publication_date'] = i['publication_date'].replace('-','')
            record['publication_date'] = record['publication_date'] + "0"*(8 - len(record['publication_date']))
            misc_type = i.get('misc_type')
            if misc_type == 'summary_national_conference':
                record['type'] = 'domestic_conference'
            elif misc_type == 'introduction_scientific_journal':
                record['type'] = 'explanation_journal'
            elif misc_type == 'summary_international_conference':
                record['type'] = 'summary_international_conference'
            elif misc_type == 'technical_report':
                record['type'] = 'technical_report'
            elif misc_type == 'meeting_report':
                record['type'] = 'meeting_report'
            elif misc_type == 'others':
                record['type'] = 'others'
            elif misc_type is None:
                # If misc_type is None, default to 'others'
                warning_msg = f"misc_type is None. Defaulting to 'others'."
                print(f"Warning: {warning_msg} for item {i.get('@id')}")
                warnings.append({
                    'warning_message': warning_msg,
                    'item_identifier': get_item_identifier(i),
                    'raw_data': i
                })
                record['type'] = 'others'
            else:
                # For unknown misc_type values, print the value and default to 'others'
                warning_msg = f"Unknown misc_type '{misc_type}'. Defaulting to 'others'."
                print(f"Warning: {warning_msg} for item {i.get('@id')}")
                warnings.append({
                    'warning_message': warning_msg,
                    'item_identifier': get_item_identifier(i),
                    'raw_data': i
                })
                record['type'] = 'others'
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
                raise Exception(f"can not identify type (unknown published_paper_type: '{i.get('published_paper_type')}')")
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
            raise Exception(f"can not identify @type: '{i.get('@type')}'")

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
            elif idtype == "orcid_put_cd":
                # ORCID ID はとりあえず無視（文献のIDに対応するページが不明）
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
 
            elif info['label'] == 'web_of_science' or info['label'] == 'scopus' or info['label'] == 'scopus_citedby':
                # Web of Science ID, Scopus ID, Scopus Citedby はとりあえず無視
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
                raise Exception('unknown see_also type: '+info['label'])
        if len(ids)>0:
            record["ids"] = ids
        record['outside_kuaero'] = not i.get('inlab')
        records += [record]
    except Exception as e:
        # エラーが発生した場合、エラー情報を収集して処理を継続
        error_info = {
            'error_message': str(e),
            'item_identifier': get_item_identifier(i),
            'raw_data': i
        }
        errors.append(error_info)
        print(f"Error processing item: {error_info['item_identifier'].get('title', 'Unknown')} - {str(e)}")
        continue


# 出力

toml.dump({'record':records}, open('data/publications/autogen_from_researchmap.toml', mode='w', encoding='utf-8'))
print(f"Successfully processed {len(records)} records.")

# エラーレポートの出力
# dataディレクトリにはTOML形式で保存（HugoがデータファイルとしてTOML/JSON/YAMLのみ対応）
error_report_path = 'data/publications/autogen_errors.toml'

if len(errors) > 0:
    print(f"\n{len(errors)} errors occurred during processing.")
    
    # エラーデータをTOML形式で保存
    error_records = []
    for error in errors:
        identifier = error['item_identifier']
        error_record = {
            'error_message': error['error_message'],
            'title': identifier.get('title', '(タイトル不明)'),
            'type': identifier.get('@type', 'N/A'),
            'id': identifier.get('@id', 'N/A'),
            'publication_date': identifier.get('publication_date', 'N/A'),
            'raw_data_json': json.dumps(error['raw_data'], ensure_ascii=False, indent=2)
        }
        error_records.append(error_record)
    
    error_data = {
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'error_count': len(errors),
        'errors': error_records
    }
    
    toml.dump(error_data, open(error_report_path, mode='w', encoding='utf-8'))
    print(f"Error report saved to: {error_report_path}")
else:
    print("No errors occurred.")
    # エラーがない場合はエラーレポートを削除
    if os.path.exists(error_report_path):
        os.remove(error_report_path)

# 警告レポートの出力
warning_report_path = 'data/publications/autogen_warnings.toml'

if len(warnings) > 0:
    print(f"\n{len(warnings)} warnings occurred during processing.")
    
    # 警告データをTOML形式で保存
    warning_records = []
    for warning in warnings:
        identifier = warning['item_identifier']
        warning_record = {
            'warning_message': warning['warning_message'],
            'title': identifier.get('title', '(タイトル不明)'),
            'type': identifier.get('@type', 'N/A'),
            'id': identifier.get('@id', 'N/A'),
            'publication_date': identifier.get('publication_date', 'N/A'),
            'raw_data_json': json.dumps(warning['raw_data'], ensure_ascii=False, indent=2)
        }
        warning_records.append(warning_record)
    
    warning_data = {
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'warning_count': len(warnings),
        'warnings': warning_records
    }
    
    toml.dump(warning_data, open(warning_report_path, mode='w', encoding='utf-8'))
    print(f"Warning report saved to: {warning_report_path}")
else:
    print("No warnings occurred.")
    # 警告がない場合は警告レポートを削除
    if os.path.exists(warning_report_path):
        os.remove(warning_report_path)
