'''The BiblioGlobals module defines global parameters 
   used in other BiblioAnalysis modules.

'''

__all__ = ['BLACKLISTED_WORDS',
           'COL_NAMES',
           'COLUMN_LABEL_SCOPUS',
           'COLUMN_LABEL_WOS',
           'CONCATENATED_XLSX',
           'COOC_AUTHORIZED_ITEMS',
           'COOC_AUTHORIZED_ITEMS_DICT',
           'COOC_COLOR_NODES',
           'COOC_NETWORKS_FILE',
           'COOC_HTML_PARAM',
           'COUPL_AUTHORIZED_ITEMS',
           'COUPL_FILENAME_GEXF',
           'COUPL_FILENAME_XLSX',
           'COUPL_GLOBAL_VALUES',
           'COUPL_HTML_PARAM',
           'DEDUPLICATED_XLSX',
           'DIC_DOCTYPE',
           'DIC_AMB_WORDS',
           'DIC_LOW_WORDS',
           'DIC_OUTDIR_DESCRIPTION',
           'DIC_OUTDIR_PARSING',
           'DIC_INST_FILENAME',
           'DIC_TOWN_SYMBOLS',
           'DIC_TOWN_WORDS',
           'DIC_WORD_RE_PATTERN',
           'DISTRIBS_ITEM_FILE',
           'EMPTY',
           'ENCODING',
           'FIELD_SIZE_LIMIT',
           'FOLDER_NAMES',
           'FOLDER_SELECTION_HELP_TEXT',
           'FR_UNIVERSITY_TOWNS',
           'GUI_BUTTON_RATIO',
           'GUI_TEXT_MAX_LINES_NB',
           'GUI_WIDGET_RATIO',
           'HEADER',
           'INST_BASE_LIST',
           'INST_FILTER_LIST',
           'KEEPING_WORDS',
           'LABEL_MEANING',
           'LENGTH_DIFF_THRESHOLD',
           'LENGTH_THRESHOLD',
           'NAME_MEANING',
           'NLTK_VALID_TAG_LIST',
           'NMAX_NODES',
           'NOUN_MINIMUM_OCCURRENCES',
           'NODE_SIZE_REF',
           'PARSING_PERF',
           'RAW_INST_FILENAME',
           'RE_ADDRESS',
           'RE_ADDS_JOURNAL',
           'RE_AUTHOR',
           'RE_NUM_CONF',
           'RE_REF_AUTHOR_SCOPUS',
           'RE_REF_AUTHOR_WOS',
           'RE_REF_JOURNAL_SCOPUS',
           'RE_REF_JOURNAL_WOS',
           'RE_REF_PAGE_SCOPUS',
           'RE_REF_PAGE_WOS',
           'RE_REF_VOL_SCOPUS',
           'RE_REF_VOL_WOS',
           'RE_REF_YEAR_SCOPUS',
           'RE_REF_YEAR_WOS',
           'RE_SUB',
           'RE_SUB_FIRST',
           'RE_YEAR',
           'RE_YEAR_JOURNAL',
           'REP_UTILS',
           'RE_ZIP_CODE',
           'SCOPUS',
           'SCOPUS_CAT_CODES',
           'SCOPUS_JOURNALS_ISSN_CAT',
           'SIMILARITY_THRESHOLD',
           'SIZE_MIN',
           'SYMBOL',
           'UNKNOWN',
           'USECOLS_SCOPUS',
           'USECOLS_WOS',
           'VALID_LABEL_GRAPH',
           'WOS',
          ]

# Standard library imports
import re

#####################
# Globals to be set #
#####################

BLACKLISTED_WORDS = [] #['null','nan'] for title keywords

pub_id = 'Pub_id'

COL_NAMES = {   'pub_id':       pub_id,
                'address':      [pub_id,
                                 'Idx_address',
                                 'Address'],
                'articles':     [pub_id,
                                 'Authors',
                                 'Year',
                                 'Journal',
                                 'Volume',
                                 'Page',
                                 'DOI',
                                 'Document_type',
                                 'Language',
                                 'Title',
                                 'ISSN'],
                'authors':      [pub_id,
                                 'Idx_author',
                                 'Co_author'],  
                'auth_inst':    [pub_id,
                                 'Idx_author',
                                 'Address',
                                 'Country',
                                 'Norm_institutions',
                                 'Raw_institutions',
                                 'Secondary_institutions'
                                 ], 
                'country':      [pub_id,
                                 'Idx_address',
                                 'Country'],
                'institution':  [pub_id,
                                 'Idx_address',
                                 'Institution'],                             
                'keywords':     [pub_id,
                                 'Keyword'],                             
                'references':   [pub_id,
                                 'Author',
                                 'Year',                             
                                 'Journal',
                                 'Volume',
                                 'Page'],
                'subject':      [pub_id,
                                 'Subject'],
                'sub_subject':  [pub_id,
                                 'Sub_subject'],
                'temp_col':     ['Title_LC', 
                                 'Journal_norm',
                                 'Title',
                                 'title_tokens',
                                 'kept_tokens'],             
            }                   
            
COLUMN_LABEL_SCOPUS = {'affiliations': 'Affiliations',
                       'author_keywords': 'Author Keywords',
                       'authors': 'Authors',
                       'authors_with_affiliations': 'Authors with affiliations',
                       'document_type': 'Document Type',
                       'doi': 'DOI',
                       'index_keywords': 'Index Keywords' ,
                       'issn': 'ISSN',
                       'journal': 'Source title',
                       'language': 'Language of Original Document',
                       'page_start': 'Page start' ,
                       'references': 'References' ,
                       'sub_subjects': '',
                       'subjects': '',
                       'title': 'Title' ,
                       'volume': 'Volume',
                       'year': 'Year',
                       }
            
COLUMN_LABEL_WOS = {'affiliations': '',
                    'author_keywords': 'ID',
                    'authors': 'AU',
                    'authors_with_affiliations': 'C1',
                    'document_type': 'DT',
                    'doi': 'DI',
                    'index_keywords': 'DE',
                    'issn': 'SN',
                    'journal': 'SO',
                    'language': 'LA',
                    'page_start': 'BP',
                    'references': 'CR',
                    'sub_subjects': 'SC',
                    'subjects': 'WC',
                    'title': 'TI',
                    'volume': 'VL',
                    'year': 'PY' ,
                    }

CONCATENATED_XLSX = 'articles_concat.xlsx'

COOC_AUTHORIZED_ITEMS = ['AU','CU','AK','IK','TK','S','S2']

COOC_COLOR_NODES = {"Y": "255,255,0",  # default color for gephi display
                    "J": "150,0,150",
                    "AU": "20,50,255",
                    "IK": "255,0,255",
                    "AK": "255,0,255",
                    "TK": "205,0,205",
                    "S": "50,0,150",
                    "S2": "50,0,150",
                    "R": "255,0,0",
                    "RJ": "255,97,0",
                    "I": "0,255,0",
                    "CU": "0,255,255",
                    "LA": "0,180,0",
                    "DT": "0,180,0",
                   }

COOC_HTML_PARAM = {'algo': 'barnes',
                   'height': 1000,
                   'width': 1000,
                   'bgcolor': '#EAEDED',
                   'font_color': 'black',
                  }

COOC_NETWORKS_FILE = 'coocnetworks.json'

COUPL_AUTHORIZED_ITEMS = ['AU','CU','I','AK','IK','TK','S','S2']

COUPL_FILENAME_XLSX = 'biblio_network.xlsx'

COUPL_FILENAME_GEXF = 'biblio_network.gexf'

COUPL_GLOBAL_VALUES = {'BCTHR':  1, # minimum number of shared references 
                                    # for keeping an edge
                       'RTUTHR': 2, # minimum times of use in the corpus
                                    # to count a reference in the 
                                    # shared references
                       'WTHR':   0, # minimum weight to keep a link
                       'NRTHR':  1, # minimum number of references to keep a node
                       }

COUPL_HTML_PARAM = {'background_color': '#EAEDED', #light grey,
                    'font_color': 'black',
                    'edges_color': '#808080',       # gray,
                    'nodes_colors': {0: '#5677fc',  #blue
                                     1: '#3f51b5',  #indigo
                                     2: '#e51c23',  #red
                                     3: '#00bcd4',  #cyan
                                     4: '#259b24',  #green
                                     5: '#ffeb3b',  #yellow
                                     6: '#ff9800',  #orange
                                     7: '#795548',  #brown 
                                     8: '#cddc39',  #lime   # limited number of colored values 
                                     'uncolor': '#e0e0e0',  # grey 300 - for nodes out of colored values
                                     },
                    }

DEDUPLICATED_XLSX = 'articles_dedup.xlsx'

DIC_DOCTYPE = {'Article':              ['Article'],
               'Article; Early Access':['Article; Early Access'], 
               'Conference Paper':     ['Conference Paper','Proceedings Paper'],
               'Data Paper':           ['Data Paper','Article; Data Paper'],
               'Correction':           ['Correction'],
               'Editorial Material':   ['Editorial Material'],               
               'Erratum':              ['Erratum'],
               'Note':                 ['Note'], 
               'Review':               ['Review'],
               'Review; Early Access': ['Review; Early Access']}

DIC_LOW_WORDS = {'proceedings of':         '',
                 'conference record of':   '',
                 'proceedings':            '',
                 'communications':         '',
                 'conference proceedings': '',
                 'ieee':                   '',
                 'international':          'int',
                 'conference':             'conf',
                 'journal of':             'j',
                 'transactions on':        'trans',
                 'science':                'sci',
                 'technology':             'tech',
                 'engineering':            'eng',
                 '&': 'and',                # & to and 
                 ':': ' ',                  # colon to space
                 '-': ' ',                  # hyphen-minus to space
                 ',': ' ',                  # comma to space
                 '(': ' ',                  # parenthese to space
                 ')': ' ',                  # parenthese to space
                 '/': ' ',                  # slash to space
                }

DIC_OUTDIR_PARSING = {'A':'articles.dat',
                      'AU':'authors.dat',
                      'AD':'addresses.dat',
                      'CU':'countries.dat',
                      'I':'institutions.dat',
                      'I2':'authorsinst.dat',
                      'AK':'authorskeywords.dat',
                      'IK':'journalkeywords.dat',
                      'TK':'titlekeywords.dat',
                      'S':'subjects.dat',
                      'S2':'subjects2.dat',
                      'R':'references.dat',
                     }

DISTRIBS_ITEM_FILE = 'DISTRIBS_itemuse.json'

EMPTY = 'empty'

ENCODING = 'iso-8859-1' # encoding used by the function read_database_wos

FIELD_SIZE_LIMIT = 256<<10 # extend maximum field size for wos file reading

FOLDER_NAMES = {'corpus':      'Corpus',
                'concat':      'concatenation',
                'cooccurrence':'cooc',
                'coupling':    'coupling',
                'description': 'freq',
                'dedup':       'deduplication',
                'filtering':   'filter',
                'parsing':     'parsing',
                'rawdata':     'rawdata',
                'scopus':      'scopus',
                'wos':         'wos',
               }

FOLDER_SELECTION_HELP_TEXT ='''The selected folder is edited.
                               For changing the selection, just make a new selection.
                               If the selection is valid, please close the window'''

GUI_BUTTON_RATIO = 2.5

GUI_TEXT_MAX_LINES_NB = 3

GUI_WIDGET_RATIO = 1.2 
 
HEADER = True                                                                                      #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

LABEL_MEANING = {'AU':'Authors',          # ex: Nom1 J, Nom2 E, Nom3 J-P
                 'CU':'Countries',        # ex: France, United States
                 'I':'Institutions',      # ex: Acronyme1, Acronyme2
                 'DT':'Document types',   # ex: Review, Article, Proceeding
                 'J':'Journals',          
                 'AK':'Authors keywords', # ex: BIOMASS, SOLAR FUEL
                 'IK':'Journal keywords',
                 'TK':'Title keywords',
                 'S':'Subjects',          # ex: Chemical Engineering,Engineering 
                 'S2':'Sub-subjects',     # ex: Applied Mathematics, Organic Chemistry     
                 'R':'References',
                 'RJ':'References journals',
                 'LA':'Languages',        # ex: English, French
                 'Y':'Years',             # ex: 2019
                } 

LENGTH_DIFF_THRESHOLD = 10                # unused

LENGTH_THRESHOLD = 30

NAME_MEANING = {'years': 'Y',
                'languages': 'LA',
                'doctypes': 'DT',
                'countries': 'CU',
                'institutions': 'I',
                'journals': 'J',
                'references': 'R',
                'refjournals': 'RJ',
                'subjects': 'S',
                'subjects2': 'S2',
                'journalkeywords': 'IK',
                'titlekeywords': 'TK',
                'authorskeywords': 'AK',
                'authors':'AU',
               }

NLTK_VALID_TAG_LIST = ['NN','NNS','VBG','JJ'] # you can find help on the nltk tags set
                                              # using nltk.help.upenn_tagset() 
    
NMAX_NODES = 100 # maximum number of nodes to keep in corpus description    

NOUN_MINIMUM_OCCURRENCES = 3 # Minimum occurrences of a noun to be retained when 
                             # building the set of title keywords see build_title_keywords
    
NODE_SIZE_REF = 30

PARSING_PERF = 'failed.json'

RE_ADDRESS = re.compile('''(?<=\]\s)               # Captures: "xxxxx" in string between "]" and "["  
                        [^;]*                      # or  between "]" and end of string or ";"
                        (?=; | $ )''',re.X)

RE_ADDS_JOURNAL = re.compile(r'\([^\)]+\)')        # Captures string between "()" in journal name   (unused)

RE_AUTHOR = re.compile('''(?<=\[)
                      [a-zA-Z,;\s\.\-']*(?=, | \s )
                      [a-zA-Z,;\s\.\-']*
                      (?=\])''',re.X)               # Captures: "xxxx, xxx" or "xxxx xxx" in string between "[" and "]"

RE_NUM_CONF = re.compile(r'\s\d+th\s|\s\d+nd\s')    # Captures: " d...dth " or " d...dnd " in string

RE_REF_AUTHOR_SCOPUS = re.compile(r'^[^,0123456789:]*,'               # Captures: "ccccc, ccccc,"
                                  '[^,0123456789:]*,') 

RE_REF_AUTHOR_WOS = re.compile(r'^[^,0123456789:]*,')    # Captures: "ccccc ccccc,"  ; To Do: to be converted to explicite list 

RE_REF_JOURNAL_SCOPUS = re.compile('''\(\d{4}\)\s+[^,]*,       # Capures "(dddd) cccccc," c not a comma
                            |\(\d{4}\)\s+[^,]*$''',re.X)       # or "(dddd) cccccc" at the end

RE_REF_JOURNAL_WOS = re.compile('''(?<=,)\s[A-Z]{2}[0-9A-Z&\s\-\.\[\]]+(?=,)         # Captures ", Science & Dev.[3],"
                           |(?<=,)\s[A-Z]{2}[0-9A-Z&\s\-\.\[\]]+$''',re.X)

RE_REF_PAGE_SCOPUS = re.compile(r'\s+[p]{1,2}\.\s+[a-zA-Z0-9]{1,9}')  # Captures: "pp. ddd" or "p. ddd"

RE_REF_PAGE_WOS = re.compile(r',\s+P\d{1,6}')            # Captures: ", Pdddd"

RE_REF_VOL_SCOPUS = re.compile(''',\s+\d{1,6},                       # Capture: ", dddd,"
                        |,\s+\d{1,6}\s\(                       # or: ", dddd ("
                        |,\s+\d{1,6}$''',re.X)                 # or: ", dddd" at the string end

RE_REF_VOL_WOS = re.compile(r',\s+V\d{1,6}')             # Captures: ", Vdddd"

RE_REF_YEAR_SCOPUS = re.compile(r'(?<=\()\d{4}(?=\))')  # Captures: "dddd" within parenthesis in scopus references

RE_REF_YEAR_WOS = re.compile(r',\s\d{4},')               # Captures: ", dddd," in wos references

RE_SUB = re.compile('''[a-z]?Univ[\.a-zé]{0,6}\s        # Captures alias of University surrounded by texts
                    |[a-z]?Univ[\.a-zé]{0,6}$''',re.X)

RE_SUB_FIRST = re.compile('''[a-z]?Univ[,]\s ''',re.X)       # Captures alias of University before a coma

RE_YEAR = re.compile(r'\d{4}')                            # Captures "dddd" as the string giving the year

RE_YEAR_JOURNAL = re.compile(r'\s\d{4}\s')               # Captures " dddd " as the year in journal name

REP_UTILS = 'BiblioAnalysis_RefFiles'

RE_ZIP_CODE = re.compile(',\s[a-zA-Z]?[\-]?\d+.*',)     # Captures text begining with ', '                                        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                                        # and that possibly contains letters and hyphen-minus

# Scopus database name
SCOPUS = 'scopus'

SCOPUS_CAT_CODES = 'scopus_cat_codes.txt'

SCOPUS_JOURNALS_ISSN_CAT = 'scopus_journals_issn_cat.txt'

SIMILARITY_THRESHOLD = 80

SIZE_MIN = 1 # Minimum size of co-occurrence nodes

SYMBOL = '\s,;:.\-\/'

UNKNOWN = 'unknown'

# Cooccurrence graph built only for the following labels
VALID_LABEL_GRAPH = ['AU', 'CU', 'S', 'S2', 'IK', 'R', 'RJ', 'I', 'AK', 'TK'] 

# WOS database name
WOS = 'wos'

#################
# Built globals #
#################

COOC_AUTHORIZED_ITEMS_DICT = {label:name for name,label in LABEL_MEANING.items() 
                              if name in COOC_AUTHORIZED_ITEMS}

_DIC_OUTDIR_DESCRIPTION = {acronym:'freq_'+file for acronym,file in DIC_OUTDIR_PARSING.items()}

_DIC_OUTDIR_DESCRIPTION_ADD = {'DT':'freq_doctypes.dat',
                              'J':'freq_journals.dat',
                              'LA':'freq_languages.dat',
                              'RJ':'freq_refjournals.dat',
                              'Y':'freq_years.dat',
                              }
DIC_OUTDIR_DESCRIPTION = res = {**_DIC_OUTDIR_DESCRIPTION, **_DIC_OUTDIR_DESCRIPTION_ADD}

# This global is used in merge_database function
_USECOLS_SCOPUS = '''Abstract,Affiliations,Authors,Author Keywords,Authors with affiliations,
       CODEN,Document Type,DOI,EID,Index Keywords,ISBN,ISSN,Issue,Language of Original Document,
       Page start,References,Source title,Title,Volume,Year'''
USECOLS_SCOPUS = [x.strip() for x in _USECOLS_SCOPUS.split(',')]

# To Do: Check if this global is still used
_USECOLS_WOS ='''AB,AU,BP,BS,C1,CR,DE,DI,DT,ID,IS,LA,PY,RP,
                SC,SN,SO,TI,UT,VL,WC'''
USECOLS_WOS = [x.strip() for x in _USECOLS_WOS.split(',')]


#############################################
# Specific globals for institutions parsing #
#############################################

# Standard library imports
import re

# Local imports 
from BiblioAnalysis_Utils.BiblioParsingUtils import special_symbol_remove
from BiblioAnalysis_Utils.BiblioParsingUtils import town_names_uniformization

# For replacing symbols in town names
DIC_TOWN_SYMBOLS = {"-": " ",
                     }

# For replacing names in town names
DIC_TOWN_WORDS = {" lez ":  " les ",
                   "saint ": "st ",
                   } 

# For replacing aliases of a word by a word (case sensitive)
DIC_WORD_RE_PATTERN = {}
DIC_WORD_RE_PATTERN['University'] = re.compile(r'\bUniv[aàädeéirstyz]{0,8}\b\.?')
DIC_WORD_RE_PATTERN['Laboratory'] = re.compile(r"'?\bLab\b\.?" \
                                                    +  "|" \
                                                    + r"'?\bLabor[aeimorstuy]{0,7}\b\.?")
DIC_WORD_RE_PATTERN['Center'] = re.compile(r"\b[CZ]ent[erum]{1,3}\b\.?")
DIC_WORD_RE_PATTERN['Department'] = re.compile(r"\bD[eé]{1}p[artemnot]{0,9}\b\.?")
DIC_WORD_RE_PATTERN['Institute'] = re.compile(r"\bInst[ituteosky]{0,7}\b\.?")
DIC_WORD_RE_PATTERN['Faculty'] = re.compile(r"\bFac[lutey]{0,4}\b\.?")
DIC_WORD_RE_PATTERN['School'] = re.compile(r"\bSch[ol]{0,3}\b\.?")


# For keeping chunks of addresses (without accents and in lower case)
    # Setting a list of keeping words
        # Setting a basic list of keeping words
_BASIC_KEEPING_WORDS = list(DIC_WORD_RE_PATTERN.keys())
        # Setting a user list of keeping words
_USER_KEEPING_WORDS = ['Beamline', 'CEA', 'CNRS', 'EA', 'ED', 'FR', 'IMEC', 'INES', 'IRCELYON',\
                      'LEPMI', 'LITEN', 'LOCIE', 'STMicroelectronics', 'TNO', 'ULR', 'UMR', 'VTT']
_KEEPING_WORDS = _BASIC_KEEPING_WORDS + _USER_KEEPING_WORDS
        # Removing accents keeping non adcii characters and converting to lower case the keeping words, by default
KEEPING_WORDS =[special_symbol_remove(x, only_ascii = False, strip = False).lower() for x in _KEEPING_WORDS]


# For droping chunks of addresses (without accents and in lower case)
    # Setting a list of droping suffixes
_DROPING_SUFFIX = ["platz", "strae", "strasse", "straße", "vej"] # added "ring" but drops chunks containing "Engineering"
        # Removing accents keeping non adcii characters and converting to lower case the droping suffixes, by default
DROPING_SUFFIX = [special_symbol_remove(x, only_ascii = False, strip = False).lower() for x in _DROPING_SUFFIX]

    # Setting a list of droping words
_DROPING_WORDS = ["allee", "av", "avda", "avenue", "bat", "batiment", "boulevard", "blv.", "box", "bp", "calle", 
                 "campus", "carrera", "cedex", "cesta", "chemin", "ch.", "city", "ciudad", "cours", "cs", "district", 
                 "lane", "mall", "no.", "po", "p.", "rd", "route", "rue", "road", "sec.", "st.", "strada",
                 "street", "str.", "via", "viale"]
        # Removing accents keeping non adcii characters and converting to lower case the droping words, by default
_DROPING_WORDS = [special_symbol_remove(x, only_ascii = False, strip = False).lower() for x in _DROPING_WORDS]
        # Escaping the regex meta-character "." from the droping words, by default
DROPING_WORDS = [x.replace(".", r"\.") for x in _DROPING_WORDS]


# For droping towns in addresses 
    # Setting string listing raw french-town names 
_FR_UNIVERSITY_TOWNS = '''Aix-Marseille,Aix-en-Provence,Amiens,Angers,Arras,Avignon,
                         Besançon,Bordeaux,Brest,Caen,Chambéry,Clermont-Ferrand,Dijon,
                         Gif-sur-Yvette,Grenoble,La Rochelle,Le Bourget-du-Lac,
                         Le Havre,Le Mans,Lille,Limoges,Lyon,Marseille,Metz,Montpellier,Mulhouse,
                         Nancy,Nantes,Nice,Nîmes,Orléans,Paris,Pau,Perpignan,Pointe-à-Pitre,
                         Poitiers,Reims,Rennes,Rouen,Saint-Denis de La Réunion,Saint-Étienne,
                         Saint-Paul-lez-Durance,Strasbourg,Toulon,Toulouse,Tours,Troyes,Valenciennes'''

    # Converting to lower case
_FR_UNIVERSITY_TOWNS = _FR_UNIVERSITY_TOWNS.lower() 

    # Uniformizing town names 
_FR_UNIVERSITY_TOWNS = town_names_uniformization(_FR_UNIVERSITY_TOWNS)

    # Removing accents keeping non adcii characters
_FR_UNIVERSITY_TOWNS = special_symbol_remove(_FR_UNIVERSITY_TOWNS, only_ascii = False, strip = False)

    # Converting to list of lower-case stripped names of towns 
FR_UNIVERSITY_TOWNS = [x.strip() for x in _FR_UNIVERSITY_TOWNS.split(',')]


# Use to be checked

# Potentialy ambiguous words in institutions names
DIC_AMB_WORDS = {' des ': ' ', # Conflict with DES institution
                 ' @ ': ' ', # Management conflict with '@' between texts
                }

DIC_INST_FILENAME = 'Inst_dic.csv'

INST_BASE_LIST = ['UMR', 'CNRS', 'University']                                                     #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Authors affiliations filter (default: None) as a list of tuples (instituion,country)
INST_FILTER_LIST = [('LITEN','France'),('INES','France')]

RAW_INST_FILENAME = 'Raw_inst.csv'
    

