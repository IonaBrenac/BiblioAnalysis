
__all__ = ['COUNTRIES','WOS_TAGS','WOS_TAGS_DICT',
           'biblio_parser_scopus', 'biblio_parser_wos',
           'biblio_parser','build_title_keywords','read_database_wos',
           'USECOLS_SCOPUS','USECOLS_WOS',
           'merge_database','DIC_OUTDIR_PARSING','LABEL_MEANING']

DIC_OUTDIR_PARSING = {'K':'keywords.dat',
                      'AK':'authorskeywords.dat',
                      'IK':'journalkeywords.dat',
                      'TK':'titlekeywords.dat',
                      'S':'subjects.dat',
                      'S2':'subjects2.dat',
                      'AD':'addresses.dat',
                      'CU':'countries.dat',
                      'I':'institutions.dat',
                      'AU':'authors.dat',
                      'R':'references.dat',
                      'A':'articles.dat'}

LABEL_MEANING = {'AU':'co-authors',
                 'AK':'author_keywords',
                 'CU':'countries',
                 'DT':'doc_type',
                 'I':'institution',
                 'J':'journal',
                 'IK':'journal_keywords',
                 'LA':'languages',
                 'R':'references',
                 'RJ':'refjournal',
                 'S':'subjects',
                 'S2':'subjects2',
                 'TK':'title_keywords',
                 'Y':'year'}
    
COUNTRY = '''
    United States,Afghanistan,Albania,Algeria,American Samoa,Andorra,Angola,
    Anguilla,Antarctica,Antigua And Barbuda,Argentina,Armenia,Aruba,Australia,
    Austria,Azerbaijan,Bahamas,Bahrain,Bangladesh,Barbados,Belarus,Belgium,
    Belize,Benin,Bermuda,Bhutan,Bolivia,Bosnia And Herzegowina,Botswana,Bouvet Island,
    Brazil,Brunei Darussalam,Bulgaria,Burkina Faso,Burundi,Cambodia,Cameroon,Canada,
    Cape Verde,Cayman Islands,Central African Rep,Chad,Chile,China,Christmas Island,
    Cocos Islands,Colombia,Comoros,Congo,Cook Islands,Costa Rica,Cote D`ivoire,Croatia,
    Cuba,Cyprus,Czech Republic,Denmark,Djibouti,Dominica,Dominican Republic,East Timor,
    Ecuador,Egypt,El Salvador,Equatorial Guinea,Eritrea,Estonia,Ethiopia,Falkland Islands (Malvinas),
    Faroe Islands,Fiji,Finland,France,French Guiana,French Polynesia,French S. Territories,
    Gabon,Gambia,Georgia,Germany,Ghana,Gibraltar,Greece,Greenland,Grenada,Guadeloupe,Guam,
    Guatemala,Guinea,Guinea-bissau,Guyana,Haiti,Honduras,Hong Kong,Hungary,Iceland,India,
    Indonesia,Iran,Iraq,Ireland,Israel,Italy,Jamaica,Japan,Jordan,Kazakhstan,Kenya,Kiribati,
    North Korea,South Korea,Kuwait,Kyrgyzstan,Laos,Latvia,Lebanon,Lesotho,Liberia,Libya,
    Liechtenstein,Lithuania,Luxembourg,Macau,Macedonia,Madagascar,Malawi,Malaysia,Maldives,
    Mali,Malta,Marshall Islands,Martinique,Mauritania,Mauritius,Mayotte,Mexico,Micronesia,
    Moldova,Monaco,Mongolia,Montserrat,Morocco,Mozambique,Myanmar,Namibia,Nauru,Nepal,Netherlands,
    Netherlands Antilles,New Caledonia,New Zealand,Nicaragua,Niger,Nigeria,Niue,Norfolk Island,
    Northern Mariana Islands,Norway,Oman,Pakistan,Palau,Panama,Papua New Guinea,Paraguay,Peru,
    Philippines,Pitcairn,Poland,Portugal,Puerto Rico,Qatar,Reunion,Romania,Russian Federation,
    Rwanda,Saint Kitts And Nevis,Saint Lucia,St Vincent/Grenadines,Samoa,San Marino,Sao Tome,
    Saudi Arabia,Senegal,Seychelles,Sierra Leone,Singapore,Slovakia,Slovenia,Solomon Islands,
    Somalia,South Africa,Spain,Sri Lanka,St. Helena,St.Pierre,Sudan,Suriname,Swaziland,Sweden,
    Switzerland,Syrian Arab Republic,Taiwan,Tajikistan,Tanzania,Thailand,Togo,Tokelau,Tonga,
    Trinidad And Tobago,Tunisia,Turkey,Turkmenistan,Tuvalu,Uganda,Ukraine,United Arab Emirates,
    United Kingdom,Uruguay,Uzbekistan,Vanuatu,Vatican City State,Venezuela,Viet Nam,Virgin Islands (British),
    Virgin Islands (U.S.),Western Sahara,Yemen,Yugoslavia,Zaire,Zambia,Zimbabwe
'''
COUNTRIES = [x.strip() for x in COUNTRY.split(',')]

USA_STATES = '''AL,AK,AZ,AR,CA,CO,CT,DE,FL,GA,HI,ID,IL,IN,IA,KS,KY,LA,ME,MD,MA,MI,MN,MS,MO,MT,
NE,NV,NH,NJ,NM,NY,NC,ND,OH,OK,OR,PA,RI,SC,SD,TN,TX,UT,VT,VA,WA,WV,WI,WY'''
USA_STATES = [x.strip() for x in USA_STATES.split(',')]

DIC_CHANGE_CHAR = {"Ł":"L",   # polish capital to L 
                   "ł":"l",   # polish l
                   "ı":"i",    
                   "‐":"-",   # Non-Breaking Hyphen to hyphen-minus
                   "Đ":"D",   # D with stroke (Vietamese,South Slavic) to D
                   ".":"",
                   ",":""}
CHANGE = str.maketrans(DIC_CHANGE_CHAR)

WOS_TAGS = '''FN,VR,PT,AU,AF,BA,BF,CA,GP,BE,TI,SO,SE,BS,LA,DT,CT,CY,CL,
              SP,HO,DE,ID,AB,C1,RP,EM,RI,OI,FU,FX,CR,NR,TC,Z9,U1,U2,PU,
              PI,PA,SN,EI,BN,J9,JI,PD,PY,VL,IS,SI,PN,SU,MA,BP,EP,AR,DI,
              D2,EA,EY,PG,P2,WC,SC,GA,PM,UT,OA,HP,ES,HC,DA,ER,EF'''

WOS_TAGS_VALUES ='''File Name,Version Number,Publication Type (J=Journal; B=Book; S=Series;P=Patent),
Authors,Author Full Name,Book Authors,Book Authors Full Name,
Group Authors,Book Group Authors,Editors,Document Title,Publication Name,
Book Series Title,Book Series Subtitle,Language,Document Type,
Conference Title,Conference Date,Conference Location,Conference Sponsors,
Conference Host,Author Keywords,Keywords Plus,Abstract,Author Address,Reprint Address,
E-mail Address,ResearcherID Number,ORCID Identifier (Open Researcher and Contributor ID),
Funding Agency and Grant Number,Funding Text,Cited References,Cited Reference Count,
Web of Science Core Collection Times Cited Count,Total Times Cited Count 
(Web of Science Core Collection; BIOSIS Citation Index; Chinese Science Citation Database;
Data Citation Index; Russian Science Citation Index; SciELO Citation Index),
Usage Count (Last 180 Days),Usage Count (Since 2013),Publisher,Publisher City,Publisher Address,
International Standard Serial Number (ISSN),Electronic International Standard Serial Number (eISSN),
International Standard Book Number (ISBN),29-Character Source Abbreviation,
ISO Source Abbreviation,Publication Date,Year Published,Volume,Issue,Special Issue,Part Number,
Supplement,Meeting Abstract,Beginning Page,Ending Page,Article Number,Digital Object Identifier (DOI),
Book Digital Object Identifier (DOI),Early access date,Early access year,Page Count,
Chapter Count (Book Citation Index),Web of Science Categories,Research Areas,Document Delivery Number,
PubMed ID,Accession Number,Open Access Indicator,ESI Hot Paper. Note that this field is valued only for subscribers.,
ESI Highly Cited Paper. Note that this field is valued only for ESI subscribers.,
Date this report was generated.,End of Record,End of File'''
WOS_TAGS_DICT = dict(zip([x.strip() for x in WOS_TAGS.split(',')],
                         [x.strip() for x in WOS_TAGS_VALUES.split(',')]))

USECOLS_WOS ='''AB,AU,BP,BS,C1,CR,DE,DI,DT,ID,IS,LA,PY,RP,
                SC,SN,SO,TI,UT,VL,WC'''
USECOLS_WOS = [x.strip() for x in USECOLS_WOS.split(',')]


SCOPUS_TAGS = '''Authors,Title,Year,Source title,Volume,Issue,Art. No.,
Page start,Page end,Page count,Cited by,DOI,Link,Affiliations,
Authors with affiliations,Abstract,Author Keywords,Index Keywords,References,
ISSN,ISBN,CODEN,Language of Original Document,Abbreviated Source Title,
Document Type,Source,EID'''
SCOPUS_TAGS = [x.strip() for x in SCOPUS_TAGS.split(',')]

USECOLS_SCOPUS = '''Abstract,Affiliations,Authors,Author Keywords,Authors with affiliations,
       CODEN,Document Type,DOI,EID,Index Keywords,ISBN,ISSN,Issue,Language of Original Document,
       Page start,References,Source title,Title,Volume,Year'''
USECOLS_SCOPUS = [x.strip() for x in USECOLS_SCOPUS.split(',')]

HEADER = False

ALIAS_UK = '''England,Wales,North Ireland,Scotland'''
ALIAS_UK = [x.strip() for x in ALIAS_UK.split(',')]                                

ENCODING = 'iso-8859-1' # encoding used by the function read_database_wos

SCOPUS_CAT_CODES = 'scopus_cat_codes.txt'
SCOPUS_JOURNALS_ISSN_CAT = 'scopus_journals_issn_cat.txt'

NLTK_VALID_TAG_LIST = ['NN','NNS','VBG','JJ'] # you can find help on the nltk tags set
                                              # using nltk.help.upenn_tagset() 

NOUN_MINIMUM_OCCURRENCES = 3 # Minimum occurrences of a noun to be retained when 
                             # building the set of title keywords see build_title_keywords

def country_normalization(country):
    '''
    Normalize the country name for coherence seeking between wos and scopus corpuses.
    '''

    country_clean = country
    if country not in COUNTRIES:
        if country in  ALIAS_UK:
            country_clean = 'United Kingdom'
        elif 'USA' in country:
            country_clean = 'United States'
        elif ('china' in country) or ('China' in country):
            country_clean = 'China'
        elif country == 'Russia':    
            country_clean = 'Russian Federation'
        elif country == 'U Arab Emirates':    
            country_clean = 'United Arab Emirates'
        elif country == 'Vietnam':   
            country_clean = 'Viet Nam'
        else:
            country_clean = ''

    return country_clean

def read_database_wos(filename):
    
    '''Used to circumvent the error ParserError: '	' expected after '"' generated
    by the method pd.read_csv
    '''
    
    from csv import reader
    import pandas as pd

    with open(filename,'rt',encoding=ENCODING) as csv_file: 
        csv_reader = reader(csv_file, delimiter = '\t')
        csv_list = []
        for row in csv_reader:
            csv_list.append(row)

    df = pd.DataFrame(csv_list)
    
    # Columns selection and dataframe reformatting
    dc = dict(zip(df.iloc[0,:],df.columns))  # Buids {n° column: column name,...}
    df.drop(list(set(df.columns).difference(set([dc[key] for key in USECOLS_WOS]))),
            axis=1,
            inplace=True)                    # Drops unused columns
    df.columns = df.iloc[0]
    df = df.drop(0)
    df.index = range(len(df))
    
    return df

def merge_database(database,filename,in_dir,out_dir):
    
    '''Merges several databases in one database
    
    Args:
        database (string): database type (scopus or wos)
        filename (str): name of the merged database
        in_dir (str): name of the folder where the databases are stored
        out_dir (str): name of the folder where the merged databases will be stored
    
    '''
    # Standard library imports
    import os
    from pathlib import Path
    import sys

    # 3rd party imports
    import pandas as pd

    list_data_base = []
    list_df = []
    if database == 'wos':
        for path, _, files in os.walk(in_dir):
            list_data_base.extend(Path(path) / Path(file) for file in files
                                                          if file.endswith(".txt"))
        for file in list_data_base:
            list_df.append(read_database_wos(file))

    else:
        for path, _, files in os.walk(in_dir):
            list_data_base.extend(Path(path) / Path(file) for file in files
                                                          if file.endswith(".csv"))
        for file in list_data_base:
            df = pd.read_csv(file,usecols=USECOLS_SCOPUS) # reads the database
            list_df.append(df)
        
    result = pd.concat(list_df,ignore_index=True)
    result.to_csv(out_dir / Path(filename),sep='\t')

def build_title_keywords(df):
    
    '''Given the dataframe 'df' with one column 'title':
    
                    Title
            0  Experimental and CFD investigation of inert be...
            1  Impact of Silicon/Graphite Composite Electrode...
            
    the function 'build_title_keywords':
    
       1- Builds the set "keywords_TK" of the tokens appearing at least NOUN_MINIMUM_OCCURRENCE times 
    in all the article titles of the corpus. The tokens are the words of the title with nltk tags 
    belonging to the global list 'NLTK_VALID_TAG_LIST'.
       2- Adds two columns 'token' and 'pub_token' to the dataframe 'df'. The column 'token' contains
    the set of the tokenized and lemmelized (using the nltk WordNetLemmatizer) title. The column
    'pub_token' contains the list of words common to the set "keywords_TK" and to the column 'kept_tokens'
       3- Buids the list of tuples 'list_of_words_occurrences.sort'
    [(token_1,# occurrences token_1), (token_2,# occurrences token_2),...] ordered by decreasing values
    of # occurrences token_i.
    
        
    '''

    # Standard library imports
    from collections import Counter
    import operator
    
    # 3rd party imports
    import nltk
    
    def tokenizer(text):
        
        '''
        Tokenizes, lemmelizes the string 'text'. Only the words with nltk tags in the global
        NLTK_VALID_TAG_LIST are kept.
        
        ex 'Thermal stability of Mg2Si0.55Sn0.45 for thermoelectric applications' 
        gives the list : ['thermal', 'stability', 'mg2si0.55sn0.45', 'thermoelectric', 'application']
        
        Args:
            text (string): string to tokenize
            
        Returns
            The list valid_words_lemmatized 
        '''
            
        tokenized = nltk.word_tokenize(text.lower())
        valid_words = [word for (word, pos) in nltk.pos_tag(tokenized) 
                       if pos in NLTK_VALID_TAG_LIST] 

        stemmer = nltk.stem.WordNetLemmatizer()
        valid_words_lemmatized = [stemmer.lemmatize(valid_word) for valid_word in valid_words]
    
        return valid_words_lemmatized
    
    def list_keywords_TK(x):
        list_keywords_TK = list(keywords_TK.intersection(set(x)))
        if list_keywords_TK == []:
            list_keywords_TK = ['']
            
        return list_keywords_TK
        

    df['title_token'] = df['Title'].apply(tokenizer)

    bag_of_words = df.title_token.sum()

    bag_of_words_occurrences = list(Counter(bag_of_words).items())
    bag_of_words_occurrences.sort(key = operator.itemgetter(1),reverse=True)

    keywords_TK = set([x for x,y in bag_of_words_occurrences if y>=NOUN_MINIMUM_OCCURRENCES])

    df['kept_tokens'] = df['title_token'].apply(list_keywords_TK)
   
    return df,bag_of_words_occurrences 

def name_normalizer(text):
    
    '''Normalizes the author name spelling according the three debatable rules:
            - replacing none ascii letters by ascii ones
            - capitalizing first name 
            - capitalizing surnames
            - supressing comma and dot
            
       ex: name_normalizer(" GrÔŁ-biçà-vèLU D'aillön, E-kj. ")
        >>> "Grol-Bica-Velu D'Aillon E-KJ"
        
    Args:
        text (str): text to normalize
    
    Returns
        The normalized text
    '''

    # Standard library imports
    import re
    import unicodedata


    clear_data = lambda text : \
        unicodedata.normalize('NFD', text.translate(CHANGE)). \
        encode('ascii', 'ignore'). \
        decode('utf-8').strip()
    
    text = clear_data(text.lstrip())
    
    re_minus = re.compile('(-[a-zA-Z]+)')       # Captures: "cCc-cC-ccc-CCc"
    for text_minus_texts in re.findall(re_minus,text):
        text = text.replace(text_minus_texts,'-' + text_minus_texts[1:].capitalize() )
    
    re_apostrophe = re.compile("('[a-zA-Z]+)")  # Captures: "cCc'cC'ccc'cc'CCc"
    for text_minus_texts in re.findall(re_apostrophe,text):
        text = text.replace(text_minus_texts,"'" + text_minus_texts[1:].capitalize() )
        
    re_minus = re.compile('([a-zA-Z]+-)')       # Captures: "cCc-" 
    for text_minus_texts in re.findall(re_minus,text):
        text = text.replace(text_minus_texts,text_minus_texts[:-1].capitalize() + '-')
        
    re_apostrophe = re.compile("([a-zA-Z]+')")  # Captures: "cCc'"
    for text_minus_texts in re.findall(re_apostrophe,text):
        text = text.replace(text_minus_texts,text_minus_texts[:-1].capitalize() + "'")
        
    re_surname = "[a-zA-Z]+\s"                  # Captures: "cCccC "
    for text_minus_texts in re.findall(re_surname,text):
        text = text.replace(text_minus_texts,text_minus_texts.capitalize())
        
    re_minus_first_name = '\s[a-zA-Z]+-[a-zA-Z]+$'     # Captures: "cCc-cC" in the first name
    for x in  re.findall(re_minus_first_name,text):
        text = text.replace(x,x.upper())
           
    return text

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
        The dataframe df_keyword
    '''
    
    # Standard library imports
    from collections import namedtuple
    from operator import attrgetter
    import re
    
    # 3rd party imports
    import nltk
    import pandas as pd

    key_word = namedtuple('key_word',['pub_id','type','keyword'] )
    list_keyword = []

    df_AK = df_corpus['ID']
    for pub_id,x in zip(df_AK.index,df_AK):
        for y in x.split(';'):
            list_keyword.append(key_word(pub_id=pub_id,
                                         type="AK",
                                         keyword=y.lower().strip()))

    df_IK = df_corpus['DE']
    for pub_id,x in zip(df_IK.index,df_IK):
        for y in x.split(';'):
            list_keyword.append(key_word(pub_id=pub_id,
                                         type="IK",
                                         keyword=y.lower().strip()))

    df_title = pd.DataFrame(df_corpus['TI'])
    df_title.columns = ['Title']
    df_TK,list_of_words_occurrences = build_title_keywords(df_title)
    for pub_id in df_TK.index:
        for token in df_TK.loc[pub_id,'kept_tokens']:
            list_keyword.append(key_word(pub_id=pub_id,
                                             type="TK",
                                             keyword=token))

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
       the author country and affiliation.
       
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
            #authors = re_author.findall(affiliation)    # for future use
            addresses = re_address.findall(affiliation)
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
        if list_keywords_AK != ['']:
            for keyword_AK in list_keywords_AK:
                list_keyword.append(key_word(pub_id=pub_id,
                                             type="AK",
                                             keyword=keyword_AK.strip()))
        else:
            list_keyword.append(key_word(pub_id=pub_id,
                                             type="AK",
                                             keyword=''))

    df_IK = df_corpus['Index Keywords'].fillna('')
    for pub_id,keywords_IK in zip(df_IK.index,df_IK):
        list_keywords_IK = keywords_IK.split(';')
        if list_keywords_IK != ['']:
            for keyword_IK in list_keywords_IK:
                list_keyword.append(key_word(pub_id=pub_id,
                                             type="IK",
                                             keyword=keyword_IK.strip()))
        else:
            list_keyword.append(key_word(pub_id=pub_id,
                                             type="IK",
                                             keyword=''))

    df_title = pd.DataFrame(df_corpus['Title'].fillna(''))
    df_TK,list_of_words_occurrences = build_title_keywords(df_title)
    for pub_id in df_TK.index:
        for token in df_TK.loc[pub_id,'kept_tokens']:
            list_keyword.append(key_word(pub_id=pub_id,
                                             type="TK",
                                             keyword=token))

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

def biblio_parser(in_dir_parsing, out_dir_parsing, database, expert, rep_utils):
    
    '''Chooses the appropriate parser to parse wos or scopus databases
    '''
    
    if database == "wos":
        biblio_parser_wos(in_dir_parsing, out_dir_parsing)
    elif database == "scopus":
        biblio_parser_scopus(in_dir_parsing, out_dir_parsing, rep_utils)
    else:
        raise Exception("Sorry, unrecognized database {database} : should be wos or scopus ")







