__all__ = ['biblio_parser',
           'build_title_keywords',
           'country_normalization',
           'merge_database',
           'name_normalizer',
           ]

# Globals used from .BiblioGeneralGlobals: ALIAS_UK, CHANGE, COUNTRIES,
# Globals used from .BiblioSpecificGlobals: BLACKLISTED_WORDS, INST_FILTER_DIC, 
#                                           NLTK_VALID_TAG_LIST, NOUN_MINIMUM_OCCURRENCES


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
       4- Suppress words pertening to BLACKLISTED_WORDS to the list  from the bag of words
    
    Args:
       df (dataframe): pub_id | Title 
       
    Returns:
       df (dataframe): pub_id | title_token | kept_tokens where title_token is the list of token of the title
         and kept_token the list of tokens with a frequency occurrence >= NOUN_MINIMUM_OCCURRENCES
       bag_of_words_occurrences (list of tuples): [(word_1,# occurrence_1), (word_2,# occurrence_2), ...]
        
    '''

    # Standard library imports
    import operator
    from collections import Counter
       
    # 3rd party imports
    import nltk
    import numpy as np
    
    # Local imports
    from .BiblioSpecificGlobals import NLTK_VALID_TAG_LIST
    from .BiblioSpecificGlobals import NOUN_MINIMUM_OCCURRENCES
    from .BiblioSpecificGlobals import BLACKLISTED_WORDS
    
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

    df['title_token'] = df['Title'].apply(tokenizer)

    bag_of_words = np.array(df.title_token.sum()) # remove the blacklisted words from the bag of words
    for remove in BLACKLISTED_WORDS:
        bag_of_words = bag_of_words[bag_of_words != remove] 

    bag_of_words_occurrences = list(Counter(bag_of_words).items())
    bag_of_words_occurrences.sort(key = operator.itemgetter(1),reverse=True)

    keywords_TK = set([x for x,y in bag_of_words_occurrences if y>=NOUN_MINIMUM_OCCURRENCES])
    
    df['kept_tokens'] = df['title_token'].apply(lambda x :list(keywords_TK.intersection(set(x))))
   
    return df,bag_of_words_occurrences

def country_normalization(country):
    '''
    Normalize the country name for coherence seeking between wos and scopus corpuses.
    '''

    # Local imports
    from .BiblioGeneralGlobals import ALIAS_UK
    from .BiblioGeneralGlobals import COUNTRIES
    
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
    
    # Local imports
    from .BiblioSpecificGlobals import USECOLS_SCOPUS

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
    import functools
    import re
    import unicodedata
    
    # Local imports
    from .BiblioGeneralGlobals import CHANGE

    nfc = functools.partial(unicodedata.normalize,'NFD')
    
    text = text.translate(CHANGE) # Translate special character using global CHANGE dict
    text = nfc(text). \
           encode('ascii', 'ignore'). \
           decode('utf-8').\
           strip()
    
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

def biblio_parser(in_dir_parsing, out_dir_parsing, database, expert, rep_utils, inst_filter_dic=None):
    
    '''Chooses the appropriate parser to parse wos or scopus databases.
    '''
    
    # Local imports
    from .BiblioParsingScopus import biblio_parser_scopus
    from .BiblioParsingWos import biblio_parser_wos
    from .BiblioSpecificGlobals import INST_FILTER_DIC
    
    if inst_filter_dic== None: inst_filter_dic = INST_FILTER_DIC
    
    if database == "wos":
        biblio_parser_wos(in_dir_parsing, out_dir_parsing, inst_filter_dic)
    elif database == "scopus":
        biblio_parser_scopus(in_dir_parsing, out_dir_parsing, rep_utils, inst_filter_dic)
    else:
        raise Exception("Sorry, unrecognized database {database} : should be wos or scopus ")
