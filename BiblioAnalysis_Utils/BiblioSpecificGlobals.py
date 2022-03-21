'''The BiblioGlobals module defines global parameters 
   used in other BiblioAnalysis modules.

'''

__all__ = ['BLACKLISTED_WORDS',
           'COL_NAMES',
           'COLUMN_LABEL_SCOPUS',
           'COLUMN_LABEL_WOS',
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
           'DIC_OUTDIR_DESCRIPTION',
           'DIC_OUTDIR_PARSING',
           'DISTRIBS_ITEM_FILE',
           'ENCODING',
           'FIELD_SIZE_LIMIT',
           'FOLDER_NAMES',
           'FOLDER_SELECTION_HELP_TEXT',
           'GUI_BUTTON_RATIO',
           'GUI_TEXT_MAX_LINES_NB',
           'GUI_WIDGET_RATIO',
           'HEADER',
           'INST_FILTER_LIST',
           'LABEL_MEANING',
           'NAME_MEANING',
           'NLTK_VALID_TAG_LIST',
           'NMAX_NODES',
           'NOUN_MINIMUM_OCCURRENCES',
           'NODE_SIZE_REF',
           'RE_ADDRESS',
           'RE_AUTHOR',
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
           'REP_UTILS',
           'SCOPUS_CAT_CODES',
           'SCOPUS_JOURNALS_ISSN_CAT',
           'SIZE_MIN',
           'SYMBOL',
           'USECOLS_SCOPUS',
           'USECOLS_WOS',
           'VALID_LABEL_GRAPH',
          ]

# Standard library imports
import re

#####################
# Globals to be set #
#####################

BLACKLISTED_WORDS = [] #['null','nan'] for title keywords

pub_id = 'Pub_id'

COL_NAMES = {   'address':      [pub_id,
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
                                 'Institution',
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
                                 'Sub_subject']
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

ENCODING = 'iso-8859-1' # encoding used by the function read_database_wos

FIELD_SIZE_LIMIT = 256<<10 # extend maximum field size for wos file reading

FOLDER_NAMES = {'rawdata':     'rawdata',
                'parsing':     'parsing',
                'description': 'freq',
                'filtering':   'filter',
                'coupling':    'coupling',
                'cooccurrence':'cooc',
               }

FOLDER_SELECTION_HELP_TEXT ='''The selected folder is edited.
                               For changing the selection, just make a new selection.
                               If the selection is valid, please close the window'''

GUI_BUTTON_RATIO = 2.5

GUI_TEXT_MAX_LINES_NB = 3

GUI_WIDGET_RATIO = 1.2 

HEADER = True

# Authors affiliations filter (default: None) as a list of tuples (instituion,country)
INST_FILTER_LIST = None 

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

RE_ADDRESS = re.compile('''(?<=\]\s)               # Captures: "xxxxx" in string between "]" and "["  
                        [^;]*                      # or  between "]" and end of string or ";"
                        (?=; | $ )''',re.X)

RE_AUTHOR = re.compile('''(?<=\[)
                      [a-zA-Z,;\s\.\-']*(?=, | \s )
                      [a-zA-Z,;\s\.\-']*
                      (?=\])''',re.X)               # Captures: "xxxx, xxx" or "xxxx xxx" in string between "[" and "]"



RE_REF_AUTHOR_SCOPUS = re.compile('^[^,0123456789:]*,'               # Captures: "ccccc, ccccc,"
                                  '[^,0123456789:]*,') 

RE_REF_AUTHOR_WOS = re.compile('^[^,0123456789:]*,')    # Captures: "ccccc ccccc,"  ; To Do: to be converted to explicite list 

RE_REF_JOURNAL_SCOPUS = re.compile('''\(\d{4}\)\s+[^,]*,       # Capures "(dddd) cccccc," c not a comma
                            |\(\d{4}\)\s+[^,]*$''',re.X)       # or "(dddd) cccccc" at the end

RE_REF_JOURNAL_WOS = re.compile('''(?<=,)\s[A-Z]{2}[0-9A-Z&\s\-\.\[\]]+(?=,)         # Captures ", Science & Dev.[3],"
                           |(?<=,)\s[A-Z]{2}[0-9A-Z&\s\-\.\[\]]+$''',re.X)

RE_REF_PAGE_SCOPUS = re.compile('\s+[p]{1,2}\.\s+[a-zA-Z0-9]{1,9}')  # Captures: "pp. ddd" or "p. ddd"

RE_REF_PAGE_WOS = re.compile(',\s+P\d{1,6}')            # Captures: ", Pdddd"

RE_REF_VOL_SCOPUS = re.compile(''',\s+\d{1,6},                       # Capture: ", dddd,"
                        |,\s+\d{1,6}\s\(                       # or: ", dddd ("
                        |,\s+\d{1,6}$''',re.X)                 # or: ", dddd" at the string end

RE_REF_VOL_WOS = re.compile(',\s+V\d{1,6}')             # Captures: ", Vdddd"

RE_REF_YEAR_SCOPUS = re.compile(r'(?<=\()\d{4}(?=\))')               # Captures: "dddd" within parenthesis

RE_REF_YEAR_WOS = re.compile(',\s\d{4},')               # Captures: ", dddd,"

RE_SUB = re.compile('''[a-z]?Univ[\.a-zé]{0,6}\s    # Captures alias of University
                    |[a-z]?Univ[\.a-zé]{0,6}$''',re.X)

REP_UTILS = 'BiblioAnalysis_RefFiles'

SCOPUS_CAT_CODES = 'scopus_cat_codes.txt'

SCOPUS_JOURNALS_ISSN_CAT = 'scopus_journals_issn_cat.txt' 

SIZE_MIN = 1 # Minimum size of co-occurrence nodes

SYMBOL = '\s,;:.\-\/'

USECOLS_SCOPUS = '''Abstract,Affiliations,Authors,Author Keywords,Authors with affiliations,
       CODEN,Document Type,DOI,EID,Index Keywords,ISBN,ISSN,Issue,Language of Original Document,
       Page start,References,Source title,Title,Volume,Year'''

USECOLS_WOS ='''AB,AU,BP,BS,C1,CR,DE,DI,DT,ID,IS,LA,PY,RP,
                SC,SN,SO,TI,UT,VL,WC'''

# Cooccurrence graph built only for the following labels
VALID_LABEL_GRAPH = ['AU', 'CU', 'S', 'S2', 'IK', 'R', 'RJ', 'I', 'AK', 'TK']  

#################
# Built globals #
#################

COOC_AUTHORIZED_ITEMS_DICT = {label:name for name,label in LABEL_MEANING.items() 
                              if name in COOC_AUTHORIZED_ITEMS}

DIC_OUTDIR_DESCRIPTION = {acronym:'freq_'+file for acronym,file in DIC_OUTDIR_PARSING.items()}

_DIC_OUTDIR_DESCRIPTION_ADD = {'DT':'freq_doctypes.dat',
                              'J':'freq_journals.dat',
                              'LA':'freq_languages.dat',
                              'RJ':'freq_refjournals.dat',
                              'Y':'freq_years.dat',
                              }
DIC_OUTDIR_DESCRIPTION = res = {**DIC_OUTDIR_DESCRIPTION, **_DIC_OUTDIR_DESCRIPTION_ADD}

USECOLS_SCOPUS = [x.strip() for x in USECOLS_SCOPUS.split(',')]

USECOLS_WOS = [x.strip() for x in USECOLS_WOS.split(',')]





    

