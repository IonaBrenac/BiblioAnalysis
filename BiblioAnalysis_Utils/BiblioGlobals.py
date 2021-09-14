'''The BiblioGlobals module defines global dicts 
   used in other BiblioAnalysis modules.

'''

__all__ = ['DIC_OUTDIR_PARSING','LABEL_MEANING','COOC_AUTHORIZED_ITEMS','COOC_AUTHORIZED_ITEMS_DICT']

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

LABEL_MEANING = {'AU':'Authors',          # ex: Faure-Vincent J, De Vito E, Simonato J-P
                 'AK':'Authors keywords', # ex: BIOMASS, SOLAR FUEL
                 'CU':'Countries',        # ex: France, United States
                 'DT':'Document types',   # ex: review, article, proceding
                 'I':'Institutions',      # ex: CEA-Liten, CEA/CNRS/IRIG
                 'J':'Journals',          # ex: Conference Paper, Article 
                 'IK':'Journal keywords',
                 'LA':'Languages',        # ex: English, French
                 'R':'References',
                 'RJ':'References journals',
                 'S':'Subjects',          # ex: Chemical Engineering,Engineering 
                 'S2':'Sub-subjects',     # ex: Applied Mathematics, Organic Chemistry
                 'TK':'Title keywords',
                 'Y':'Years'}             # ex: 2019
    
COOC_AUTHORIZED_ITEMS = ['AK','AU','CU','IK','S','S2','TK']
COOC_AUTHORIZED_ITEMS_DICT = {label:name for name,label in LABEL_MEANING.items() 
                                    if name in COOC_AUTHORIZED_ITEMS}

