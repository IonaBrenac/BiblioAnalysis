__all__ = ['biblio_parser_wos','read_database_wos']


from .BiblioParsingGlobals import DIC_OUTDIR_PARSING
from .BiblioParsingGlobals import ENCODING
from .BiblioParsingGlobals import HEADER
from .BiblioParsingGlobals import USECOLS_WOS
from .BiblioParsingGlobals import WOS_TAGS
from .BiblioParsingGlobals import WOS_TAGS_DICT

from .BiblioParsingUtils import country_normalization
from .BiblioParsingUtils import build_title_keywords
from .BiblioParsingUtils import name_normalizer

def read_database_wos(filename):
    
    '''Used to circumvent the error ParserError: '	' expected after '"' generated
    by the method pd.read_csv
    '''
    # Standard library imports
    import sys
    import csv
    
    # 3rd party imports
    import pandas as pd
    
    from .BiblioParsingGlobals import FIELD_SIZE_LIMIT
    
    csv.field_size_limit(FIELD_SIZE_LIMIT) # To extend the field size limit for reading .txt files

    with open(filename,'rt',encoding=ENCODING) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter = '\t')
        csv_list = []
        for row in csv_reader:
            csv_list.append(row)

    df = pd.DataFrame(csv_list)
    
    # Columns selection and dataframe reformatting
    dc = dict(zip(df.iloc[0,:],df.columns))  # Builds {n° column: column name,...}
    df.drop(list(set(df.columns).difference(set([dc[key] for key in USECOLS_WOS]))),
            axis=1,
            inplace=True)                    # Drops unused columns
    df.columns = df.iloc[0]
    df = df.drop(0)
    df.index = range(len(df))
    
    return df

def build_references_wos(df_corpus=None):
   
    '''Builds the dataframe "df_references" of cited references by the article
    referenced with the key publi_id:
   
            pub_id  author     year         journal          volume  page
        0    0    Bellouard Q  2017   INT. J. HYDROG. ENERGY   42    13486
        1    0    Bellouard Q  2017   ENERGY FUELS             31    10933
        2    0    Bellouard Q  2018   INT. J. HYDROG. ENERGY   44    19193
 
    Args:
        df_corpus (dataframe): the dataframe of the wos/scopus corpus
 
 
    Returns:
        A dataframe df_keyword
    '''
 
    # Standard library imports
    import re
    from collections import namedtuple
 
    # 3rd party imports
    import pandas as pd
 
    ref_article = namedtuple('ref_article',
                                 ['pub_id','author','year','journal','volume','page'] )
 
 
    re_author = re.compile('^[^,0123456789:]*,')                # Captures: "ccccc ccccc,"            
    re_year = re.compile(',\s\d{4},')                           # Captures: ", dddd,"
    re_page = re.compile(',\s+P\d{1,6}')                        # Captures: ", Pdddd"
    re_vol = re.compile(',\s+V\d{1,6}')                         # Captures: ", Vdddd"
    re_journal = re.compile('''(?<=,)\s[A-Z]{2}[0-9A-Z&\s\-\.\[\]]+(?=,)         # Captures ", Science & Dev.[3],"
                               |
                               (?<=,)\s[A-Z]{2}[0-9A-Z&\s\-\.\[\]]+$''',re.X)
 
    list_ref_article =[]
    for pub_id, row in zip(list(df_corpus.index),
                                df_corpus['CR']):
 
        if isinstance(row, str): # if the reference field is not empty and not an URL
 
                for field in row.split(";"):
 
                    year = re.findall(re_year, field) 
                    if len(year):
                        year = year[0][1:-1]
                    else:
                        year = 0
 
                    vol = re.findall(re_vol, field)
                    if len(vol):
                        vol = vol[0][3:]
                    else:
                        vol = 0
 
                    page = re.findall(re_page, field)
                    if len(page):
                        page = page[0][3:]
                    else:
                        page = 0
 
                    journal = re.findall(re_journal, field)
                    if len(journal):
                        journal = journal[0].strip()
                    else:
                        journal = 'unknown'
 
                    author = re.findall(re_author, field)
                    if len(author):
                        author = name_normalizer(author[0][:-1])
                    else:
                        author = 'unknown'
 
                    if (author != 'unknown') and (journal != 'unknown'):
                        list_ref_article.append(ref_article(pub_id,author,year,journal,vol,page))
 
                    if (vol==0) & (page==0) & (author != 'unknown'):
                        pass
 
 
    df_references = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_ref_article],
                                            'author':[s.author for s in list_ref_article],
                                            'year':[s.year for s in list_ref_article],                             
                                            'journal':[s.journal for s in list_ref_article],
                                            'volume':[s.volume for s in list_ref_article],
                                            'page':[s.page for s in list_ref_article]})
    return df_references

def build_authors_wos(df_corpus=None):
    
    '''Builds the dataframe "df_co_authors" of the co-authors of the article
    referenced with the key publi_id:
    
               pub_id  idx_author   co-author
          0        0      0          Boujjat H.
          1        0      1          Rodat S.

    Args:
        df_corpus (dataframe): the dataframe of the wos/scopus corpus

    Returns:
        The dataframe df_country
    '''

    # Standard library imports
    from collections import namedtuple
    
    # 3rd party imports
    import pandas as pd
    
    nt_co_author = namedtuple('co_author',['pub_id','idx_author','co_author'] )
    
    list_author = []
    for pub_id,x in zip(df_corpus.index,
                        df_corpus['AU']):
        idx_author = 0
        for y in x.split(";"):
            author = name_normalizer(y.replace('.','').replace(',',''))  # <----- to be checked
            
            if author not in ['Dr','Pr','Dr ','Pr ']:
                list_author.append(nt_co_author(pub_id,
                                                idx_author,
                                                author))
                idx_author += 1
                
    df_co_authors = pd.DataFrame.from_dict(
                    {'pub_id':[s.pub_id for s in list_author],
                     'idx_author':[s.idx_author for s in list_author],
                     'co-author':[s.co_author for s in list_author]})
    df_co_authors = df_co_authors[df_co_authors['co-author'] != ""] 
    
    return df_co_authors

def build_keywords_wos(df_corpus=None,dic_failed=None):
    
    '''Builds the dataframe "df_keyword" with three columns:
                pub_id  type  keyword
            0     0      AK    Biomass
            1     0      AK    Gasification
            2     0      AK    Solar energy
    with: 
         type = AK for author keywords 
         type = IK for journal keywords
         type = TK for title keywords
         
    The title keywords are builds out of the set TK_corpus of the most cited nouns 
    (at leat N times) in the set of all the articles. The keywords of type TK of an
    article, referenced by the key pub_id, are the elements of the intersection
    between the set TK_corpus and the set of the nouns of the article title.
    
        
    Args:
        df_corpus (dataframe): the dataframe of the wos/scopus corpus

    Returns:
        df_keyword (dataframe): pub_id | type | keyword 
        dic_failed (dict): dic_failed[type] = {"success (%)":rate of success,
                            "pub_id":list of orphan article}
    '''
    
    # Standard library imports
    from collections import namedtuple
    from operator import attrgetter
    import re
    
    # 3rd party imports
    import nltk
    import pandas as pd

    key_word = namedtuple('key_word',['pub_id','type','keyword'] )
    list_keyword = []  # List of namedtuple key_word

    df_AK = df_corpus['ID'] # Pick the author keywords column
    for pub_id,ak_keywords in zip(df_AK.index,df_AK):
        for ak_keyword in ak_keywords.split(';'): # Skip empty field
            ak_keyword = ak_keyword.lower().strip()
            list_keyword.append(key_word(pub_id=pub_id,
                                         type="AK",
                                         keyword=ak_keyword if ak_keyword != 'null' else '"null"'))

    df_IK = df_corpus['DE'] # Pick the journal keywords column
    for pub_id,ik_keywords in zip(df_IK.index,df_IK):
        for ik_keyword in ik_keywords.split(';'): # Skip empty field
            ik_keyword = ik_keyword.lower().strip()
            list_keyword.append(key_word(pub_id=pub_id,
                                         type="IK",
                                         keyword=ik_keyword if ik_keyword != 'null' else '"null"'))

    df_title = pd.DataFrame(df_corpus['TI']) # Pick the title column
    df_title.columns = ['Title']
    df_TK,list_of_words_occurrences = build_title_keywords(df_title)
    for pub_id in df_TK.index:
        for token in df_TK.loc[pub_id,'kept_tokens']:
            token = token.lower().strip()
            list_keyword.append(key_word(pub_id=pub_id,
                                             type="TK",
                                             keyword=token if token != 'null' else '"null"')) 

    # Sort the list of nametuples key_word by ascending value od pub_id
    list_keyword = sorted(list_keyword, key=attrgetter('pub_id'))
    df_keyword = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_keyword],
                                         'type':[s.type for s in list_keyword],
                                         'keyword':[s.keyword for s in list_keyword]}) 
    
    df_failed = df_keyword[df_keyword["keyword"] == ""]
    for type in ["AK","IK","TK"]:
        list_id = df_failed[df_failed['type']==type]['pub_id'].values
        list_id = list(set(list_id))
        dic_failed[type] = {"success (%)":100*(1-len(list_id)/len(df_corpus)),
                            "pub_id":[int(x) for x in list(list_id)]}
    
    df_keyword = df_keyword[df_keyword["keyword"] != ""]
    
    return df_keyword
    
def  build_addresses_countries_institutions_wos(df_corpus=None,dic_failed=None):
    
    '''Parse the field 'C1' of wos database to retrieve the article author address (without duplicates),
       the author country and affiliation. Beware, multiple formats may exist for the 'C1' field. 
       We take care for two different formats in this implementation.
       
    For example the string:

    '[Boujjat, Houssame] CEA, LITEN Solar & Thermodynam Syst Lab L2ST, F-38054 Grenoble, France;
     [Boujjat, Houssame] Univ Grenoble Alpes, F-38000 Grenoble, France; 
     [Rodat, Sylvain; Chuayboon, Srirat; Abanades, Stephane] CNRS, Proc Mat & Solar Energy Lab,
     PROMES, 7 Rue Four Solaire, F-66120 Font Romeu, France'

       will be parsed in:
    
    df_address:
    
    pub_id  idx_address                     address   
        0       0        CEA, LITEN Solar & Thermodynam Syst Lab L2ST, ...
        0       1        Univ    Grenoble Alpes, F-38000 Grenoble, France;
        0       2        CNRS,   Proc Mat & Solar Energy Lab, PROMES, 7 ...
    
    df_country:
        
    pub_id  idx_author   country
      0        0         France
      0        1         France
      0        2         France
      0        3         France
      0        4         France
      
   df_institution: 
   
   pub_id  idx_author   country
     0       0          CEA
     0       1          University Grenoble Alpes
     0       2          CNRS
     0       3          CNRS
     0       4          CNRS

    Args:
        df_corpus (dataframe): the dataframe of the wos/scopus corpus

    Returns:
        The dataframe df_address, df_country, df_institution
    '''

    # Standard library imports
    from collections import namedtuple
    import re
    
    # 3rd party imports
    import pandas as pd

    re_sub = re.compile('''[a-z]?Univ[\.a-zé]{0,6}\s    # Captures alias of University
                           | 
                           [a-z]?Univ[\.a-zé]{0,6}$''',re.X)
    
    re_author = re.compile('''(?<=\[)
                          [^0123456789:]*,
                          [^0123456789:]*
                          (?=\])''',re.X)               # Captures: "xxxx, xxx" inside brackets
    
    re_address = re.compile('''(?<=\]\s)                # Captures: "xxxxx" inside ][  
                             [^;]*                      # or inside ] end of string or ;
                            (?=; | $ )''',re.X)

    address = namedtuple('address',['pub_id','idx_address','address'] )
    country = namedtuple('country',['pub_id','idx_author','country'] )
    ref_institution = namedtuple('ref_institution',['pub_id','idx_author','institution'] )

    list_author_address = []
    list_author_countries = []
    list_institution = []

    for pub_id, affiliation in zip(df_corpus.index,
                                   df_corpus['C1']):
        
        try:
            if '[' in affiliation:                           # ex: '[Author1] address1;[Author1, Author2] address2...'
                #authors = re_author.findall(affiliation)    # for future use
                addresses = re_address.findall(affiliation)
            else:                                            # ex: 'address1;address2...'
                addresses = affiliation.split(';')   
        except:
            print(pub_id,affiliation)
        
        if addresses:
            for idx, author_address in enumerate(addresses): 

                list_author_address.append(address(pub_id=pub_id,
                                                   idx_address=idx,
                                                   address=author_address))

                author_institution = author_address.split(',')[0]
                author_institution = re.sub(re_sub,"University ", author_institution)
                list_institution.append(ref_institution(pub_id=pub_id,
                                                        idx_author=idx,
                                                        institution=author_institution))

                author_country = country_normalization(author_address.split(',')[-1].replace(';','').strip())

                list_author_countries.append(country(pub_id=pub_id,
                                                     idx_author=idx,
                                                     country=author_country))
        else:
            list_author_address.append(address(pub_id=pub_id,
                                                   idx_address=0,
                                                   address=''))
            list_institution.append(ref_institution(pub_id=pub_id,
                                                        idx_author=0,
                                                        institution=''))
            list_author_countries.append(country(pub_id=pub_id,
                                                     idx_author=0,
                                                     country=''))

    df_address = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_author_address],
                                         'idx_address':[s.idx_address for s in list_author_address],
                                         'address':[s.address for s in list_author_address]})
    df_address.drop_duplicates(subset=['pub_id','address'],inplace=True)

    df_country = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_author_countries],
                                         'idx_author':[s.idx_author for s in list_author_countries],
                                         'country':[s.country for s in list_author_countries]})

    df_institution = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_institution],
                                             'idx_author':[s.idx_author for s in list_institution],
                                             'institution':[s.institution for s in list_institution]})
    
    list_id = df_address[df_address["address"] == ""]['pub_id'].values
    list_id = list(set(list_id))
    dic_failed["address"] = {"success (%)":100*(1-len(list_id)/len(df_corpus)),
                                "pub_id":[int(x) for x in list(list_id)]}
    
    df_address = df_address[df_address['address'] != ""]

    list_id = df_country[df_country["country"] == ""]['pub_id'].values
    list_id = list(set(list_id))
    dic_failed["country"] = {"success (%)":100*(1-len(list_id)/len(df_corpus)),
                                "pub_id":[int(x) for x in list(list_id)]}
    df_country = df_country[df_country['country'] != ""]
    
    list_id = df_institution[df_institution["institution"] == ""]['pub_id'].values
    list_id = list(set(list_id))
    dic_failed["institution"] = {"success (%)":100*(1-len(list_id)/len(df_corpus)),
                                "pub_id":[int(x) for x in list(list_id)]}
    df_institution = df_institution[df_institution['institution'] != ""]
    
    return df_address, df_country, df_institution


def build_subjects_wos(df_corpus=None,dic_failed=None):
    
    '''Builds the dataframe "df_subject" using the column "SC":
    
            pub_id  subject
               0    Neurosciences & Neurology
               1    Psychology
               1    Environmental Sciences & Ecology
               2    Engineering
               2    Physics
               3    Philosophy
    
    
    Args:
        df_corpus (dataframe): the dataframe of the wos/scopus corpus

    Returns:
        The dataframe df_subject
    '''    
    

    from collections import namedtuple

    import pandas as pd

    subject = namedtuple('subject',['pub_id','subject'] )
    list_subject = []

    for pub_id,scs in zip(df_corpus.index,df_corpus['SC']):
        for sc in scs.split(';'):
            list_subject.append(subject(pub_id=pub_id,
                                        subject=sc.strip()))

    df_subject = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_subject],
                                         'subject':[s.subject for s in list_subject]})
    list_id = df_subject[df_subject["subject"] == ""]['pub_id'].values
    list_id = list(set(list_id))
    dic_failed["subject"] = {"success (%)":100*(1-len(list_id)/len(df_corpus)),
                             "pub_id":[int(x) for x in list(list_id)]}
    df_subject = df_subject[df_subject['subject'] != ""]

    return   df_subject

def  build_sub_subjects_wos(df_corpus=None,dic_failed=None):
    
    '''Builds the dataframe "df_wos_category" using the column "WC":
    
            pub_id  wos_category
               0    Engineering
               1    Materials Science
               1    Physics
               2    Materials Science
               2    Physics
               3    Chemistry
    
    
    Args:
        df_corpus (dataframe): the dataframe of the wos/scopus corpus

    Returns:
        The dataframe df_gross_subject
    '''
    
    from collections import namedtuple
    
    # 3rd party imports
    import pandas as pd


    keyword = namedtuple('adresse',['pub_id','wos_category'] )

    list_wos_category = []
    for pub_id, wos_categories in zip(df_corpus.index,df_corpus['WC']):
        if isinstance(wos_categories,str):
            for wos_category in wos_categories.split(';'):
                list_wos_category.append(keyword(pub_id=pub_id,
                                        wos_category=wos_category.strip()))

    df_wos_category = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_wos_category],
                                              'wos_category':[s.wos_category for s in list_wos_category]})
    
    list_id = df_wos_category[df_wos_category["wos_category"] == ""]['pub_id'].values
    list_id = list(set(list_id))
    dic_failed["subsubject"] = {"success (%)":100*(1-len(list_id)/len(df_corpus)),
                                "pub_id":[int(x) for x in list(list_id)]}
    df_wos_category = df_wos_category[df_wos_category['wos_category'] != ""]
    
    return  df_wos_category


def  build_articles_wos(df_corpus=None):
 
    '''Builds the dataframe "df_article" with ten columns:
   
    Authors|Year|Source title|Volume|Page start|DOI|Document Type|
    Language of Original Document|Title|EID
 
    Args:
        df_corpus (dataframe): the dataframe of the wos corpus
 
 
    Returns:
        The dataframe df_institution
        
    '''
    def str_int_convertor(x):
        try:
            return(int(float(x)))
        except:
            return 0
    
    def treat_author(list_authors):
        first_author = list_authors.split(';')[0] # we pick the first author
        return  name_normalizer(first_author)
 
    df_article = df_corpus.loc[:,['AU','PY', 'SO', 'VL','BP', 'DI','DT','LA','TI','SN']].astype(str)                
 
    df_article.rename (columns = {'AU':'Authors',
                                  'PY':'Year',
                                  'SO':'Source title',
                                  'VL':'Volume',
                                  'BP':'Page start',
                                  'DI':'DOI',
                                  'DT':'Document Type',
                                  'LA':'Language of Original Document',
                                  'TI':'Title',
                                  'SN':'ISSN'}, inplace = True)
                                                                                                
    df_article['Authors'] = df_article['Authors'].apply(treat_author)    
    df_article['Year'] = df_article['Year'].apply(str_int_convertor)
   
    return df_article

def biblio_parser_wos(in_dir_parsing, out_dir_parsing):
    
    '''Using the file xxxx.txt stored in the folder rawdata, the function biblio_parser_wos
    generates the files xxxx.dat stored in the folder parsing.
    home path/myfoldername/BiblioAnalysis Data/
    |-- myprojectname/
    |   |-- rawdata/
    |   |   |-- xxxx.txt
    |   |-- parsing/
    |   |   |-- addresses.dat, articles.dat, authors.dat, countries.dat, database.dat  
    |   |   |-- institutions.dat, keywords.dat, references.dat, subjects.dat, subjects2.dat
    
    The columns USECOLS_WOS of the tsv file xxxx.txt are read and the parsed using the 
    functions:
        build_references_wos which parses the column 'CR'
        build_authors_wos which parses the column 'AU'
        build_keywords_wos which parses the column 'ID' (for author keywords AK),
                                        the column 'DE' (for journal keywords IK),
                                        the column 'TI' (for title keywords IK)
        build_addresses_countries_institutions_wos which parses the column 'C1'
        build_subjects_wos which parses the column 'SC'
        build_sub_subjects_wos which parses the column 'WC'
        build_articles_wos which parses the column 'AU', 'PY', 'SO', 'VL', 'BP',
                                                   'DI', 'DT', 'LA', 'TI', 'SN'
    '''
    
    # Standard library imports
    import os
    import json
    from pathlib import Path
    
    # 3rd party imports
    import pandas as pd 

    with open(Path(out_dir_parsing) / Path('database.dat'), "w") as file:
        file.write("wos")

    list_data_base = []
    for path, _, files in os.walk(in_dir_parsing):
        list_data_base.extend(Path(path) / Path(file) for file in files
                                                      if file.endswith(".txt"))

    filename = list_data_base[0]
    
    df = read_database_wos(filename)
    dic_failed = {}
    dic_failed['number of article'] = len(df)
    
    item = 'AU' # Deals with authors
    df_AU = build_authors_wos(df_corpus=df)
    df_AU.to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item] ), 
                 index=False,
                 sep='\t',
                 header=HEADER)
    
    item = 'K'  # Deals with keywords
    df_K = build_keywords_wos(df_corpus=df,dic_failed=dic_failed)
    df_K.to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                index=False,
                sep='\t',
                header=HEADER)
    
    item = 'AK'  # Deals with authors keywords
    df_K.query('type==@item')[['pub_id','keyword']].to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                index=False,
                sep='\t',
                header=HEADER)
    
    item = 'IK'  # Deals with journal keywords
    df_K.query('type==@item')[['pub_id','keyword']].to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                index=False,
                sep='\t',
                header=HEADER)
    
    item = 'TK'  # Deals with title keywords
    df_K.query('type==@item')[['pub_id','keyword']].to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                index=False,
                sep='\t',
                header=HEADER)    
                    
    item = 'AD'  # Deals with addresses
    df_AD, df_CU, df_I = build_addresses_countries_institutions_wos(df_corpus=df,dic_failed=dic_failed)
    df_AD.to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                 index=False,
                 sep='\t',
                 header=HEADER)
    
    item = 'CU'  # Deals with countries
    df_CU.to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                 index=False, 
                 sep='\t',
                 header=HEADER)
    
    item = 'I'   # Deals with institutions
    df_I.to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                 index=False, 
                 sep='\t',
                 header=HEADER)
    
    item = 'S'   # Deals with subjects
    df_S = build_subjects_wos(df_corpus=df,dic_failed=dic_failed)
    df_S.to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                index=False,
                sep='\t',
                header=HEADER)

    item = 'S2'   # Deals with sub-subjects
    df_S2 = build_sub_subjects_wos(df_corpus=df,dic_failed=dic_failed)
    df_S2.to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                index=False,
                sep='\t',
                header=HEADER)
    
    item = 'A'   # Deals with articles
    df_A = build_articles_wos(df_corpus=df)
    df_A.to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                index=True,
                sep='\t',
                header=HEADER)
    
    item = 'R'   # Deals with references
    df_R = build_references_wos(df_corpus=df)
    df_R.to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                index=False, 
                sep='\t',
                header=HEADER)
                
    with open(Path(out_dir_parsing) / Path('failed.json'), 'w') as write_json:
        json.dump(dic_failed, write_json,indent=4)