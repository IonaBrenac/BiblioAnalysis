__all__ = ['address_inst_full_list',        #
           'affiliation_uniformization',     #
           'build_institutions_dic',        #
           'extend_author_institutions',    #
           'getting_secondary_inst_list',   #
           'saving_raw_institutions',       #
           'setting_secondary_inst_filter', #
           ]


# Globals used from BiblioAnalysis_Utils.BiblioGeneralGlobals:  DASHES_CHANGE, SYMB_CHANGE,
#                                                                                                                                
# Globals used from BiblioAnalysis_Utils.BiblioSpecificGlobals: COL_NAMES, DIC_AMB_WORDS,
#                                                               DIC_INST_FILENAME, DIC_OUTDIR_PARSING , 
#                                                               EMPTY, INST_BASE_LIST,            
#                                                               INST_FILTER_LIST, RAW_INST_FILENAME, REP_UTILS, 
#                                                               RE_SUB, RE_SUB_FIRST, RE_ZIP_CODE,                                                               


# Functions used from BiblioAnalysis_Utils.BiblioGui: Select_multi_items
# Functions used from BiblioAnalysis_Utils.BiblioParsingUtils: country_normalization
#                                                              special_symbol_remove


def address_inst_full_list(full_address, inst_dic):

    '''The `address_inst_full_list` function allows building the affiliations list of a full address
    using the internal function `_check_institute`of `BiblioParsingUtils` module
    
    Args:
       full_address (str): the full address to be parsed in institutions and country.
       inst_dic (dict): a dict used for the normalization of the institutions names, 
                        with the raw names as keys and the normalized names as values.
        
    Returns:
        (namedtuple): tuple of two strings. 
                      - The first is the joined list of normalized institutions names 
                      found in the full address.
                      - The second is the joined list of raw institutions names of the full address 
                      with no fully corresponding normalized names.
        
    Notes:
        The globals 'RE_ZIP_CODE' and 'EMPTY' are imported from `BiblioSpecificGlobals` module 
        of `BiblioAnalysis_Utils` package.
        The function `country_normalization` is imported from `BiblioParsingUtils` module
        of `BiblioAnalysis_utils` package.
        
    '''
    
    # Standard library imports
    import re
    from collections import namedtuple
    from string import Template

    # 3rd party imports
    import pandas as pd
    from fuzzywuzzy import process
    
    # Local imports
    from BiblioAnalysis_Utils.BiblioParsingUtils import country_normalization
    from BiblioAnalysis_Utils.BiblioSpecificGlobals import INST_BASE_LIST
    from BiblioAnalysis_Utils.BiblioSpecificGlobals import RE_ZIP_CODE
    from BiblioAnalysis_Utils.BiblioSpecificGlobals import EMPTY

    inst_full_list_ntup = namedtuple('inst_full_list_ntup',['norm_inst_list','raw_inst_list'])
    
    country_raw = full_address.split(",")[-1].strip()
    country = country_normalization(country_raw)
    add_country = "_" + country
    
    if RE_ZIP_CODE.findall(full_address):
        address_to_keep = re.sub(RE_ZIP_CODE,"",full_address) + ","
    else:
        address_to_keep = ", ".join(full_address.split(",")[:-1])    
    address_to_keep = address_to_keep.lower()
    
    # Building the list of normalized institutions which raw institutions are found in 'address_to_keep' 
    # and building the corresponding list of raw institutions found in 'address_to_keep'
    norm_inst_full_list = [] 
    raw_inst_found_list = []
    for raw_inst, norm_inst in inst_dic.items():        
        raw_inst_lower = raw_inst.lower()
        raw_inst_split = raw_inst_lower.split()                     
        if _check_institute(address_to_keep,raw_inst_split):            
            norm_inst_full_list.append(norm_inst + add_country)            
            raw_inst_found_list.append(raw_inst_lower)

    # Cleaning 'raw_inst_found_list' from partial institution names
    for inst_base in INST_BASE_LIST:
        if (inst_base.lower() in raw_inst_found_list) and (inst_base.lower()+"," not in address_to_keep) : 
            raw_inst_found_list.remove(inst_base.lower())
    for raw_inst_found in raw_inst_found_list:
        other_raw_inst_found_list = raw_inst_found_list.copy()
        other_raw_inst_found_list.remove(raw_inst_found)        
        for other_raw_inst_found in other_raw_inst_found_list:
            if raw_inst_found in other_raw_inst_found:
                raw_inst_found_list = other_raw_inst_found_list

    # Removing 'raw_inst_found_list' items from 'address_to_keep'             
    for raw_inst_found in raw_inst_found_list:            
        if raw_inst_found in address_to_keep: 
            address_to_keep = address_to_keep.replace(raw_inst_found,"")  
            address_to_keep = ", ".join(x.strip() for x in address_to_keep.split(","))

    while (address_to_keep and address_to_keep[0] == "-"): address_to_keep = address_to_keep[1:]
    address_to_keep = address_to_keep.replace("-", " ")
    address_to_keep = " ".join(x.strip() for x in address_to_keep.split(" ") if x!="")       
            
    # # Building the list of raw institutions remaning in 'address_to_keep'
    raw_inst_full_list = [x.strip() + add_country for x in address_to_keep.split(",") if (x!="" and x!=" ")]

    # Building a string from the final list of raw institutions  
    if raw_inst_full_list:
        raw_inst_full_list_str = ";".join(raw_inst_full_list)       
    else:
        raw_inst_full_list_str = EMPTY 
    
    # Building a string from the final list of normalized institutions without duplicates
    norm_inst_full_list = list(set(norm_inst_full_list))
    if norm_inst_full_list:
        norm_inst_full_list_str = ";".join(norm_inst_full_list)
    else:
        norm_inst_full_list_str = EMPTY 
    
    # Setting the namedtuple to return
    inst_full_list_tup =  inst_full_list_ntup(norm_inst_full_list_str,raw_inst_full_list_str) 
    
    return inst_full_list_tup


def affiliation_uniformization(affiliation_raw):    # A refondre profondément
    
    '''The `affiliation_uniformization' function aims at getting rid 
    of heterogeneous typing of affilations. 
    It first replaces particular characters by standard ones 
    using 'DASHES_CHANGE' and 'SYMB_CHANGE' globals.
    Then, it substitutes by 'University' its aliases using specific 
    regular expressions set in 'RE_SUB',and 'RE_SUB_FIRST' globals.
    Finally, it removes accents using `special_symbol_remove` function.
    
    Args:
        affiliation_raw (str): the raw affiliation to be normalized.

    Returns:
        (str): the normalized affiliation.
        
    Notes:
        The globals 'DASHES_CHANGE' and 'SYMB_CHANGE' are imported
        from `BiblioGeneralGlobals` module of `BiblioAnalysis_Utils` package.
        The globals 'RE_SUB',and 'RE_SUB_FIRST' are imported
        from `BiblioSpecificGlobals` module of `BiblioAnalysis_Utils` package.
        The function `special_symbol_remove` is used from `BiblioParsingUtils` 
        of `BiblioAnalysis_utils` package.
        
    '''
    
    # Standard library imports
    import re
    
    # Local imports
    from BiblioAnalysis_Utils.BiblioParsingUtils import special_symbol_remove
    from BiblioAnalysis_Utils.BiblioGeneralGlobals import DASHES_CHANGE
    from BiblioAnalysis_Utils.BiblioGeneralGlobals import SYMB_CHANGE
    from BiblioAnalysis_Utils.BiblioSpecificGlobals import DIC_AMB_WORDS
    from BiblioAnalysis_Utils.BiblioSpecificGlobals import RE_SUB
    from BiblioAnalysis_Utils.BiblioSpecificGlobals import RE_SUB_FIRST
    
    def _normalize_amb_words(text): 
        for amb_word in DIC_AMB_WORDS.keys():
            text = text.replace(amb_word, DIC_AMB_WORDS[amb_word]).strip()
        text = " ".join(text.split())
        return text
    
    affiliation_raw = _normalize_amb_words(affiliation_raw)
    affiliation_raw = affiliation_raw.translate(DASHES_CHANGE)
    affiliation_raw = affiliation_raw.translate(SYMB_CHANGE)
    affiliation_raw = re.sub(RE_SUB_FIRST,'University' + ', ',affiliation_raw)
    affiliation_raw = re.sub(RE_SUB,'University' + ' ',affiliation_raw)
    affiliation = special_symbol_remove(affiliation_raw, only_ascii=True, skip=True)
    
    return affiliation


def build_institutions_dic(rep_utils = None, dic_inst_filename = None):
    
    '''The `builds_institutions_dic` fuction builds the dict 'inst_dic' 
    giving the mormalized names of institutions from a csv file `dic_inst_filename`.
    The name of the csv file is set in the `DIC_INST_FILENAME` global.
    
    Args: 
        rep_utils (str): name of the folder where the csv file is stored
        dic_inst_filename (str): name of the csv file.        
    
    Returns:       
        `dict`: `inst_dic` as {raw_inst:norm_inst} where 
                - raw_inst a raw institution name 
                - norm_inst is the normalized institution name.
        
    Note:
        The globals `DIC_INST_FILENAME` and `REP_UTILS` from `BiblioSpecificGlobals` module
        of `BiblioAnalysis_utils` package are used.
    
    '''
    
    # Standard library imports
    from pathlib import Path
    
    # 3rd party imports
    import pandas as pd
    
    # Local imports
    from BiblioAnalysis_Utils.BiblioSpecificGlobals  import DIC_INST_FILENAME
    from BiblioAnalysis_Utils.BiblioSpecificGlobals import REP_UTILS    
    
    if dic_inst_filename == None: dic_inst_filename = DIC_INST_FILENAME
    if rep_utils == None: rep_utils = REP_UTILS 
    
    # Setting the file path for dic_inst_filename file reading    
    path_dic_inst = Path(__file__).parent / rep_utils / Path(dic_inst_filename)
    
    # Reading and cleaning the dic_inst_filename file
    inst_dic = pd.read_csv(path_dic_inst,sep=':',header=None,encoding='latin1')
    inst_dic.sort_values([0],inplace=True)
    inst_dic[0] = inst_dic[0].str.strip()
    inst_dic[1] = inst_dic[1].str.strip()
    inst_dic = dict(zip(inst_dic[0],inst_dic[1]))
    
    return inst_dic


def _check_institute(address,raw_inst_split):

    '''The funstion `_check_institute` checks if all the words contained in the list 'raw_inst_split'
    are part of the string 'address'.
    
    A word is defined as a string beginning and ending with a letter.
    For instance, 'cea-leti' or 'Laue-Langevin' are words but not 'Kern-' or '&aaZ)'.
    
    The regexp used is based on the following rules:
        - Alphanumerical (AM) characters are {a…z,A…Z,0…9,_}.
        - Non-alphanumerical (NAM) characters are all other characters.
        - '\b' detects transition between NAM and AM such as '@a', '<space>a', 'a-', '(a', 'a.', etc.
        - '\B' detects transition between AM and AM such as '1a', 'za', 'a_', '_a', etc.
    
    Matches are found between a word 'WORD' of the list `raw_inst_split` and a substring 'WORDS'
    of the string 'address' in 4 cases:

        - 'WORD' matches in '...dWORD' or '...dWORDd...' by the regexp "'\d+\BWORD\B\d+'". 
        ex: 'UMR' matches in 'a6UMR7040.' '@6UMR' or 'matches in '...*WORDd*...'', etc. 
                  doesn't match in 'aUMR', '6UMR-CNRS', '6@UMR7040', etc.

        - 'WORD' matches '...dWORD*...'  by the regexp "'\d+\BWORD\b'".  
        ex: 'UMR' matches in 'a6UMR-CNRS', etc.
                  doesn't match in '@6UMRCNRS', '@UMR-CNRS', etc.

        - 'WORD' matches in '...*WORD*...' by the regexp "'\bWORD\b'". 
        ex: 'UMR' matches in '(UMR7040)', '@UMR-CNRS', etc. where 'UMR'is in between NAM
                  doesn't match in 'UMR7040', '@6UMR_CNRS', etc, where an NAM at least misses around it.

        - 'WORD' matches in '...*WORDd...', by the regexp "'\bWORD\B\d+'"
        ex UMR = %(UMR43)+#
        ex: 'UMR' matches in '6@UMR7040', 'CNRS-UMR7040', etc.
                  doesn't match in 'CNRS_UMR7040', '#UMR_CNRS', etc.

    where '...' stands for any characters, 'd' stands for a digit and '*' stands for an NAM character. 
    
    The match is case insensitive.
    
    According the mentionned 4 rules an isolated '&' such as in 'Art & Metiers' 
    and words ending by a minus (ex: Kern-) are not catched. 
    A specific pretreatment of `raw_inst_split` and `address` should be done before calling this function.
    
    Examples:
        - _check_institute(['den'],'dept. of energy conversion, university of denmark,') is False.
        - _check_institute(['den','dept'],'DEN dept. of energy conversion, university of denmark,') is True.
    
    Args:
        address (str): the address where to check the matching of words.
        raw_inst_split (list): list of words to be found to match in the string 'address'.
    
    Returns:
        (boolean): 'True' for a full match.
                   'False' otherwise.
    '''
    # Standard library imports
    import re
    from string import Template
    
    raw_inst_split = list(set(raw_inst_split))
    
    # Taking care of the potential isolated special characters '&' and '-'   
    raw_inst_split = [x.replace("&","and") for x in raw_inst_split]    
    raw_inst_split_init = raw_inst_split.copy()

    # Removing small words
    small_words_list = ['a','et','de','and','for','of','the']
    for word in small_words_list:
        if word in raw_inst_split_init:
            raw_inst_split.remove(word)
    
    raw_inst_split_init = raw_inst_split.copy()
    for word in raw_inst_split_init:
        if len(word)==1:
            raw_inst_split.remove(word)
    
    # Adding \ to escape regexp reserved char
    for char in ["$",'(',')','[',']','^','-']: 
        escaped_char = '\\'+ char
        raw_inst_split = [x.replace(char,escaped_char) for x in raw_inst_split]
        
    items_number = len(raw_inst_split)

    # Building the 're_inst' regexp searching for 'raw_inst_split' items in 'address' 
    dic = {"inst"+str(i):inst for i,inst in enumerate(raw_inst_split)}

    template_inst = Template(r'|'.join([r'\d+\B$inst'+ str(i) + r'\B\d+'
                                      + '|'
                                      + r'\d+\B$inst' + str(i) + r'\b'
                                      + '|'
                                      + r'\b$inst' + str(i) + r'\b'
                                      + '|'
                                      + r'\b$inst' + str(i) + r'\B\d+'
                                      for i in range(items_number)]))

    re_inst = re.compile(template_inst.substitute(dic), re.IGNORECASE)

    # Checking mach of 'raw_inst_split' items in 'address' using 're_inst' regexp
    items_set = set(re_inst.findall(address))
    if  len(items_set) == items_number:
        return True
    else:
        return False


def extend_author_institutions(in_dir,inst_filter_list):
    ''' The `extend_author_institutions` function extends the .dat file of authors with institutions 
    initialy obtained by the parsing of the corpus, with complementary information about institutions
    selected by the user.
    
    Args:
        in_dir (path): path to the .dat file of authors with institutions.
        inst_filter_list (list): the affiliations filter list of tuples (institution, country). 

    Retruns:
        None
        
    Notes:
        The globals 'COL_NAMES' and 'DIC_OUTDIR_PARSING' from `BiblioSpecificGlobals` module 
        of `BiblioAnalysis_Utils` package are used.
    
    '''
    
    # Standard library imports
    from pathlib import Path
    
    # 3rd party imports
    import pandas as pd
    
    # Local imports
    from BiblioAnalysis_Utils.BiblioSpecificGlobals import COL_NAMES
    from BiblioAnalysis_Utils.BiblioSpecificGlobals import DIC_OUTDIR_PARSING
    
    def _address_inst_list(inst_names_list,institutions):

        secondary_institutions = []
        for inst in inst_names_list:
            if inst in institutions:
                secondary_institutions.append(1)
            else:
                secondary_institutions.append(0)  
             
        return secondary_institutions
    
    institutions_alias = COL_NAMES['auth_inst'][4]
    sec_institutions_alias = COL_NAMES['auth_inst'][5]
    
    # Setting the key for the name of the '.dat' file of authors with institutions 
    # obtained by parsing the corpus
    item = 'I2' 
    
    # Reading the '.dat' file                   
    read_usecols = [COL_NAMES['auth_inst'][x] for x in [0,1,2,3,4]]     
    df_I2= pd.read_csv(in_dir / Path(DIC_OUTDIR_PARSING[item]),
                     sep='\t',
                     usecols=read_usecols)
    
    # Setting an institution name for each of the institutions indicated in the institutions filter
    inst_names_list = [f'{x[0]}_{x[1]}' for x in inst_filter_list]   
    
    # Building the "sec_institution_alias" column in the 'df_I2' dataframe using "inst_filter_list"
    df_I2[sec_institutions_alias] = df_I2.apply(lambda row:
                                             _address_inst_list(inst_names_list,row[institutions_alias]),
                                             axis = 1)

    # Distributing in a 'df_inst_split' df the value lists of 'df_I2[sec_institutions_alias]' column  
    # into columns which names are in 'inst_names_list' list     
    df_inst_split = pd.DataFrame(df_I2[sec_institutions_alias].sort_index().to_list(),
                                          columns=inst_names_list)
    
    # Extending the 'df' dataframe with 'df_inst_split' dataframe
    df_I2 = pd.concat([df_I2, df_inst_split], axis=1)

    # Droping the 'df[sec_institutions_alias]' column which is no more usefull
    df_I2.drop([sec_institutions_alias], axis=1, inplace=True)
    
    # Saving the extended 'df_I2' dataframe in the same '.dat' file 
    df_I2.to_csv(in_dir/ Path(DIC_OUTDIR_PARSING[item]), 
                 index=False,
                 sep='\t') 


def getting_secondary_inst_list(out_dir_parsing):
    '''The `getting_secondary_inst_list` function provides the list of institutions of the corpus.
   
    Args:
        out_dir_parsing (path): the corpus parsing path for reading the "DIC_OUTDIR_PARSING['I2']" file 
                                that lists the authors with their institutions for each article.
       
    Returns:
        (list): list of strings 'country:institution'
       
    Notes:
        The globals 'COL_NAMES'and 'DIC_OUTDIR_PARSING' from `BiblioSpecificGlobals` module 
        of `BiblioAnalysis_Utils` package are used.       
    '''
   
    # Standard library imports
    from pathlib import Path
   
    # 3rd party imports
    import numpy as np
    import pandas as pd
   
    # Local imports
    from BiblioAnalysis_Utils.BiblioSpecificGlobals import COL_NAMES
    from BiblioAnalysis_Utils.BiblioSpecificGlobals import DIC_OUTDIR_PARSING
   
    
    institutions_alias = COL_NAMES['auth_inst'][4]
    country_alias = COL_NAMES['country'][2]   
    
    df_auth_inst = pd.read_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING['I2']),
                                sep = '\t')
    raw_institutions_list = []
    for auth_inst in df_auth_inst[institutions_alias]:
        raw_institutions_list.append(auth_inst.strip())
       
    institutions_list = list(np.concatenate([raw_inst.split(';') for raw_inst in raw_institutions_list]))
    institutions_list  = sorted(list(set(institutions_list)))
 
    country_institution_list = [x.split('_')[1] + ':' + x.split('_')[0] for x in institutions_list]
    country_institution_list = sorted(country_institution_list)
   
    return country_institution_list


def saving_raw_institutions(df_I2,out_dir):
    '''The `saving_raw_institutions`function allows to save the list of raw institutions of a corpus.
    The raw institutions are the ones that have not been complitly replaced by the normalized names 
    of institutions given in a specific file.
    
    Args:
        df_I2 (dataframe): a dataframe resulting from the corpus parsing containing the raw-institutions column.
        out_dir (str): a string for setting the the folder where the file of raw institutions is saved
                       as a csv file which name is given by the global `RAW_INST_FILENAME`.
    
    Returns:
    
    Note:
        The globals `COL_NAMES`and `RAW_INST_FILENAME` are imported from `BiblioSpecificGlobals` module 
        of `BiblioAnalysis_Utils` package.
    
    '''
    # Standard libraries import
    from pathlib import Path

    # 3rd party imports
    import pandas as pd

    # Local imports
    from BiblioAnalysis_Utils.BiblioSpecificGlobals import COL_NAMES
    from BiblioAnalysis_Utils.BiblioSpecificGlobals import RAW_INST_FILENAME
    
    raw_institutions_alias = COL_NAMES['auth_inst'][5]
    raw_institutions_authors_lists = df_I2[raw_institutions_alias].to_list()

    raw_institutions_full_lists = [x.split(';') for x in raw_institutions_authors_lists]

    raw_institutions_full_list = []
    [raw_institutions_full_list.extend(x) for x in raw_institutions_full_lists]

    raw_institutions_full_list = list(set(raw_institutions_full_list))
    raw_institutions_full_list.sort()

    df_raw_inst = pd.DataFrame(raw_institutions_full_list, columns = [raw_institutions_alias])
    df_raw_inst.to_csv(Path(out_dir) / Path(RAW_INST_FILENAME),
                       index=False,
                       sep='\t')

    
def setting_secondary_inst_filter(out_dir_parsing):
    
    '''The `setting_secondary_inst_filter` function allows building the affiliation filter "inst_filter_list"
    from the institutions list of the corpus using the `Select_multi_items` GUI.
    
    Args:
        out_dir_parsing (path): the corpus parsing path for reading the "DIC_OUTDIR_PARSING['I2']" file.
        
    Returns:
        (list): list of tuples (institution,country) selected by the user.
        
    Notes:
        The globals 'COL_NAMES' and 'DIC_OUTDIR_PARSING' from `BiblioSpecificGlobals` 
        of `BiblioAnalysis_utils` package are used.
        The function `Select_multi_items` from `BiblioGui module` of `BiblioAnalysis_utils` package is used.
        
    '''
    
    # Standard library imports
    from pathlib import Path
    
    # 3rd party imports
    import numpy as np
    import pandas as pd
    
    # Local imports
    from BiblioAnalysis_Utils.BiblioGui import Select_multi_items
    from BiblioAnalysis_Utils.BiblioSpecificGlobals import COL_NAMES
    from BiblioAnalysis_Utils.BiblioSpecificGlobals import DIC_OUTDIR_PARSING
    
    
    institutions_alias = COL_NAMES['auth_inst'][4]
    country_alias = COL_NAMES['country'][2]    
    
    df_auth_inst = pd.read_csv(Path(out_dir_parsing) / Path(DIC_OUTDIR_PARSING['I2']),
                                sep = '\t')
    raw_institutions_list = []
    for auth_inst in df_auth_inst[institutions_alias]:
        raw_institutions_list.append(auth_inst.strip())
        
    institutions_list = list(np.concatenate([raw_inst.split(';') for raw_inst in raw_institutions_list]))
    institutions_list  = sorted(list(set(institutions_list)))

    country_institution_list = [x.split('_')[1] + ':' + x.split('_')[0] for x in institutions_list]
    country_institution_list = sorted(country_institution_list)

    selected_list = Select_multi_items(country_institution_list,
                                       mode='multiple',
                                       fact=2,
                                       win_widthmm=80,
                                       win_heightmm=100,
                                       font_size=16)

    inst_filter_list = [(x.split(':')[1].strip(),x.split(':')[0].strip()) for x in selected_list]
    
    return inst_filter_list

