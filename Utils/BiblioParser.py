
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
                   "Đ":"D"}   # D with stroke (Vietamese,South Slavic) to D
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

NOUN_MINIMUM_OCCURRENCES = 3 # Minimum occurrences of a noun to be retained when 
                             # building the set of title keywords see build_title_keywords

def country_normalization(country):

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
            country_clean = 'unknown'

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
    
    dc = dict(zip(df.iloc[0,:],df.columns))  # Columns selection and dataframe reformatting
    df.drop(list(set(df.columns).difference(set([dc[key] for key in USECOLS_WOS]))),
            axis=1,
            inplace=True)
    df.columns = df.iloc[0]
    df = df.drop(0)
    df.index = range(len(df))
    
    return df

def is_noun(pos):
    
    '''Returns True if pos is the label of a noun.
    '''
    return pos[:2] == 'NN' # we aggregate NN and NNS (see nltk doc)

def build_title_keywords(list_of_title):
    
    '''build the set "keywords_TK" of the nouns appearing at least NOUN_MINIMUM_OCCURRENCE times 
    in all the articles title.
    
    Beware: we disguard the geround, verb and adjective. 
            A noun and its plural form will appear as two different keywords.
    '''

    # Standard library imports
    from collections import Counter
    
    # 3rd party imports
    import nltk

    text = ', '.join(x for x in list_of_title)


    tokenized = nltk.word_tokenize(text.lower())
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
    keywords_TK = set([x for x,y in Counter(nouns).items() if y>=NOUN_MINIMUM_OCCURRENCES])
    
    return keywords_TK

def name_normalizer(text):
    
    '''Normalizes the author name spelling according the three debatable rules:
            - replacing none ascii letters by ascii ones
            - capitalizing first name 
            - capitalizing surnames
            
       ex: name_normalizer(" GrÔŁ-biçà-vèLU D'aillön E-kj ")
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
    re_journal = re.compile(''',\s[A-Z0-9&\s\-\.\[\]]+,         # Captures ", Science & Dev.[3],"
                               |
                               ,\s[A-Z0-9&\s\-\.\[\]]+$''',re.X)


    list_ref_article =[]
    for pub_id, row in zip(list(df_corpus.index),
                                df_corpus['CR']):

        if isinstance(row, str): # if the reference field is not empty and not an URL

                for field in row.split(";"):

                    year = re.findall(re_year, field)  
                    if len(year):
                        year = year[0][1:-1]
                    else:
                        year = 2100

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
                        journal = journal[0][2:-1]
                    else:
                        journal = 'unknown'

                    author = re.findall(re_author, field)
                    if len(author):
                        author = author[0][:-1]
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
            author = name_normalizer(y.replace('.','').replace(',',''))
            
            if author not in ['Dr','Pr','Dr ','Pr ']:
                list_author.append(nt_co_author(pub_id,
                                                idx_author,
                                                author))
                idx_author += 1
                
    df_co_authors = pd.DataFrame.from_dict(
                    {'pub_id':[s.pub_id for s in list_author],
                     'idx_author':[s.idx_author for s in list_author],
                     'co-author':[s.co_author for s in list_author]})
                
    return df_co_authors

def build_keywords_wos(df_corpus=None):
    
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

    keywords_TK = build_title_keywords(df_corpus['TI'])

    key_word = namedtuple('key_word',['pub_id','type','keyword'] )
    list_keyword = []

    df_AK = df_corpus['ID'].dropna()
    for pub_id,x in zip(df_AK.index,df_AK):
        for y in x.split(';'):
            list_keyword.append(key_word(pub_id=pub_id,
                                         type="AK",
                                         keyword=y.lower().strip()))

    df_IK = df_corpus['DE'].dropna()
    for pub_id,x in zip(df_IK.index,df_IK):
        for y in x.split(';'):
            list_keyword.append(key_word(pub_id=pub_id,
                                         type="IK",
                                         keyword=y.lower().strip()))

    df_title = df_corpus['TI'].dropna()
    for pub_id, title in zip(df_title.index,df_title):
        tokenized = nltk.word_tokenize(title.lower())
        nouns = set([word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)])
        for y in keywords_TK.intersection(nouns):
            list_keyword.append(key_word(pub_id=pub_id,
                                         type="TK",
                                         keyword=y.lower()))

    list_keyword = sorted(list_keyword, key=attrgetter('pub_id'))
    df_keyword = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_keyword],
                                         'type':[s.type for s in list_keyword],
                                         'keyword':[s.keyword for s in list_keyword]})
    return df_keyword


def  build_addresses_countries_institutions_wos(df_corpus=None):
    
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
            authors = re_author.findall(affiliation)    # for future use
            addresses = re_address.findall(affiliation)
        except:
            print(pub_id,affiliation)
        

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

    df_address = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_author_address],
                                         'idx_address':[s.idx_address for s in list_author_address],
                                         'address':[s.address for s in list_author_address]})
    df_address.drop_duplicates(subset=['pub_id','address'],inplace=True)

    df_country = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_author_countries],
                                         'idx_author':[s.idx_author for s in list_author_countries],
                                         'country':[s.country for s in list_author_countries]})

    df_institution = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_institution],
                                             'idx_author':[s.idx_author for s in list_institution],
                                             'country':[s.institution for s in list_institution]})
    
    return df_address, df_country, df_institution


def build_subjects_wos(df_corpus=None):

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
    return df_subject


def  build_sub_subjects_wos(df_corpus=None):
    
    '''Builds the dataframe "df_wos_category":
    
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
    
    return df_wos_category


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
 
    df_article = df_corpus.loc[:,['AU','PY', 'SO', 'VL','BP', 'DI','DT','LA','TI','SN']].astype(str)
    df_article.AU = df_article.AU.str.split(';').str[0] # we pick the first author                     
 
    df_article.rename (columns = {'AU':'Authors',
                                  'PY':'Year',
                                  'SO':'Source title',
                                  'VL':'Volume',
                                  'BP':'Page start',
                                  'DI':'DOI',
                                  'DT':'Document Type',
                                  'LA':'Language of Original Document',
                                  'TI':'Title',
                                  'SN':'EID'}, inplace = True)
   
    df_article['Year'] = df_article['Year'].apply(str_int_convertor)
    #df_article['Volume'] = df_article['Volume'].apply(str_int_convertor)
    #df_article['Page start'] = df_article['Page start'].apply(str_int_convertor)
   
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
                    author = author[0] .replace(".","").replace(",","")
                else:
                    author = 'unknown'

                year = re.findall(re_year, field)  
                if len(year):
                    year = year[0]
                else:
                    year = 2100

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
                     path_scopus_journals_issn_cat=None):
    
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
                pass

        else:                            # check if journal found in scopus issn list
            keywords = df_scopus_journals_issn_cat.query('issn==@issn')['keyword_id']

            if len(keywords):
                try:
                    keywords = keywords.tolist()
                    for keyword in keywords: # append keyword dont take care of duplicates
                        res.extend([(pub_id,code_cat[int(i)]) for i in keyword[:-1]])
                except:
                    pass

    # Builds the dataframe "df_keyword" out of tuples [(publi_id,scopus category),...]
    # "df_keyword" has two columns "pub_id" and "scopus_keywords". 
    # The duplicated rows are supressed.
    # ----------------------------------------------------------------            
    list_pub_id,list_keywords = zip(*res)
    df_fine_subjects = pd.DataFrame.from_dict({'pub_id':list_pub_id,
                                               'ASJC_description':list_keywords})
    df_fine_subjects.drop_duplicates(inplace=True)
    
    return df_fine_subjects

def  build_addresses_countries_institutions_scopus(df_corpus=None):
    
    '''Builds the dataframe "df_address" :
    
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
        for idx_address, address_pub in enumerate(affiliation.split(";")):
                
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

    df_address = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_addresses],
                                         'idx_address':[s.idx_address for s in list_addresses],
                                         'address':[s.address for s in list_addresses]})
    
    df_country = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_countries],
                                     'idx_address':[s.idx_address for s in list_countries],
                                     'country':[s.country for s in list_countries]})

    df_institution = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_institution],
                                             'idx_address':[s.idx_address for s in list_institution],
                                             'country':[s.institution for s in list_institution]})
    
    
    return df_address, df_country, df_institution

def build_keywords_scopus(df_corpus=None):
    
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
    from collections import Counter
    from operator import attrgetter
    import re
    
    # 3rd party imports
    import nltk
    import pandas as pd
    
    keywords_TK = build_title_keywords(df_corpus['Title'])

    key_word = namedtuple('key_word',['pub_id','type','keyword'] )
    list_keyword = []

    df_AK = df_corpus['Author Keywords'].dropna()
    for pub_id,keywords_AK in zip(df_AK.index,df_AK):
        for keyword_AK in keywords_AK.split(';'):
            list_keyword.append(key_word(pub_id=pub_id,
                                         type="AK",
                                         keyword=keyword_AK.strip()))

    
    df_IK = df_corpus['Index Keywords'].dropna()
    for pub_id,keywords_IK in zip(df_IK.index,df_IK):
        for keyword_IK in keywords_IK.split(';'):
            list_keyword.append(key_word(pub_id=pub_id,
                                         type="IK",
                                         keyword=keyword_IK.strip()))

    df_title = df_corpus['Title'].dropna()
    for pub_id, title in zip(df_title.index,df_title):
        tokenized = nltk.word_tokenize(title.lower())
        nouns = set([word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)])
        for keyword_TK in keywords_TK.intersection(nouns):
            list_keyword.append(key_word(pub_id=pub_id,
                                         type="TK",
                                         keyword=keyword_TK))

    list_keyword = sorted(list_keyword, key=attrgetter('pub_id'))
    df_keyword = pd.DataFrame.from_dict({'pub_id':[s.pub_id for s in list_keyword],
                                         'type':[s.type for s in list_keyword],
                                         'keyword':[s.keyword for s in list_keyword]})
    return df_keyword

def  build_subjects_scopus(df_corpus=None,
                          path_scopus_cat_codes=None,
                          path_scopus_journals_issn_cat=None):
    
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
                pass

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
                    pass

    # Builds the dataframe "df_keyword" out of tuples [(publi_id,scopus category),...]
    # "df_keyword" has two columns "pub_id" and "scopus_keywords". 
    # The duplicated rows are supressed.
    # ----------------------------------------------------------------            
    list_pub_id,list_keywords = zip(*res)
    df_gross_subject = pd.DataFrame.from_dict({'pub_id':list_pub_id,
                                               'ASJC_description':list_keywords})
    df_gross_subject.drop_duplicates(inplace=True)
    
    return df_gross_subject


def  build_articles_scopus(df_corpus=None):
 
    '''Builds the dataframe "df_article" with three columns:
   
    Authors|Year|Source title|Volume|Page start|DOI|Document Type|
    Language of Original Document|Title|EID
 
    Args:
        df_corpus (dataframe): the dataframe of the wos/scopus corpus
 
 
    Returns:
        The dataframe df_institution
        
    '''
   
    def str_int_convertor(x):
        try:
            return(int(float(x)))
        except:
            return 0
 
    df_article = df_corpus[['Authors',
                            'Year',
                            'Source title',
                            'Volume',
                            'Page start',
                            'DOI',
                            'Document Type',
                            'Language of Original Document',
                            'Title',
                            'EID']].astype(str)
   
    df_article.Authors = df_article.Authors.str.split(',').str[0] # we pick the first author
    df_article['Year'] = df_article['Year'].apply(str_int_convertor)
   # df_article['Volume'] = df_article['Volume'].apply(str_int_convertor)
   # df_article['Page start'] = df_article['Page start'].apply(str_int_convertor)
   
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
            'Page start','DOI','Document Type','Language of Original Document','Title','EID'

    '''
    
    # Standard library imports
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
    filename1 = rep_utils / Path(scopus_cat_codes)
    filename2 = rep_utils / Path(scopus_journals_issn_cat)

    df = pd.read_csv(filename,usecols=USECOLS_SCOPUS) # reads the database

    df_AU = build_authors_scopus(df_corpus=df)
    df_AU.to_csv(Path(out_dir_parsing) / Path('authors.dat'), 
                 index=False,
                 sep='\t',
                 header=HEADER)

    df_R = build_references_scopus(df_corpus=df)
    df_R.to_csv(Path(out_dir_parsing) / Path('references.dat'),
                index=False, 
                sep='\t',
                header=HEADER)

    df_S2 = build_sub_subjects_scopus(df_corpus=df,
                                 path_scopus_cat_codes=filename1,
                                 path_scopus_journals_issn_cat=filename2)
    df_S2.to_csv(Path(out_dir_parsing) / Path('subjects2.dat'),
                 index=False, 
                 sep='\t',
                 header=HEADER)

    df_S = build_subjects_scopus(df_corpus=df,
                                path_scopus_cat_codes=filename1,
                                path_scopus_journals_issn_cat=filename2)
    df_S.to_csv(Path(out_dir_parsing) / Path('subjects.dat'),
                index=False,
                sep='\t',
                header=HEADER)

    df_AD, df_CU, df_I  = build_addresses_countries_institutions_scopus(df_corpus=df)
    df_AD.to_csv(Path(out_dir_parsing) / Path('addresses.dat'),
                 index=False,
                 sep='\t',
                 header=HEADER)
    df_I.to_csv(Path(out_dir_parsing) / Path('institutions.dat'),
                index=False,
                sep='\t',
                header=HEADER)
    df_CU.to_csv(Path(out_dir_parsing) / Path('countries.dat'),
                 index=False, 
                 sep='\t',
                 header=HEADER)

    df_K = build_keywords_scopus(df_corpus=df)
    df_K.to_csv(Path(out_dir_parsing) / Path('keywords.dat'),
                index=False,
                sep='\t',
                header=HEADER)

    df_A = build_articles_scopus(df_corpus=df)
    df_A.to_csv(Path(out_dir_parsing) / Path('articles.dat'),
                index=True,
                sep='\t',
                header=HEADER)

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
    
    
    df_AU = build_authors_wos(df_corpus=df)
    df_AU.to_csv(Path(out_dir_parsing) / Path('authors.dat'), 
                 index=False,
                 sep='\t',
                 header=HEADER)
    
    df_K = build_keywords_wos(df_corpus=df)
    df_K.to_csv(Path(out_dir_parsing) / Path('keywords.dat'),
                index=False,
                sep='\t',
                header=HEADER)
    
    df_AD, df_CU, df_I = build_addresses_countries_institutions_wos(df_corpus=df)
    df_AD.to_csv(Path(out_dir_parsing) / Path('addresses.dat'),
                 index=False,
                 sep='\t',
                 header=HEADER)
    df_CU.to_csv(Path(out_dir_parsing) / Path('countries.dat'),
                 index=False, 
                 sep='\t',
                 header=HEADER)
    df_I.to_csv(Path(out_dir_parsing) / Path('institutions.dat'),
                 index=False, 
                 sep='\t',
                 header=HEADER)
    
    df_S = build_subjects_wos(df_corpus=df)
    df_S.to_csv(Path(out_dir_parsing) / Path('subjects.dat'),
                index=False,
                sep='\t',
                header=HEADER)

    df_S2 = build_sub_subjects_wos(df_corpus=df)
    df_S2.to_csv(Path(out_dir_parsing) / Path('subjects2.dat'),
                index=False,
                sep='\t',
                header=HEADER)
       
    df_A = build_articles_wos(df_corpus=df)
    df_A.to_csv(Path(out_dir_parsing) / Path('articles.dat'),
                index=True,
                sep='\t',
                header=HEADER)
    
    df_R = build_references_wos(df_corpus=df)
    df_R.to_csv(Path(out_dir_parsing) / Path('references.dat'),
                index=False, 
                sep='\t',
                header=HEADER)

def biblio_parser(in_dir_parsing, out_dir_parsing, database, expert, rep_utils):
    
    '''Chooses the appropriate parser to parse wos or scopus databases
    '''
    
    if database == "wos":
        biblio_parser_wos(in_dir_parsing, out_dir_parsing)
    elif database == "scopus":
        biblio_parser_scopus(in_dir_parsing, out_dir_parsing, rep_utils)
    else:
        raise Exception("Sorry, unrecognized database {database} : should be wos or scopus ")
