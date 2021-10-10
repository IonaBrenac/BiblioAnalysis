__all__ = ['biblio_parser_scopus']

from .BiblioParsingGlobals import DIC_OUTDIR_PARSING
from .BiblioParsingGlobals import HEADER
from .BiblioParsingGlobals import SCOPUS_CAT_CODES
from .BiblioParsingGlobals import SCOPUS_JOURNALS_ISSN_CAT
from .BiblioParsingGlobals import SCOPUS_TAGS
from .BiblioParsingGlobals import USECOLS_SCOPUS

from .BiblioParsingUtils import country_normalization
from .BiblioParsingUtils import build_title_keywords
from .BiblioParsingUtils import name_normalizer

def build_authors_scopus(df_corpus=None):
    
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
                        df_corpus['Authors']):
        idx_author = 0
        for y in x.split(","):
            author = name_normalizer(y.replace('.',''))
            
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


def build_references_scopus(df_corpus=None):
    
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
    from collections import namedtuple
    import re
    
    # 3rd party imports
    import pandas as pd
    

    ref_article = namedtuple('ref_article',
                             ['pub_id','author','year','journal','volume','page'] )
    list_ref_article =[]

    re_author = re.compile('^[^,0123456789:]*,'               # Captures: "ccccc, ccccc,"
                           '[^,0123456789:]*,')                                      
    re_year = re.compile(r'(?<=\()\d{4}(?=\))')               # Captures: "dddd" within parenthesis
    re_page = re.compile('\s+[p]{1,2}\.\s+[a-zA-Z0-9]{1,9}')  # Captures: "pp. ddd" or "p. ddd"
    re_vol = re.compile(''',\s+\d{1,6},                       # Capture: ", dddd,"
                        |
                        ,\s+\d{1,6}\s\(                       # or: ", dddd ("
                        |
                        ,\s+\d{1,6}$''',re.X)                 # or: ", dddd" at the string end
    re_journal = re.compile('''\(\d{4}\)\s+[^,]*,             # Capures "(dddd) cccccc," c not a comma
                            |
                            \(\d{4}\)\s+[^,]*$''',re.X)       # or "(dddd) cccccc" at the end

    dic_ref = {}
    for pub_id, row in zip(list(df_corpus.index),
                                df_corpus['References']):

        if isinstance(row, str): # if the reference field is not empty and not an URL

            for field in row.split(";"):
                author = re.findall(re_author, field)
                if len(author):
                    author = name_normalizer(author[0])
                else:
                    author = 'unknown'

                year = re.findall(re_year, field)  
                if len(year):
                    year = year[0]
                else:
                    year = 0

                journal = re.findall(re_journal, field)
                if journal:
                    if ',' in journal[0] :
                        journal = journal[0][6:-1].upper()
                    else:
                        journal = journal[0][6:].upper()
                else:
                    journal = 'unknown'

                vol = re.findall(re_vol, field)
                if len(vol):
                    if ',' in vol[0]:
                        vol = re.findall(r'\d{1,6}',vol[0])[0]
                    else:
                        vol = vol[0].strip()
                else:
                    vol = 0

                page = re.findall(re_page, field)
                if len(page) == 0:
                    page = 0
                else:
                    page = page[0].split('p.')[1]

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


def  build_sub_subjects_scopus(df_corpus=None,
                     path_scopus_cat_codes=None,
                     path_scopus_journals_issn_cat=None,
                     dic_failed=None):
    
    '''Builds the dataframe "df_fine_subjects" with two columns 'publi_id' and 'ASJC_description'
    ex:       pub_id   ASJC_description
        0       0      Applied Mathematics
        1       0      Industrial and Manufacturing Engineering

    Args:
        df_corpus (dataframe): the dataframe of the wos/scopus corpus
        path_scopus_cat_codes (path): full path of the file path_scopus_cat_codes.txt
        path_scopus_journals_issn_cat (path): full path of the file scopus_journals_issn_cat.txt

    Returns:
        The dataframe fine_subjects
    '''
    
    # 3rd party imports
    import pandas as pd

    # Builds the dict "code_cat" {ASJC classification codes:description} out of the file "scopus_cat_codes.txt"
    # ex: {1000: 'Multidisciplinary', 1100: 'General Agricultural and Biological Sciences',...}
    # -------------------------------------------------------------------------------------------------
    df_scopus_cat_codes = pd.read_csv(path_scopus_cat_codes,
                                      sep='\t',
                                      header=None)
    code_cat = dict(zip(df_scopus_cat_codes[1].fillna(0.0).astype(int),df_scopus_cat_codes[0]))

    # Builds the dataframe "df_scopus_journals_issn_cat" out of the file "scopus_journals_issn_cat.txt"
    # "df_scopus_journals_issn_cat" has three columns:
    #       "journal": scopus journal name
    #       "issn": journal issn
    #       "keyword_id": list of keywords id asoociated to the journal or the issn
    # -----------------------------------------------------------------------------
    df_scopus_journals_issn_cat = pd.read_csv(path_scopus_journals_issn_cat,
                                              sep='\t',
                                              header=None).fillna(0) 
    df_scopus_journals_issn_cat[2] = df_scopus_journals_issn_cat[2].str.split(';')
    df_scopus_journals_issn_cat.columns = ['journal','issn','keyword_id']


    # Builds the list "res" of tuples [(publi_id,scopus category),...]
    # ex: [(0, 'Applied Mathematics'), (0, 'Materials Chemistry'),...]
    # ----------------------------------------------------------------
    res = [] 
    for pub_id,journal, issn in zip(df_corpus.index,
                                    df_corpus['Source title'],
                                    df_corpus['ISSN'] ):
        keywords = df_scopus_journals_issn_cat.query('journal==@journal ')['keyword_id']

        if len(keywords):                # Checks if journal found in scopus journal list
            try:                         # Checks if keywords id not empty (nan)
                keywords = keywords.tolist()
                for keyword in keywords: # append keyword dont take care of duplicates
                    res.extend([(pub_id,code_cat[int(i)]) for i in keyword[:-1]])
            except:
                res.extend([(pub_id,'')])

        else:                            # check if journal found in scopus issn list
            keywords = df_scopus_journals_issn_cat.query('issn==@issn')['keyword_id']

            if len(keywords):
                try:
                    keywords = keywords.tolist()
                    for keyword in keywords: # append keyword dont take care of duplicates
                        res.extend([(pub_id,code_cat[int(i)]) for i in keyword[:-1]])
                except:
                    res.extend([(pub_id,'')])

    # Builds the dataframe "df_keyword" out of tuples [(publi_id,scopus category),...]
    # "df_keyword" has two columns "pub_id" and "scopus_keywords". 
    # The duplicated rows are supressed.
    # ----------------------------------------------------------------            
    list_pub_id,list_keywords = zip(*res)
    df_fine_subjects = pd.DataFrame.from_dict({'pub_id':list_pub_id,
                                               'ASJC_description':list_keywords})
    list_id = df_fine_subjects[df_fine_subjects["ASJC_description"] == ""]['pub_id'].values
    dic_failed["subsubject"] = {"success (%)":100*(1-len(list_id)/len(df_corpus)),
                                "pub_id":[int(x) for x in list(list_id)]}
    df_fine_subjects.drop_duplicates(inplace=True)
    
    df_fine_subjects = df_fine_subjects[df_fine_subjects['ASJC_description'] != ""]
    
    return df_fine_subjects 

def  build_addresses_countries_institutions_scopus(df_corpus=None,dic_failed=None):
    
    '''Builds the dataframe "df_address" from the column "Affiliations" of the scopus corpus:
    
            pub_id  idx_address  address
              0         0         CEA-LITEN Solar and ...
              0         1         Univ. Grenoble Alpes, Grenoble, F-38000, France
              0         2         Processes, Materials and Solar Energy Laboratory,...
        
    where: idx_address is the rank of the address in the list of affiliations
    of the article referenced with the key pub_id.
    We use the column 'Affiliations' formated as :
    
    'CEA-LITEN Solar and Thermodynamic Systems Laboratory (L2ST), Grenoble, F-38054, France;
    Univ. Grenoble Alpes, Grenoble, F-38000, France;
    Processes, Materials and Solar Energy Laboratory, PROMES-CNRS, 
    7 Rue du Four Solaire, Font-Romeu, 66120, France'
    
    Args:
        df_corpus (dataframe): the dataframe of the wos/scopus corpus


    Returns:
        The dataframe df_address
         
    '''
    # Standard library imports
    from collections import namedtuple
    import re
    
    # 3rd party imports
    import pandas as pd
    
    re_sub = re.compile('[a-z]?Univ[\.a-zé]{0,6}\s|'# Captures alias of University 
                        '[a-z]?Univ[\.a-zé]{0,6}$')

    address = namedtuple('address',['pub_id','idx_address','address'] )
    ref_country = namedtuple('country',['pub_id','idx_address','country'] )
    ref_institution = namedtuple('ref_institution',['pub_id','idx_address','institution'] )

    list_addresses = []
    list_institution = []
    list_countries =[]
    for pub_id, affiliation in zip(df_corpus.index,
                                   df_corpus['Affiliations']):
        list_affiliation = affiliation.split(";")
        
        if list_affiliation:
            for idx_address, address_pub in enumerate(list_affiliation):

                list_addresses.append(address(pub_id=pub_id,
                                             idx_address=idx_address,
                                             address=address_pub))

                institution = address_pub.split(',')[0]
                institution = re.sub(re_sub,"University ", institution)
                list_institution.append(ref_institution(pub_id=pub_id,
                                                        idx_address=idx_address,
                                                        institution=institution))
                country = address_pub.split(',')[-1].replace(';','').strip()  
                country = country_normalization(country)

                list_countries.append(ref_country(pub_id=pub_id,
                                                     idx_address=idx_address,
                                                     country=country))
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
            

    df_address = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_addresses],
                                         'idx_address':[s.idx_address for s in list_addresses],
                                         'address':[s.address for s in list_addresses]})
    
    df_country = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_countries],
                                     'idx_address':[s.idx_address for s in list_countries],
                                     'country':[s.country for s in list_countries]})

    df_institution = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_institution],
                                             'idx_address':[s.idx_address for s in list_institution],
                                             'institution':[s.institution for s in list_institution]})
    
    list_id = df_address[df_address["address"] == ""]['pub_id'].values
    dic_failed["address"] = {"success (%)":100*(1-len(list_id)/len(df_corpus)),
                                "pub_id":[int(x) for x in list(list_id)]}
    
    df_address = df_address[df_address['address'] != ""]
    
    
    list_id = list(set(df_country[df_country["country"] == ""]['pub_id'].values))
    dic_failed["country"] = {"success (%)":100*(1-len(list_id)/len(df_corpus)),
                                "pub_id":[int(x) for x in list(list_id)]}
    df_country = df_country[df_country['country'] != ""]
    
    list_id = df_institution[df_institution["institution"] == ""]['pub_id'].values
    dic_failed["institution"] = {"success (%)":100*(1-len(list_id)/len(df_corpus)),
                                "pub_id":[int(x) for x in list(list_id)]}
    df_institution = df_institution[df_institution['institution'] != ""]
    
    return df_address, df_country, df_institution

def build_keywords_scopus(df_corpus=None,dic_failed=None):
    
    '''Builds the dataframe "df_keyword" with three columns:
                pub_id  type  keyword
            0     0      AK    Biomass
            1     0      AK    Gasification
            2     0      AK    Solar energy
    with: 
         type = AK for author keywords 
         type = IK for journal keywords
         type = TK for title keywords 
         
    The author keywords are extracted from the scopus column 'Author Keywords' 
    The journal keywords are extracted from the scopus column 'Index Keywords' 
    The title keywords are builds out of the set TK_corpus of the most cited nouns 
      (at leat N times) in the set of all the articles. The keywords of type TK of an
      article, referenced by the key pub_id, are the elements of the intersection
      between the set TK_corpus and the set of the nouns of the article title.
    
        
    Args:
        df_corpus (dataframe): the dataframe of the wos/scopus corpus

    Returns:
        The dataframe df_keyword
    '''
    
    # Standard library imports
    from collections import namedtuple
    from collections import Counter
    from operator import attrgetter
    import re
    
    # 3rd party imports
    import nltk
    import pandas as pd

    key_word = namedtuple('key_word',['pub_id','type','keyword'] )
    list_keyword = []

    df_AK = df_corpus['Author Keywords'].fillna('')
    for pub_id,keywords_AK in zip(df_AK.index,df_AK):
        list_keywords_AK = keywords_AK.split(';')      
        for keyword_AK in list_keywords_AK:
            keyword_AK = keyword_AK.strip()
            list_keyword.append(key_word(pub_id=pub_id,
                                         type="AK",
                                         keyword=keyword_AK if keyword_AK != 'null' else '”null”'))

    df_IK = df_corpus['Index Keywords'].fillna('')
    for pub_id,keywords_IK in zip(df_IK.index,df_IK):
        list_keywords_IK = keywords_IK.split(';')
        for keyword_IK in list_keywords_IK:
            keyword_IK = keyword_IK.strip()
            if keyword_IK == 'null': keyword_IK = 'unknown' # replace Null by the keyword 'unknown'
            list_keyword.append(key_word(pub_id=pub_id,
                                         type="IK",
                                         keyword=keyword_IK if keyword_IK != 'null' else '”null”'))


    df_title = pd.DataFrame(df_corpus['Title'].fillna(''))
    df_TK,list_of_words_occurrences = build_title_keywords(df_title)
    for pub_id in df_TK.index:
        for token in df_TK.loc[pub_id,'kept_tokens']:
            token = token.strip()
            list_keyword.append(key_word(pub_id=pub_id,
                                             type="TK",
                                             keyword=token if token != 'null' else '”null”'))

    list_keyword = sorted(list_keyword, key=attrgetter('pub_id'))
    df_keyword = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_keyword],
                                         'type':[s.type for s in list_keyword],
                                         'keyword':[s.keyword for s in list_keyword]})
    
    df_failed = df_keyword[df_keyword["keyword"] == ""]
    for type in ["AK","IK","TK"]:
        list_id = df_failed[df_failed['type']==type]['pub_id'].values
        dic_failed[type] = {"success (%)":100*(1-len(list_id)/len(df_corpus)),
                            "pub_id":[int(x) for x in list(list_id)]}
        
    df_keyword = df_keyword[df_keyword["keyword"] != ""]
    
    return df_keyword

def  build_subjects_scopus(df_corpus=None,
                          path_scopus_cat_codes=None,
                          path_scopus_journals_issn_cat=None,
                          dic_failed=None):
    
    '''Builds the dataframe "df_gross_subject" with two columns 'publi_id' 
    and 'ASJC_description'
    
    ex:       pub_id   ASJC_description
        0       0      Mathematics
        1       0      Engineering
         
    the AJS_description is the generic name of category given every multiple of 1OO in the 
    scopus_cat_codes.txt file. For exemple an extract of the scopus_cat_codes.txt file:
    
    General Medicine                 2700  mutiple of 100 General category
    Medicine (miscellaneous)         2701  subcategory
    Anatomy                          2702
    Anesthesiology and Pain Medicine 2703
    Biochemistry, medical            2704
    
    The codes attached to a journal are given in the tcv file scopus_journals_issn_cat:
    
    21st Century Music \t 15343219 \t 1210; 
    2D Materials \t \t     2210; 2211; 3104; 2500; 1600; 
    3 Biotech \t 2190572X \t1101; 2301; 1305;
    
    Args:
        df_corpus (dataframe): the dataframe of the wos/scopus corpus
        path_scopus_cat_codes=None,
        path_scopus_journals_issn_cat=None):

    Returns:
        The dataframe df_gross_subject
    '''
    # 3rd party imports
    import pandas as pd

    # Builds the dict "code_cat" {ASJC classification codes:description} out 
    # of the file "scopus_cat_codes.txt"
    # ex: {1000: 'Multidisciplinary', 1100: 'General Agricultural',...}
    # -----------------------------------------------------------------------
    df_scopus_cat_codes = pd.read_csv(path_scopus_cat_codes,
                                      sep='\t',
                                      header=None)
    code_cat = dict(zip(df_scopus_cat_codes[1].fillna(0.0).astype(int),
                        df_scopus_cat_codes[0]))

    # Builds the dataframe "df_scopus_journals_issn_cat" out of the file
    # "scopus_journals_issn_cat.txt"
    # "df_scopus_journals_issn_cat" has three columns:
    #       "journal": scopus journal name
    #       "issn": journal issn
    #       "keyword_id": list of keywords id asociated to the journal or the issn
    # -----------------------------------------------------------------------------
    df_scopus_journals_issn_cat = pd.read_csv(path_scopus_journals_issn_cat,
                                              sep='\t',
                                              header=None).fillna(0) 
    df_scopus_journals_issn_cat[2] = df_scopus_journals_issn_cat[2].str.split(';')
    df_scopus_journals_issn_cat.columns = ['journal','issn','keyword_id']


    # Builds the list "res" of tuples [(publi_id,scopus category),...]
    # ex: [(0, 'Applied Mathematics'), (0, 'Materials Chemistry'),...]
    # ----------------------------------------------------------------
    res = [] 
    for pub_id,journal, issn in zip(df_corpus.index,
                                    df_corpus['Source title'],
                                    df_corpus['ISSN'] ):
        keywords = df_scopus_journals_issn_cat.query('journal==@journal ')['keyword_id']

        if len(keywords):                # Checks if journal found in scopus journal list
            try:                         # Checks if keywords id not empty (nan)
                keywords = keywords.tolist()
                for keyword in keywords: # append keyword dont take care of duplicates
                                         # takes index multiple of 100 to select "generic" keyword
                    res.extend([(pub_id,code_cat[int(i.strip()[0:2] + "00")].replace("General",""))
                                for i in keyword[:-1]])
            except:
                res.extend([(pub_id,'')])

        else:                            # check if journal found in scopus issn list
            keywords = df_scopus_journals_issn_cat.query('issn==@issn')['keyword_id']

            if len(keywords):
                try:
                    keywords = keywords.tolist()
                    for keyword in keywords: # append keyword dont take care of duplicates
                                             # takes index multiple of 100 to select "generic" keyword
                        res.extend([(pub_id,code_cat[int(i.strip()[0:2] + "00")].\
                                     replace("General",""))
                                     for i in keyword[:-1]])
                except:
                    res.extend([(pub_id,'')])

    # Builds the dataframe "df_keyword" out of tuples [(publi_id,scopus category),...]
    # "df_keyword" has two columns "pub_id" and "scopus_keywords". 
    # The duplicated rows are supressed.
    # ----------------------------------------------------------------            
    list_pub_id,list_keywords = zip(*res)
    df_gross_subject = pd.DataFrame.from_dict({'pub_id':list_pub_id,
                                               'ASJC_description':list_keywords})
    
    list_id = df_gross_subject[df_gross_subject["ASJC_description"] == ""]['pub_id'].values
    dic_failed["subject"] = {"success (%)":100*(1-len(list_id)/len(df_corpus)),
                                "pub_id":[int(x) for x in list(list_id)]}
                               
    df_gross_subject = df_gross_subject[df_gross_subject['ASJC_description'] != ""]
    df_gross_subject.drop_duplicates(inplace=True)
    
    return df_gross_subject 


def  build_articles_scopus(df_corpus=None):
 
    '''Builds the dataframe "df_article" with three columns:
   
    Authors|Year|Source title|Volume|Page start|DOI|Document Type|
    Language of Original Document|Title|ISSN
 
    Args:
        df_corpus (dataframe): the dataframe of the wos/scopus corpus
 
 
    Returns:
        The dataframe df_institution
        
    '''
    
    import re

    re_issn = re.compile(r'^[0-9]{8}|[0-9]{4}|[0-9]{3}X') # Use to normalize the ISSN to the
                                                          # form dddd-dddd or dddd-dddX used by wos
    
    def convert_issn(text):
        
        y = ''.join(re.findall(re_issn,  text))
        if len(y) != 0:
            return y[0:4]+"-"+y[4:]
        else:
            return 'unknown'
   
    def str_int_convertor(x):
        try:
            return(int(float(x)))
        except:
            return 0
        
    def treat_author(list_authors):
        first_author = list_authors.split(',')[0] # we pick the first author
        return  name_normalizer(first_author)
 
    df_article = df_corpus[['Authors',
                            'Year',
                            'Source title',
                            'Volume',
                            'Page start',
                            'DOI',
                            'Document Type',
                            'Language of Original Document',
                            'Title',
                            'ISSN']].astype(str)
   
    df_article['Authors'] = df_article['Authors'].apply(treat_author)
    df_article['Year'] = df_article['Year'].apply(str_int_convertor)
    df_article['ISSN'] = df_article['ISSN'].apply(convert_issn)
   
   
    return df_article

def biblio_parser_scopus(in_dir_parsing, out_dir_parsing, rep_utils):
    
    '''Using the files xxxx.csv stored in the folder rawdata, the function biblio_parser_scopus
    generates the tsv files xxxx.dat stored in the folder parsing.
    home path//BiblioAnalysis Data/
    |-- myprojectname/
    |   |-- rawdata/
    |   |   |-- xxxx.txt
    |   |-- parsing/
    |   |   |-- addresses.dat, articles.dat, authors.dat, countries.dat, database.dat  
    |   |   |-- institutions.dat, keywords.dat, references.dat, subjects.dat, subjects2.dat 
    
    The columns USECOLS_SCOPUS of the tsv file xxxx.csv are read and the parsed using the 
    functions:
        build_references_scopus which parses the column 'References'
        build_authors_scopus which parses the column 'Authors'
        build_keywords_scopus which parses the column 'Author Keywords' (for author keywords AK),
                                        the column 'Index Keywords' (for journal keywords IK),
                                        the column 'title' (for title keywords IK)
        build_addresses_countries_institutions_scopus which parses the column 'Affiliations'
        build_subjects_scopus which parses the column 'Source title', 'ISSN'
        build_sub_subjects_scopus which parses the column 'Source title', 'ISSN'
        build_articles_scopus which parses the columns 'Authors','Year','Source title','Volume',
            'Page start','DOI','Document Type','Language of Original Document','Title','ISSN'

    '''
    
    # Standard library imports
    import json
    import os
    from pathlib import Path
    
    # 3rd party imports
    import pandas as pd 

    with open(Path(out_dir_parsing) / Path('database.dat'), "w") as file:
        file.write("scopus")

    list_data_base = []
    for path, _, files in os.walk(in_dir_parsing):
        list_data_base.extend(Path(path) / Path(file) for file in files 
                                                      if file.endswith(".csv"))

    filename = list_data_base[0]
    filename1 = rep_utils / Path(SCOPUS_CAT_CODES)
    filename2 = rep_utils / Path(SCOPUS_JOURNALS_ISSN_CAT)

    df = pd.read_csv(filename,usecols=USECOLS_SCOPUS) # reads the database
    
    dic_failed = {}
    dic_failed['number of article'] = len(df)
    
    item = 'AU' # Deals with authors
    df_AU = build_authors_scopus(df_corpus=df)
    df_AU.to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]), 
                 index=False,
                 sep='\t',
                 header=HEADER)
    
    item = 'R'   # Deals with references
    df_R = build_references_scopus(df_corpus=df)
    df_R.to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                index=False, 
                sep='\t',
                header=HEADER)
    
    item = 'S2'   # Deals with sub-subjects
    df_S2 = build_sub_subjects_scopus(df_corpus=df,
                                 path_scopus_cat_codes=filename1,
                                 path_scopus_journals_issn_cat=filename2,
                                 dic_failed=dic_failed)
    df_S2.to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                 index=False, 
                 sep='\t',
                 header=HEADER)
    
    item = 'S'   # Deals with subjects
    df_S = build_subjects_scopus(df_corpus=df,
                                path_scopus_cat_codes=filename1,
                                path_scopus_journals_issn_cat=filename2,
                                dic_failed=dic_failed)
    df_S.to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                index=False,
                sep='\t',
                header=HEADER)
    
    item = 'AD'   # Deals with addresses
    df_AD, df_CU, df_I  = build_addresses_countries_institutions_scopus(df_corpus=df,
                                                                        dic_failed=dic_failed)
    df_AD.to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                 index=False,
                 sep='\t',
                 header=HEADER)
    
    item = 'I'   # Deals with institutions
    df_I.to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                index=False,
                sep='\t',
                header=HEADER)
    
    item = 'CU'   # Deals with counties    
    df_CU.to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                 index=False, 
                 sep='\t',
                 header=HEADER)
    
    item = 'K'  # Deals with keywords
    df_K = build_keywords_scopus(df_corpus=df,dic_failed=dic_failed)
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

    item = 'A'   # Deals with articles
    df_A = build_articles_scopus(df_corpus=df)
    df_A.to_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING[item]),
                index=True,
                sep='\t',
                header=HEADER)
    
    with open(Path(out_dir_parsing) / Path('failed.json'), 'w') as write_json:
        json.dump(dic_failed, write_json,indent=4)