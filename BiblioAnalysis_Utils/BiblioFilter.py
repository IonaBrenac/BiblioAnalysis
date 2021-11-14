__all__ = ['filter_corpus_new',
           'filters_modification',
           'item_filter_modification',
           'item_values_list',
           'read_config_filters',]

# Functions used from .BiblioGui: Select_multi_items, filter_item_selection


def read_config_filters(file_config):
    """
    Parse json file to build the filtering configuration
    
    Args:
        file_config (Path): absolute path of the configuration file
       
    Returns:
        combine (str):
        filter_param (dict): {key:list of keywords}
    """
    # Standard library imports
    import json
    from collections import defaultdict

    filter_param = defaultdict(list)

    with open(file_config, "r") as read_file:
            config_filter = json.load(read_file)

    combine = config_filter["COMBINE"]
    exclusion = config_filter["EXCLUSION"]

    for key, value in config_filter.items():
        if isinstance(value, dict):
            if value['mode']:
                filter_param[key] = value["list"]

    return combine,exclusion,filter_param

def _save_filtered_files(tokeep,in_dir,out_dir):
    
    '''Filters all the files with ".dat" extension located in the folder in_dir #<---------------------
    and saves the filtered files in the folder out_dir_.   #<---------------------
    The set "tokeep" contains the id (pu_id) of the articles to be kept in the filtered corpus. #<--------------
    
    Args:
        tokeep (set): set of id
        in_dir (Path): path of the folder containing the files to filter
        out_dir (Path): path of the folder where the filtered files are stored
    '''
    # Standard library imports
    import os
    from pathlib import Path
    
    # 3rd party imports
    import pandas as pd

    #tokeep =[str(x) for x in tokeep] ! not clear, to be understood (generate empty filtered corpus)

    for file in [file  for file in os.listdir(in_dir)
                 if file.endswith('.dat')]:
        df = pd.read_csv(in_dir / Path(file),
                         sep='\t',
                         header=None)
        df.rename(columns = {0 : 'pub_id'}, inplace = True)
        df.query('pub_id in @tokeep').to_csv(out_dir / Path(file), 
                                             index=False,
                                             header=None,
                                             sep="\t")

def _filter_pub_id(combine,exclusion,filter_param,in_dir):

    '''<--------------------- modifié AC
    This function finds the set of the identifiers (pub_id) of the publications
    that satisfy sorting criteria.                

    Args:
       combine (string) : "intersection" or "union"; defines the combination 
       of the sets of the kept pub_id by item key
       
       exclusion (bool): if true the complementary set of the kept pub_id set
       resulting from combination is returned

       filter_param (dict): {item key: [list of items to keep]}
           ex {"CU":["France","Italy"]}

    Returns:
        tokeep (set): set of kept publications id
    '''

    # Standard library imports
    import os
    import re
    from pathlib import Path

    # 3rd party imports
    import pandas as pd

    filter_on = list(filter_param.keys())

    keepid = {}

    # Builds keepid[Y]={Y}, keepid[J]={J}, keepid[DT]={DT}, keepid[LA]={LA}
    # where {Y}, {J}, {DT} and {LA} are the sets of pub_id of articles with
    # Ymin>=Year>=Ymax, with Journal in filter_param["J"],
    # with doctypes in filter_param["J"] and with Language (LA) in  filter_param["LA"]
    #----------------------------------------------------------------------------
    for idx, item in enumerate(set(filter_on) & set(["Y","J","DT","LA"])):
        if idx == 0:
            df = pd.read_csv(in_dir / Path('articles.dat'),
                             sep='\t',header=None,usecols=[0,2,3,8,9])
            df.columns = ['pub_id',    # article id
                          'Y',         # publication year
                          'J',         # journal
                          'DT',        # document type ex: article
                          'LA',        # language
                          ]
        if item == 'Y': #years selection
            year = filter_param['Y']
            keepid[item] = set(df.query('Y in @year').index)

        elif item == 'LA': #language selection
            languages = filter_param['LA']
            keepid[item] = set(df.query('LA in @languages').index)

        elif item == 'DT': #document type selection
            doctypes = filter_param['DT']
            keepid[item] = set(df.query('DT in @doctypes').index)

        elif item == 'J': #journal selection
            pubsources = filter_param['J']
            keepid[item] = set(df.query('DT in @pubsources').index)

    # Builds keepid[IK]={IK} keepid[TK]={TK} keepid[AK]={AK} 
    # where {IK}, {TK}, {AK} are the sets of pub_id of articles with
    # one keyword repectivelly in filter_param["IK"], filter_param["TK"], filter_param["AK"]
    # ---------------------------------------------------------------
    for idx, item in enumerate(set(filter_on) & set(["IK","TK","AK"])):
        if idx==0:
            df = pd.read_csv(in_dir / Path('keywords.dat'),
                             sep='\t',header=None)
            df.columns = ['pub_id','label','keyword']

        keywords =  filter_param[item]
        keepid[item] = set([xx[0]  
                           for xx in df.query('label==@item').   # SELECT the row with the proper label
                           groupby('pub_id')['keyword']          # group by article id
                           if len(set(xx[1]) & set(keywords))!=0])


    # Builds keepid[AU]={AU} where {AU} is the set of pub_id 
    # of articles with at least one coauthors in the list filter_param["AU"]
    # ------------------------------------------------------------
    if "AU" in filter_on:
        df = pd.read_csv(in_dir / Path('authors.dat'),
                         sep='\t',header=None,usecols=[0,2])
        df.columns = ["pub_id","author"]
        authors =  filter_param["AU"]
        keepid['AU'] = set(df.query('author in @authors')['pub_id'])

    # Builds keepid[CU]={CU} where {CU} is the of pub_id 
    # of articles with at least one coauthor country in the list filter_param["CU"]
    # ------------------------------------------------------------
    if "CU" in filter_on:
        df = pd.read_csv(in_dir / Path('countries.dat'),
                         sep='\t',header=None,usecols=[0,2])
        df.columns = ["pub_id","country"]
        countries =  filter_param["CU"]
        keepid["CU"] = set(df.query('country in @countries')['pub_id'])

    # Builds keepid[I]={I} where {I} is the of pub_id 
    # of articles with at least one coauthor institution in the list filter_param["CU"]
    # ------------------------------------------------------------
    if "I" in filter_on:
        df = pd.read_csv(in_dir / Path('institutions.dat'),
                         sep='\t',header=None,usecols=[0,2])
        df.columns = ["pub_id","institution"]
        institutions =  filter_param["I"]
        keepid["I"] = set(df.query('institution in @institutions')['pub_id'])

    # Builds keepid[S]={S} where {S} is the of pub_id 
    # of articles with subjects in the list filter_param["S"]
    # ------------------------------------------------------------
    if "S" in filter_on:
        df = pd.read_csv(in_dir / Path('subjects.dat'),
                         sep='\t',header=None)
        df.columns = ["pub_id","subject"]
        subjects =  filter_param["S"]
        keepid["S"] = set(df.query('subject in @subjects')['pub_id'])

    # Builds keepid[S2]={S2} where {S2} is the of pub_id 
    # of articles with subsubjects in the list filter_param["S2"]
    # ------------------------------------------------------------
    if "S2" in filter_on:
        df = pd.read_csv(in_dir / Path('subjects2.dat'),
                         sep='\t',header=None)
        df.columns = ["pub_id","subject"]
        subsubjects =  filter_param["S2"]
        keepid["S2"] = set(df.query('subject in @subsubjects')['pub_id'])
        
    # Builds keepid[R]={R}, keepid[RJ]={RJ}
    # where {R} is the set acticles id with references 
    #     in the list filter_param["R"]
    # {RJ} is the set acticles id with references journal 
    #     in the list filter_param["RJ"]
    # of articles with references 
    # ------------------------------------------------------------
    if ("R" in filter_on) or ("RJ" in filter_on):
        df = pd.read_csv(in_dirg / Path('references.dat'),
                         sep='\t',header=None,
                         usecols=[0,1,2,3,4,5] ).astype(str)
        df.columns = ['pub_id','author','year','journal','vol','page']
        
        if "R" in filter_on:
            find_0 = re.compile(r',\s?0')
            df['ref'] = df.apply(lambda row:re.sub(find_0,'', ', '.join(row[1:-1]))
                                 ,axis=1)
            references =  filter_param["R"]
            keepid["R"] = set(df.query('ref in @references')['pub_id']) 
            
        if "RJ" in filter_on:
            refsources = filter_param["RJ"]
            keepid["RJ"] = set(df.query('subject in @refsources')['pub_id'])
            
    # Combines the filtering conditions union / intersection /exclusion
    # -------------------------------------------------------------------
    tokeep = [value for value in keepid.values()] # list of kept id sets
    if combine == "intersection":
        tokeep = set.intersection(*tokeep)

    if combine == "union":
        tokeep = set.union(*tokeep)

    if exclusion:
        df = pd.read_csv(in_dir / Path('articles.dat'),
                             sep='\t',header=None,usecols=[0])
        set_pub_id = set(df[0])              # set of all pub_id
        tokeep = set_pub_id.difference(tokeep)
        
    return tokeep

def filter_corpus_new(in_dir, out_dir, verbose, file_config_filters):
    
    '''Filters the 
    '''

    # Reads the fitering parameters
    combine,exclusion,filter_param = read_config_filters(file_config_filters)
    
    # Builds the set of articles id to keep
    tokeep = _filter_pub_id(combine,exclusion,filter_param,in_dir)
    
    # Stores the filtered files 
    _save_filtered_files(tokeep,in_dir,out_dir)
    
def item_filter_modification(item,item_values, filters_filename) :
    '''
    Modification of items values list in the json file of the filtering configuration
    for corpus filtering 
    
    Args: 
        item (str): item accronyme
        item_values (list): list of item values to be put in the json file 
        filters_filename (path): path of the json file 
        
    '''
    
    # Standard library imports
    import json

    with open(filters_filename, "r") as read_file:
        config_filter = json.load(read_file)
    
    config_filter[item]['list'] = item_values
    
    with open(filters_filename, "w") as write_file:
        jsonString = json.dumps(config_filter, indent=4)
        write_file.write(jsonString)
        
def item_values_list(item_values_file):
    '''
    Builds a list of item values from a file of the same structure 
    as the text files resulting from the corpus description (".dat" extension)
    
    Args: 
        item_values_file (path): path of the dat file that contains the item values (str)
        
    Returns:
        item_values_select (list): list of item values
    '''

    # Standard library imports
    import csv
    
    item_values = []
    with open(item_values_file, newline='') as f:
        reader = csv.reader(f)
        item_values = list(reader)
        
    item_values_select =[]
    for x in range(len(item_values)):
        mystring = str(item_values[x])
        start = 2
        end = mystring.find(',', start) - 1
        value = str(mystring[start:end]).replace("'",'"')
        item_values_select.append(value)
        
    return item_values_select

def filters_modification(config_folder,file_config_filters):
    '''
    Modification of the filter configuration 
    using a selection of item values saved in the file item_values_file (.dat file) 
    of the same structure as item files resulting from corpus description
    
    Args:
        config_folder (path): path of the configuration folder 
                              containing the file item_values_file selected interactively
        file_config_filters (path): path of the json filters configuration file
    
    '''
    
    # Standard library imports
    import os
    from pathlib import Path
    
    # Local imports
    from .BiblioGui import Select_multi_items
    from .BiblioGui import filter_item_selection

    # Identifying the item to be modified in the filters configuration
    filter_item = filter_item_selection()

    # Setting the folders list for item_values selection list
    folders_list = [x[0] for x in os.walk(config_folder)][1:]
    folders_list = [os.path.split(x)[-1] for x in folders_list]
    folders_list.sort()

    # Selection of the folder of the item_values selection files
    print('Please select the folder of item_values selection file via the tk window')
    myfolder_name = Select_multi_items(folders_list,'single')[0]+'/'
    myfolder = config_folder / Path(myfolder_name)

    # Setting the list of item_values selection files to be put in the filters configuration file
    files_list = os.listdir(myfolder)
    files_list.sort()
    print('\nPlease select the item_values selection file via the tk window')
    myfile = Select_multi_items(files_list,'single')[0]+'/'

    item_values_file = myfolder / Path(myfile)
    item_values_list_select = item_values_list(item_values_file) 

    item_filter_modification(filter_item,item_values_list_select, file_config_filters)


