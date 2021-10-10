'''The BiblioGlobals module defines global dicts 
   used in other BiblioAnalysis modules.

'''

__all__ = ['DIC_OUTDIR_PARSING',
           'DIC_OUTDIR_DESCRIPTION',
           'LABEL_MEANING',
           'NAME_MEANING',
           'VALID_LABEL_GRAPH',
           'COOC_AUTHORIZED_ITEMS',
           'COOC_AUTHORIZED_ITEMS_DICT',
           'COOC_COLOR_NODES',
           'COUPL_AUTHORIZED_ITEMS',
           'COUPL_FILENAME_XLSX',
           'COUPL_FILENAME_GEXF',]

DIC_OUTDIR_PARSING = {'A':'articles.dat',
                      'AU':'authors.dat',
                      'AD':'addresses.dat',
                      'CU':'countries.dat',
                      'I':'institutions.dat',
                      'AK':'authorskeywords.dat',
                      'IK':'journalkeywords.dat',
                      'TK':'titlekeywords.dat',
                      'S':'subjects.dat',
                      'S2':'subjects2.dat',
                      'R':'references.dat',
                      'K':'keywords.dat'
                      }

DIC_OUTDIR_DESCRIPTION = {acronym:'freq_'+file for acronym,file in DIC_OUTDIR_PARSING.items()}

DIC_OUTDIR_DESCRIPTION_ADD = {'DT':'freq_doctypes.dat',
                              'J':'freq_journals.dat',
                              'LA':'freq_languages.dat',
                              'RJ':'freq_refjournals.dat',
                              'Y':'freq_years.dat'}

DIC_OUTDIR_DESCRIPTION = res = {**DIC_OUTDIR_DESCRIPTION, **DIC_OUTDIR_DESCRIPTION_ADD}

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
                 'Y':'Years'}             # ex: 2019
    
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
                'authors':'AU'}

COOC_AUTHORIZED_ITEMS = ['AU','CU','AK','IK','TK','S','S2']

COOC_AUTHORIZED_ITEMS_DICT = {label:name for name,label in LABEL_MEANING.items() 
                                    if name in COOC_AUTHORIZED_ITEMS}

COOC_COLOR_NODES = {
    "Y": "255,255,0",  # default color for gephi display
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

COUPL_AUTHORIZED_ITEMS = ['AU','CU','I','AK','IK','TK','S','S2']

COUPL_FILENAME_XLSX = 'biblio_network.xlsx'

COUPL_FILENAME_GEXF = 'biblio_network.gexf'

# To build a cooccurrence graph only for these labels
VALID_LABEL_GRAPH = ['AU', 'CU', 'S', 'S2', 'IK', 'R', 'RJ', 'I', 'AK', 'TK']
