__all__ = ['filter_corpus_new']

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

    acronyme = {"authors":"AU",             # ex: Faure-Vincent J, De Vito E, Simonato J-P
                "countries":"CU",           # ex: France, United States
                "institutions":"I",         # ex: CEA-Liten, CEA/CNRS/IRIG
                "document type":"DT",       # ex: Conference Paper, Article 
                "pubsources":"J",           # ex: Physical Review B
                "language":"LA",            # ex: English, French
                "publication year":"Y",     # ex: 2019
                "subject category":"S",     # ex: Chemical Engineering,Engineering 
                "subject subcategory":"S2", # ex: Applied Mathematics, Organic Chemistry
                "refsouce":"RJ",
                "references":"R",
                "keywords_IK":"IK",
                "keywords_TK":"TK",
                "keywords_AK":"AK"          # ex: BIOMASS, SOLAR FUEL
                }


    with open(file_config, "r") as read_file:
            config_filter = json.load(read_file)

    combine = config_filter["COMBINE"]
    exclusion = config_filter["EXCLUSION"]

    for key, value in config_filter.items():
        if isinstance(value, dict):
            if value['mode']:
                filter_param[acronyme[key]]=value["list"]

    return combine,exclusion,filter_param

def save_filtered_files(tokeep,in_dir,out_dir):
    
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
    
    # 3rd party import
    import pandas as pd

    tokeep =[str(x) for x in tokeep]

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

def filter_pub_id(combine,exclusion,filter_param,in_dir):

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
    import os as os
    from pathlib import Path
    import re
    
    # 3rd party import
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
            Ymin = filter_param['Y']['ymin']
            Ymax = filter_param['Y']['ymax']
            keepid[item] = set(df.loc[(df[item] >= Ymin) & (df[item]<=Ymax)].index)

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
    #tokeep = filter_pub_id(combine,exclusion,filter_param,out_dir_parsing)
    tokeep = filter_pub_id(combine,exclusion,filter_param,in_dir)
    
    # Stores the filtered files 
    #save_filtered_files(tokeep,in_dir_parsing,out_dir)
    save_filtered_files(tokeep,in_dir,out_dir)

