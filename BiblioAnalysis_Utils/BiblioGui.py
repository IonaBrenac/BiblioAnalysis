__all__ = ['item_selection',
           'cooc_selection',
           'merge_database_gui',
           'filters_selection',
           'SAVE_CONFIG_FILTERS',
           'coupling_attr_selection',
           'Select_multi_items',
           'filter_item_selection',
           'select_folder_gui',
           'select_folder_gui_new',]

# Globals used from .BiblioSys: DISPLAYS
# Globals used from .BiblioGeneralGlobals: IN_TO_MM

from .BiblioSpecificGlobals import (DIC_OUTDIR_PARSING,
                            LABEL_MEANING,
                            COOC_AUTHORIZED_ITEMS_DICT)

ACRONYME_MEANING = dict(zip(LABEL_MEANING.values(),LABEL_MEANING.keys()))

TREE_MAP_ITEM = [
    ("years", 1),
    ("languages", 2),
    ("doctypes", 3),
    ("countries", 4),
    ("institutions", 5),
    ("journals", 6),
    ("references", 7),
    ("refjournals", 8),
    ("subjects", 9),
    ("subjects2", 10),
    ("journalkeywords", 11),
    ("titlekeywords", 12),
    ("authorskeywords", 13),
    ("authors",14)
]

TREE_MAP_ITEM_HELP_TEXT = '''Select the item you want to deal with.

With MACOS, to exit you have to kill manually the menu window.''' 

GEOMETRY_ITEM_SELECTION = '350x520+50+50'

COOC_SELECTION_HELP_TEXT = '''In a cooccurrence graph two authors, keywords, sujects 
or more generally two 'items' are linked by an edge, if two
authors have coothered an article, if two keywords
names belong to the same article...

To build a cooccurrence graph, you have to select:
                                 - the item used to build cooccurrences graph (default='Authors')
                                 - the minimum size of the node (integer, default=1)
                                 
The node size is the total number of occurences of an author, keyword name,... in the corpus.

With macOS, to exit you have to kill manually the menu window.''' 

GEOMETRY_COOC_SELECTION = '410x350+50+50'
GEOMETRY_COUPLING_SELECTION = '470x350+50+50'

MERGE_DATABASE_HELP_TEXT = '''Merge several databases (wos/scopus) in one database.
You have to choose:
    the database type (wos/scopus)
    the name of the merged database (without extension)
    the input dfolder where the databases are stored
    the output folder where the merged database will be stored.
    
With macOS, to exit you have to kill manually the menu window.''' 

GEOMETRY_MERGE_GUI = '500x550+50+50'

FILTERS_ITEMS_DICT = {'Authors':'AU',
                      'Years':'Y',
                      'Institutions':'I',
                      'Document types':'DT',
                      'Journals':'J',
                      'References journals':'RJ',
                      'Full references':'R',
                      'Authors keywords':'AK',
                      'Title keywords':'TK',
                      'Journal keywords':'IK',
                      'Countries':'CU',
                      'Subjects':'S',
                      'Sub-subjects':'S2',
                        }

FILTERS_SELECTION_HELP_TEXT = '''To be done'''

GEOMETRY_FILTERS_SELECTION = '500x580+50+50'

SAVE_CONFIG_FILTERS = 'save_config_filters.json'

DEFAULT_SAVE_CONFIG_FILTER = {'description': 'items to be combined in union or intersection for filtering the corpus',
 'COMBINE': 'union',
 'EXCLUSION': False,
 'AU': {'description': 'Selected authors',
  'mode': False,
  'list': []},
 'Y': {'description': 'Selected time period', 'mode': False, 'list': []},
 'CU': {'description': 'Selected countries',
  'mode': False,
  'list': []},
 'I': {'description': 'Selected institutions',
  'mode': False,
  'list': []},
 'DT': {'description': 'Selected document types',
  'mode': False,
  'list': []},
 'J': {'description': 'Selected journals',
  'mode': False,
  'list': []},
 'LA': {'description': 'Selected languages',
  'mode': False,
  'list': []},
 'S': {'description': 'Selected subject categories',
  'mode': False,
  'list': []},
 'S2': {'description': 'Selected subject subcategories',
  'mode': False,
  'list': []},
 'RJ': {'description': 'Selected journals of cited publications',
  'mode': False,
  'list': []},
 'R': {'description': 'Selected full references of cited publications',
  'mode': False,
  'list': []},
 'IK': {'description': 'Selected keywords',
  'mode': False,
  'list': []},
 'TK': {'description': 'Selected title words',
  'mode': False,
  'list': []},
 'AK': {'description': 'Selected authors keywords',
  'mode': False,
  'list': []}}

def item_selection() :
    
    '''
    Selection of items for treemaps
    
    Arguments: none
    
    Returns:
        ITEM_CHOICE (string): choosen item

    '''
    
    # Standard library imports
    import os
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
    
    global ITEM_CHOICE
    
    def help():
        messagebox.showinfo("Item selection info", TREE_MAP_ITEM_HELP_TEXT)
    
    tk_root = tk.Tk()
    tk_root.attributes("-topmost", True)
    tk_root.geometry(GEOMETRY_ITEM_SELECTION)
    tk_root.title("Treemap GUI") 
    item_choice = ttk.LabelFrame(tk_root, text=' Label selection ')
    item_choice.grid(column=0, row=0, padx=8, pady=4)
    
    menu = ttk.LabelFrame(tk_root, text=' Menu ')
    menu.grid(column=1, row=0, padx=8, pady=4)
    
    
    ITEM_CHOICE = "subjects"
    def choice(text, v):
        global ITEM_CHOICE
        ITEM_CHOICE = text
        
    #
    # choice of the item for treemap
    #
    varitem = tk.IntVar()
    varitem.set(TREE_MAP_ITEM[0][1])

    tk.Label(item_choice, text='Choose the item for treemap :').grid(column=0, row=1, padx=8, pady=4)
    
    idx_row = 2
    for txt, val in TREE_MAP_ITEM:
        tk.Radiobutton(item_choice, text = txt, variable = varitem, value=val,
            command=lambda t = txt, v = varitem: choice(t, v)).grid(column=0, row=idx_row+2, padx=8, pady=4,sticky=tk.W)
        idx_row += 1

    help_button = ttk.Button(menu, text="HELP", command=help)
    help_button.grid(column=0, row=0)
    
    if os.name == 'nt':
        tk.Button(menu, text="EXIT", command=tk_root.destroy).grid(column=0, row=1, padx=8, pady=4)
    tk_root.mainloop()
    
    return ITEM_CHOICE

def cooc_selection() :
    
    '''
    Selection of items for cooccurrences graph treatment
    
    Arguments: none
    
    Returns:
        ITEM_CHOICE (string): item acronyme
        minimum_size_node (int): minimum size of the nodes


    '''
    # Standard library imports
    import os
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
    
    global ITEM_CHOICE, minimum_size_node
     
    tk_root = tk.Tk()
    tk_root.attributes("-topmost", True)
    tk_root.geometry(GEOMETRY_COOC_SELECTION)
    tk_root.title("Graph cooccurrence GUI") 
    
    item_choice = ttk.LabelFrame(tk_root, text=' Label selection ')
    item_choice.grid(column=0, row=0, padx=8, pady=4)
    
    size_choice = ttk.LabelFrame(tk_root, text=' Size choice ')
    size_choice.grid(column=1, row=0, padx=8, pady=4)
    
    ITEM_CHOICE = 'AU'  # Default value
    def choice(text, v):
        global ITEM_CHOICE
        ITEM_CHOICE = COOC_AUTHORIZED_ITEMS_DICT[text]
    
    minimum_size_node = 1 # Default value
    def submit(): 
        global minimum_size_node
        minimum_size_node = size_entered.get()
    
    def help():
        messagebox.showinfo("cooc selection info", COOC_SELECTION_HELP_TEXT)
        
        
    #                               Choice of the item for the cooccurrence graph
    # -------------------------------------------------------------------------------------------
    item = [(x,i) for i,x in enumerate(COOC_AUTHORIZED_ITEMS_DICT.keys())]
    varitem = tk.IntVar()
    #varitem.set(item[0][1])

    ttk.Label(item_choice , 
             text='Choose an item\nfor the co-occurrence graph:').grid(column=0, row=1, padx=8, pady=4)
    
    idx_row = 2
    for txt, val in item:
        tk.Radiobutton(item_choice, text=txt, variable=varitem, value=val,
            command=lambda t = txt, v=varitem: choice(t, v)).grid(column=0, \
                                    row=idx_row+2, padx=8, pady=4,sticky=tk.W)
        idx_row += 1
     
    #                                Minmum node size selection
    # -------------------------------------------------------------------------------------------
    name = tk.StringVar()
    ttk.Label(size_choice , 
             text='Choose the minimum\nsize of the nodes:').grid(column=0, row=0, padx=8, pady=4)
    size_entered = ttk.Entry(size_choice, width=5, textvariable=name)
    size_entered.grid(column=0, row=1, padx=8, pady=4) #sticky=tk.W) 
    

    submit_button = ttk.Button(size_choice, text="Submit", command=submit)   
    submit_button.grid(column=0, row=2, padx=8, pady=4) 
    help_button = ttk.Button(size_choice, text="HELP", command=help)
    help_button.grid(column=0, row=3, padx=8, pady=4)
    
    if os.name == 'nt':
        tk.Button(size_choice, text="EXIT", command=tk_root.destroy).grid(column=0, row=4, padx=8, pady=4)
    
    tk_root.mainloop()
    
    try:
        minimum_size_node = int(minimum_size_node)
    except: # Takes a default value
        minimum_size_node = 1
    
 
    return ITEM_CHOICE, minimum_size_node
    
def merge_database_gui() :
    
    '''
    Selection of database files to be merged
    
    Arguments: none
    
    Returns:
        database (str): database type (scopus or wos)
        filename (str): name of the merged database
        in_dir (str): name of the folder where the databases to be merged are stored
        out_dir (str): name of the folder where the merged database will be stored

    '''
    # Standard library imports
    import os
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
    from tkinter import filedialog
    from pathlib import Path

    
    global DATABASE_TYPE, DATABASE_FILENAME, IN_DIR, OUT_DIR
     
    tk_root = tk.Tk()
    tk_root.attributes("-topmost", True)
    tk_root.geometry(GEOMETRY_MERGE_GUI)
    tk_root.title("Graph cooccurrence GUI") 
    
    item_choice = ttk.LabelFrame(tk_root, text=' Database selection ')
    item_choice.grid(column=0, row=0, padx=8, pady=4)
    
    folder_choice = ttk.LabelFrame(tk_root, text=' Folders selection ')
    folder_choice.grid(column=1, row=0, padx=8, pady=4)
    
    DATABASE_TYPE = 'wos'  # Default value
    def choice(text, v):
        global DATABASE_TYPE
        DATABASE_TYPE = text
    
    DATABASE_FILENAME = "test" # Default value
    def submit(): 
        global DATABASE_FILENAME
        DATABASE_FILENAME = size_entered.get()
        if DATABASE_TYPE == "wos":
            DATABASE_FILENAME = DATABASE_FILENAME + '.txt'
        else:
            DATABASE_FILENAME = DATABASE_FILENAME + '.csv'
    
    def indir_folder_choice():
        global IN_DIR
        IN_DIR = filedialog.askdirectory(initialdir=str(Path.home()), title="Select in_dir folder")                             
    
    def outdir_folder_choice():
        global OUT_DIR
        OUT_DIR = filedialog.askdirectory(initialdir=str(Path.home()), title="Select out_dir folder")   
    
    def help():
        messagebox.showinfo("Merge database info", MERGE_DATABASE_HELP_TEXT)
        
        
    #                               Choice of a database
    # -------------------------------------------------------------------------------------------
    item = ["wos", 'scopus']
    varitem = tk.IntVar()
    varitem.set(item[0][1])

    ttk.Label(item_choice , 
             text='Choose a database type:').grid(column=0, row=1, padx=8, pady=4)
    
    idx_row = 2
    for  val, txt,  in enumerate(item):
        tk.Radiobutton(item_choice, text = txt, variable = varitem, value=val,
            command=lambda t = txt, v = varitem: choice(t, v)).grid(column=0, row=idx_row+2, padx=8, pady=4,sticky=tk.W)
        idx_row += 1
     
    #                   File name, in_dir,  out_dir selection
    # -------------------------------------------------------------------------------------------
    name = tk.StringVar()
    ttk.Label(folder_choice , 
             text='File name of the merged database:').grid(column=0, row=0, padx=8, pady=4)
    size_entered = ttk.Entry(folder_choice, width=30, textvariable=name)
    size_entered.grid(column=0, row=1, sticky=tk.W) 
    

    submit_button = ttk.Button(folder_choice, text="Submit", command=submit)   
    submit_button.grid(column=1, row=1, padx=8, pady=4)
    
    indir_button = ttk.Button(folder_choice, text="In-dir folder", command=indir_folder_choice)
    indir_button.grid(column=0, row=2, padx=8, pady=4)
    
    outdir_button = ttk.Button(folder_choice, text="Out-dir folder", command=outdir_folder_choice)
    outdir_button.grid(column=0, row=3, padx=8, pady=4)
    
    help_button = ttk.Button(folder_choice, text="HELP", command=help)
    help_button.grid(column=0, row=5, padx=8, pady=4)
    
    
    if os.name == 'nt': # Work with nt not macos
        tk.Button(folder_choice, text="EXIT", command=tk_root.destroy).grid(column=0, row=6, padx=8, pady=4)
    
    tk_root.mainloop()
    
    return DATABASE_TYPE, DATABASE_FILENAME, IN_DIR, OUT_DIR
    
def read_item_state(item,parsing_dir):
    '''
    item: 
    parsing_dir:
    '''

    # Standard library imports
    from pathlib import Path
    
    # 3rd party imports
    import pandas as pd
    
    if item in ['AU','CU','I']:
        df = pd.read_csv(parsing_dir / Path(DIC_OUTDIR_PARSING[item]),
                     sep='\t',
                     engine='python',
                     header=None)
        df.columns = ['pub_id','idx','attribute']
        dg = df['attribute'].tolist()
    
    elif item in ['IK','TK','AK','S','S2']:
        df = pd.read_csv(parsing_dir / Path(DIC_OUTDIR_PARSING[item]),
                     sep='\t',
                     engine='python',
                     header=None)
        df.columns = ['pub_id','attribute']
        dg = df['attribute'].tolist()
        
    elif item in ['Y','DT','J','LA']:
        df = pd.read_csv(parsing_dir / Path(DIC_OUTDIR_PARSING['A']),
                     sep='\t',
                     engine='python',
                     header=None).astype(str)
        df.columns = ['pub_id','authors','Y','J','vol', 'page','DOI', 'DT','LA','title','ISSN']
        if item == 'Y':
            dg = df['Y'].tolist()
        if item == 'DT':
            dg = df['DT'].tolist()       
        if item == 'J':
            dg = df['J'].tolist()            
        if item == 'LA':
            dg = df['LA'].tolist()
            
    elif item in ['R','RJ']:
        df = pd.read_csv(parsing_dir / Path(DIC_OUTDIR_PARSING['R']),
                     sep='\t',
                     engine='python',
                     header=None).astype(str)
        df.columns = ['pub_id','first_author','year','journal','volume','page']
        if item == 'R':
            table = df.T.apply(lambda row : ", ".join(row[1:] )) # Builds ref: "author, year, journal, volume, page"
                                                                 # ex:"Gordon P, 2004, SCIENCE, 306, 496"
            dg = table.tolist()
        if item == 'RJ':
            dg = df['journal'].tolist()              

    return dg

def select_item_attributes(dg,item_tag,config_filter):

    """interactive selection of items among the list list-item
    
    Args:
        list_item (list): list of items used for the selection
        
    Returns:
        list (list): list of selected items without duplicate
        
    """
    import collections
    import os
    import re
    import tkinter as tk
    
    global val
    val = list_default = config_filter[item_tag]['list']
    
    re_split = re.compile('\s\(\d{1,5}\)')
    
    dg = sorted([ (token,nbr_occurrence_token) for token,nbr_occurrence_token in collections.Counter(dg).items()],
                   key=lambda tup: tup[1], reverse=True)

    list_item = [token+ f' ({int(nbr_occurrence_token)})' for token,nbr_occurrence_token 
                  in dg
                  if nbr_occurrence_token>2]

    top = tk.Toplevel()
    top.geometry(GEOMETRY_FILTERS_SELECTION)
    top.attributes("-topmost", True)

    yscrollbar = tk.Scrollbar(top)
    yscrollbar.pack(side = tk.RIGHT, fill = tk.Y)

    listbox = tk.Listbox(top, width=40, height=10, selectmode=tk.MULTIPLE,
                     yscrollcommand = yscrollbar.set)

    x = list_item

    for idx,item in enumerate(x):
        listbox.insert(idx, item)
        listbox.itemconfig(idx,
                 bg = "white" if idx % 2 == 0 else "white")
    
    for default_value in list_default:
        idx = [dg.index(tupl) for tupl in dg if tupl[0] == default_value]
        if idx != []:
            listbox.selection_set(idx)

    def selected_item():
        global val
        val = [re.split(re_split, listbox.get(i))[0] for i in listbox.curselection()]
        config_filter[item_tag]['list'] = val
        if os.name == 'nt':
            top.destroy()

    btn = tk.Button(top, text='OK', command=selected_item)

    btn.pack(side='bottom')

    listbox.pack(padx = 10, pady = 10,
              expand = tk.YES, fill = "both")
    yscrollbar.config(command = listbox.yview)
    top.mainloop()
    return val
    
def function_help():
    import tkinter as tk
    top = tk.Toplevel()
    top.geometry(GEOMETRY_FILTERS_SELECTION)
    top.attributes("-topmost", True)
    T = tk.Text(top)
    T.pack(expand = True, fill = tk.BOTH)
    T.insert("end",FILTERS_SELECTION_HELP_TEXT)
    top.mainloop()

def filters_selection(filters_filename, save_filename, parsing_dir) :
    
    '''
    Selection of items for corpus filtering 
    
    Arguments: 
        filters_filename (path): path of the json file of the filtering configuration
        save_filename (path): full path name of the new .json file
        parsing_dir (path) : path of the corpus folder containing the files used to build 
                            the selection menu of items 
        
    
    Returns:
        ITEM_CHOICE (string): item acronyme
        minimum_size_node (int): minimum size of the nodes


    '''
    # Standard library imports
    import functools
    import json
    import os
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
    from pathlib import Path
    
    global ITEM_CHOICE, minimum_size_node,val, number_of_call
    number_of_call = 0
    
    try:
        with open(filters_filename, "r") as read_file:
            config_filter = json.load(read_file)
    except:
        config_filter = DEFAULT_SAVE_CONFIG_FILTER
            
    def spy_state(*args):
        global number_of_call
        number_of_call += 1
        nbr_select = sum([x.get() for x in varitem] )
        if (nbr_select<2) & (number_of_call>=len(items)):
            button_union["state"] = "disable"
            button_inter["state"] = "disable"
            button_union.deselect()
            button_inter.deselect()
            
            #messagebox.showwarning('you must select at leasst two items to use \n union/intersection set operation')
            
        else:
            button_union["state"] = "normal"
            button_inter["state"] = "normal"
            if config_filter['COMBINE'] == 'union':
                button_union.select()
            else:
                button_inter.select()
            
        
    def action_varitem():
        for idx in range(len(LABEL_MEANING)):
            if varitem[idx].get():
                list_button[idx]['state'] = 'normal'
                item_label = [tupl[0] for i, tupl in enumerate(items) if tupl[1] == idx][0]
                item_acronyme = ACRONYME_MEANING[item_label]
                config_filter[item_acronyme]['mode'] = True
            else:
                list_button[idx]['state'] = 'disabled'
                item_label = [tupl[0] for i, tupl in enumerate(items) if tupl[1] == idx][0]
                item_acronyme = ACRONYME_MEANING[item_label]
                config_filter[item_acronyme]['mode'] = False
            
    def func(item_acronyme):
        dg = read_item_state(item_acronyme,parsing_dir)
        select_item_attributes(dg,item_acronyme,config_filter)
        
    def ModeSelected():
        choice  = var_union_inter.get()
        if choice == 1:
           config_filter['COMBINE'] = "union"

        elif choice == 2:
           config_filter['COMBINE'] = "intersection"
        
    def action_exlusion():
        choice  = var_exclusion.get()
        if choice:
            config_filter['EXCLUSION'] = True
        else:
            config_filter['EXCLUSION'] = False
    
    def func_help():
        function_help()    
     
    tk_root = tk.Tk()
    tk_root.attributes("-topmost", True)
    tk_root.title("Filters GUI")
    tk_root.geometry(GEOMETRY_FILTERS_SELECTION)
    tk_root.columnconfigure(0,weight=1)
    tk_root.columnconfigure(1,weight=1)
    item_choice = ttk.LabelFrame(tk_root, text=' ')
    item_choice.grid(column=0, row=0, padx=8, pady=4,sticky=tk.W+tk.E)
    
    combine_exit = ttk.LabelFrame(tk_root, text=' ')
    combine_exit.grid(column=1, row=0, padx=8, pady=4,sticky=tk.W+tk.E)
    
    combine_choice = ttk.LabelFrame(combine_exit, text=' ')
    combine_choice.grid(column=0, row=0, padx=8, pady=4,sticky=tk.W+tk.E)

    exit_choice = ttk.LabelFrame(combine_exit, text='  ')
    exit_choice.grid(column=0, row=1, padx=8, pady=4)
    
   
    items = [(x,i) for i,x in enumerate(LABEL_MEANING.values())]

    ttk.Label(item_choice , 
             text='Choose the items for filtering').grid(column=0, row=1, padx=8, pady=4)
    
    var_union_inter = tk.IntVar()
    var_exclusion = tk.IntVar()
    tk.Label(combine_choice, text='Choose a combination mode\n between at least 2 items :'
            ).grid(column=0, row=1, padx=8, pady=4)
    
    button_union = tk.Radiobutton(combine_choice,
                                  text = 'Union',
                                  variable = var_union_inter,
                                  value=1,
                                  command=ModeSelected,
                                  state="normal")
    button_union.grid(column=0, row=2, padx=8, pady=4,sticky=tk.W)
    button_inter = tk.Radiobutton(combine_choice,
                                  text = 'Intersection',
                                  variable = var_union_inter,
                                  value=2,
                                  command=ModeSelected,
                                  state="normal")
    button_inter.grid(column=0, row=3, padx=8, pady=4,sticky=tk.W)
    
    if config_filter['COMBINE'] == 'union':
        button_union.select()
    else:
        button_inter.select()
        
    tk.Checkbutton(combine_choice, 
                       text = 'Exclusion', 
                       variable = var_exclusion,command=action_exlusion
                      ).grid(column=0, row=5, padx=8, pady=4,sticky=tk.W)
    
    if config_filter['EXCLUSION']:
        var_exclusion.set(True)
        
    button_help = tk.Button(exit_choice, 
                            text='HELP', 
                            command=func_help)
    button_help.grid(column=0, row=0, padx=8, pady=4,sticky=tk.E+tk.W)
    if os.name == 'nt':
        exit = tk.Button(exit_choice, text="EXIT", command=tk_root.destroy)
        exit.grid(column=0, row=1, padx=8, pady=4)
    
    idx_row = 2
    list_button = []
    varitem = []
    for  txt, val in items:
        check_state = tk.BooleanVar()    #<------------------------
        check_state.trace('w',spy_state) #<------------------------
        varitem.append(check_state)
        if config_filter[ACRONYME_MEANING[txt]]['mode']:
            state = 'normal'
            varitem[val].set(True)
        else:
            state = 'disabled'
            varitem[val].set(False)
        button = tk.Button(item_choice, 
                               text='SELECT', 
                               command=functools.partial(func,ACRONYME_MEANING[txt]),
                               state = state)
        button.grid(column=1, row=idx_row+2, padx=8, pady=4,sticky=tk.W)
        list_button.append(button)
            
        tk.Checkbutton(item_choice, 
                       text = txt, 
                       variable = varitem[idx_row-2],command=action_varitem
                       ).grid(column=0, row=idx_row+2, padx=8, pady=4,sticky=tk.W)
        #button = tk.Button(item_choice, 
        #                       text='SELECT', 
        #                       command=functools.partial(func,ACRONYME_MEANING[txt]),
        #                       state = 'normal')
        #button.grid(column=1, row=idx_row+2, padx=8, pady=4,sticky=tk.W+tk.E)
        #list_button.append(button)
        idx_row += 1 
    
    tk_root.mainloop()
    
    with open(save_filename, "w") as write_file:
        jsonString = json.dumps(config_filter, indent=4)
        write_file.write(jsonString)
        
    return
    
def coupling_attr_selection():
    
    '''
    Selection of items for coupling graph treatment
    
    Arguments: none
    
    Returns:
        ITEM_CHOICE (string): item acronyme
        m_max_attrs (int): maximum added attributes


    '''
    # Standard library imports
    import os
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
    
    global ITEM_CHOICE, m_max_attrs
     
    tk_root = tk.Tk()
    tk_root.attributes("-topmost", True)
    tk_root.geometry(GEOMETRY_COUPLING_SELECTION)
    tk_root.title("Graph coupling GUI") 
    
    item_choice = ttk.LabelFrame(tk_root, text=' Item selection ')
    item_choice.grid(column=0, row=0, padx=8, pady=4)
    
    size_choice = ttk.LabelFrame(tk_root, text=' Number of item values ')
    size_choice.grid(column=1, row=0, padx=8, pady=4)


    
    ITEM_CHOICE = 'S'  # Default value
    def choice(text, v):
        global ITEM_CHOICE
        ITEM_CHOICE = COOC_AUTHORIZED_ITEMS_DICT[text]
    
    m_max_attrs = 2 # Default value
    def submit(): 
        global m_max_attrs
        m_max_attrs = size_entered.get()
    
    def help():
        messagebox.showinfo("coupling selection info", COOC_SELECTION_HELP_TEXT)
        
        
    #           Choice of the item for the coupling graph completion
    # -------------------------------------------------------------------------------------------
    item = [(x,i) for i,x in enumerate(COOC_AUTHORIZED_ITEMS_DICT.keys())]
    varitem = tk.IntVar()
    #varitem.set(item[0][1])

    ttk.Label(item_choice , 
             text='Choose an item\nfor the coupling graph node attribute:').grid(column=0, row=1, padx=8, pady=4)
    
    idx_row = 2
    for txt, val in item:
        tk.Radiobutton(item_choice, text=txt, variable=varitem, value=val,
            command=lambda t = txt, v=varitem: choice(t, v)).grid(column=0, row=idx_row+2, padx=8, pady=4,sticky=tk.W)
        idx_row += 1
     
    #                       Selection of the maximum number of item values
    # -------------------------------------------------------------------------------------------
    name = tk.StringVar()
    ttk.Label(size_choice , 
             text='Choose the maximum \n number of item values:').grid(column=0,
                                                                       row=0,
                                                                       padx=8,
                                                                       pady=4)
    size_entered = ttk.Entry(size_choice, width=5, textvariable=name)
    size_entered.grid(column=0, row=1, padx=10, pady=4)
    

    submit_button = ttk.Button(size_choice, text="Submit", command=submit)   
    submit_button.grid(column=0, row=2, padx=8, pady=4) 
    help_button = ttk.Button(size_choice, text="HELP", command=help)
    help_button.grid(column=0, row=3, padx=8, pady=4)
    
    if os.name == 'nt':
        tk.Button(size_choice, text="EXIT", command=tk_root.destroy).grid(column=0, row=4, padx=8, pady=4)
    
    tk_root.mainloop()
    
    try:
        m_max_attrs = int(m_max_attrs)
    except: # Takes a default value
        m_max_attrs = 2
    
 
    return ITEM_CHOICE, m_max_attrs

def Select_multi_items(list_item,mode = 'multiple'): 

    """interactive selection of items among the list list_item
    
    Args:
        list_item (list): list of items used for the selection
        
    Returns:
        val (list): list of selected items without duplicate
        
    """
    import os
    import tkinter as tk
    
    global val

    window = tk.Tk()
    window.geometry(GEOMETRY_FILTERS_SELECTION)
    window.attributes("-topmost", True)
    if mode == 'single': 
        title = 'Single item selection'
    else:
        title = 'Multiple items selection'
    window.title(title)

    yscrollbar = tk.Scrollbar(window)
    yscrollbar.pack(side = tk.RIGHT, fill = tk.Y)
    selectmode = tk.MULTIPLE
    if mode == 'single':selectmode = tk.SINGLE
    listbox = tk.Listbox(window, width=40, height=10, selectmode=selectmode,
                     yscrollcommand = yscrollbar.set)

    x = list_item
    for idx,item in enumerate(x):
        listbox.insert(idx, item)
        listbox.itemconfig(idx,
                           bg = "white" if idx % 2 == 0 else "white")
    
    def selected_item():
        global val
        val = [listbox.get(i) for i in listbox.curselection()]
        if os.name == 'nt':
            window.destroy()

    btn = tk.Button(window, text='OK', command=selected_item)
    btn.pack(side='bottom')

    listbox.pack(padx = 10, pady = 10,expand = tk.YES, fill = "both")
    yscrollbar.config(command = listbox.yview)
    window.mainloop()
    return val

def filter_item_selection():
    
    '''
    Selection of item to be modifyed in the filter configuration
    
    Arguments: none
    
    Returns:
        ITEM_CHOICE (string): item acronyme


    '''
    # Standard library imports
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
    
    global ITEM_CHOICE
     
    tk_root = tk.Tk()
    tk_root.attributes("-topmost", True)
    tk_root.geometry(GEOMETRY_ITEM_SELECTION)
    tk_root.title("Filter item selection GUI") 
    
    item_choice = ttk.LabelFrame(tk_root, text=' Item selection ')
    item_choice.grid(column=0, row=0, padx=8, pady=4)
    
    
    ITEM_CHOICE = 'AK'  # Default value
    def choice(text, v):
        global ITEM_CHOICE
        ITEM_CHOICE = FILTERS_ITEMS_DICT[text]
    
    def help():
        messagebox.showinfo("coupling selection info", COOC_SELECTION_HELP_TEXT)
        
        
    #           Choice of the item for the coupling graph completion
    # -------------------------------------------------------------------------------------------
    item = [(x,i) for i,x in enumerate(FILTERS_ITEMS_DICT.keys())]
    varitem = tk.IntVar()

    ttk.Label(item_choice , 
             text='Choose an item to be modifyed in the filter configuration:').grid(column=0, row=1, padx=8, pady=4)
    
    idx_row = 2
    for txt, val in item:
        tk.Radiobutton(item_choice, text=txt, variable=varitem, value=val,
            command=lambda t = txt, v=varitem: choice(t, v)).grid(column=0, row=idx_row+2, padx=8, pady=4,sticky=tk.W)
        idx_row += 1
     
    tk_root.mainloop()

    return ITEM_CHOICE

def select_folder_gui(in_dir,title):
    
    '''
    Interactive selection of a folder.
    
    Args: 
        in_dir (str): name of the initial folder.
        title (str): title of the tk window. 
    
    Returns:
        `(str)`: name of the selected folder

    '''
    # Standard library imports
    import os
    import re
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
    from tkinter import filedialog
    
    global out_dir
    
    # set the tk window geometry 
    width = 10 * len(title + 5 * ' ')
    height = "210"
    
    win = tk.Tk()
    win.attributes("-topmost", True)
    win.geometry(str(width) + 'x' + str(height) )
    win.title('Folder selection window') 
    
    folder_select = tk.LabelFrame(win, text=title, font=('Aerial 18 bold'))
    folder_select.grid(column=0, row=0, padx=30, pady=4)
    
    folder_choice = tk.LabelFrame(win, text='Selected folder', font=('Aerial 18 bold'))
    folder_choice.grid(column=0, row=1, padx=30, pady=4)
    
    help_choice = tk.LabelFrame(win)
    help_choice.grid(column=0, row=2, padx=30, pady=4)
    
    def outdir_folder_choice():
        global out_dir
        out_dir = filedialog.askdirectory(initialdir=in_dir,title=title)
        thr = 0.6 * len(title + 5 * ' ')
        pos_list = [m.start() for m in re.finditer(r'[\\/]', out_dir)]
        for i in range(len(pos_list)):
            if pos_list[-i] >= thr : mid_pos = i
        out_dir1 = str(out_dir)[0:pos_list[-mid_pos]]
        out_dir2 = str(out_dir)[pos_list[-mid_pos]:]
        folder_label1 = ttk.Label(folder_choice, text=out_dir1, font=13)
        folder_label1.grid(column=0, row=1, padx=8, pady=4)
        out_dir2 = str(out_dir)[pos_list[-mid_pos]:]
        folder_label2 = ttk.Label(folder_choice, text=out_dir2, font=13)
        folder_label2.grid(column=0, row=2, padx=8, pady=4)
    
    def help():
        messagebox.showinfo('Folder selection info', '')
    
    outdir_button = ttk.Button(folder_select,text='Select',command=outdir_folder_choice)
    outdir_button.grid(column=0, row=1, padx=40, pady=4)

    help_button = ttk.Button(help_choice, text="HELP", command=help)
    help_button.grid(column=0, row=1, padx=20, pady=4)
    
    
    if os.name == 'nt': # Work with Windows not MacOS
        tk.Button(folder_choice, text="EXIT", command=win.destroy).grid(column=1, row=1, padx=8, pady=4)
    
    win.mainloop()
    
    return out_dir


def select_folder_gui_new(in_dir, titles, buttons_labels, prime_disp=0, widget_ratio=1.2):
    
    '''The function `select_folder_gui_grid` allows the interactive selection of a folder.
    
    Args: 
        in_dir (str): name of the initial folder.
        titles (dict): title of the tk window. 
    
    Returns:
        `(str)`: name of the selected folder.
        
    Note:
        Uses the globals: `IN_TO_MM`;`DISPLAYS`.
        Based on two frames in the main window and two buttons in the top frame.

    '''
    # Standard library imports 
    import math
    import re
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import filedialog
    import tkinter.font as TkFont
    
    # Local imports
    from .BiblioGeneralGlobals import IN_TO_MM
    from .BiblioSys import DISPLAYS
    
    global out_dir
 
    ############# Definition of local functions #############
    
      ## Define the mm to pixels conversion lambda function
    mm_to_px = lambda size_mm,fact : math. ceil((size_mm * fact / IN_TO_MM) * ppi)
    
      ## Define lambda function that get the maximum length of the titles in mm
    str_max_len_mm = lambda list_strs,font,ppi :max([str_size_mm(value, font, ppi)[0] 
                                           for value in list_strs])
    
    def str_size_mm(text, font, ppi):
        '''The function `str_size_mm` computes the sizes in mm of a string.
        
        Args:
            text (str): the text of which we compute the size in mm.
            font (tk.font): the font of the text.
            ppi (int): pixels per inch of the display.
        
        Returns:
            `(tuple)`: width in mm `(string)`, height in mm `(string)`.
            
        Note:
            The use of this function requires a tkinter window availability 
            since it is based on a tkinter font definition.
            
        '''

        (w_px,h_px) = (font.measure(text),font.metrics("linespace"))
        w_mm = w_px * IN_TO_MM / ppi
        h_mm = h_px * IN_TO_MM / ppi

        return (w_mm,h_mm )
    
    def split_path2str(in_dir,max_px,font,ppi):
        '''The function `split_path2str` splits the `in_dir` string 
        in substrings of pixels sizes lower than `max_px`.
        
        Args:
            in_dir (str): the full path of a folder.
            max_px (int): the maximum size in pixels for the substrings 
                          that should result from the split of `in-dir`.
            font (tk.font): the font used for the substrings size evaluation in mm.
            ppi (int): pixels per inch of the display.
        
        Returns:
            `(tuple)`: tuple of the substrings resulting from the split of `in-dir`.
            
        Note:
            The use of this function requires a tkinter window availability 
            since it is based on a tkinter font definition.
            
        '''        
          
        # Standard library imports 
        import numpy as np
        import re

        len_in_dir,_ = str_size_mm(in_dir, font, ppi)
        if mm_to_px(len_in_dir,1)>int(max_px):
            pos_list = np.array([m.start() for m in re.finditer(r"[\\/]", in_dir)])
            list_len = [mm_to_px(str_size_mm(in_dir[0:pos_slash], font, ppi)[0],1)
                        for pos_slash in pos_list ]
            try:
                pos_mid = pos_list[np.min(np.where(np.array(list_len) >= int(max_px))) - 1]
            except:
                pos_mid = pos_list[-1]
            out_dir1 = str(in_dir)[0:pos_mid]
            out_dir2 = str(in_dir)[pos_mid:]

        else:
            out_dir1 = str(in_dir)
            out_dir2 = ''

        return (out_dir1,out_dir2)

    def outdir_folder_choice():
        '''The function `outdir_folder_choice' allows the interactive choice of a folder, 
        puts it in the `out_dir` global variable and prints the result in the `folder_choice` frame.

        '''
        # Standard library imports
        import numpy as np

        global out_dir

        out_dir = filedialog.askdirectory(initialdir=in_dir,title=titles['main'])
        
        out_dir_split = [out_dir]
        while out_dir_split[len(out_dir_split)-1]!='':
            out_dir1,out_dir2 = split_path2str(out_dir_split[len(out_dir_split)-1],frame_widthpx,text_font,ppi)
            out_dir_split[len(out_dir_split)-1] = out_dir1
            out_dir_split.append(out_dir2)

         # Create the folder-result frame and set its geometry 
        folder_result = tk.LabelFrame(master=win,              
                        text=titles['result'],
                        font=frame_font)
        folder_result.place(x=frame_xpx,
                            y=frame_ypx,
                            width=frame_widthpx,
                            height=frame_heightpx)

         # Edit the selected folder        
        text_max_widthmm = str_max_len_mm(out_dir_split, text_font, ppi)
        text_xmm = (frame_widthmm - text_max_widthmm) / 2
        text_xpx = mm_to_px(text_xmm - mm_size_corr,1)
        text_ypx = mm_to_px(frame_unit_heightmm,1)       
        text = '\n'.join(out_dir_split)
        folder_label = tk.Label(folder_result, text=text, font=text_font)
        folder_label.place(x=text_xpx,
                           y=text_ypx)
    
    def help():
        messagebox.showinfo('Folder selection info', '')
    
    ############# Local parameters setting #############  
    
     # Get the ppi of the selected prime display
    ppi = DISPLAYS[prime_disp]['ppi']
    
     # Check the number of frames and buttons
    frames_nb = len(titles) -1 
    buttons_nb = len(buttons_labels)
    if frames_nb!=1 or buttons_nb!=2:
        print('Number of titles:', len(titles) )
        print('Number of buttons:', len(button_labels) )
        print('The number of titles should be 2 and the number of buttons should be 2')
    
     # Set the ratio of frames-width to the titles-max-width
    frame_ratio = widget_ratio
    
     # Set the ration of window-width to the frame-width
    win_ratio = widget_ratio 
    
     ####### TO DO: define the following values as globals
     # Set the buttons-height to the label-height ratio to vertically center the label in the button
    button_ratio = 2.5
    
     # Set a potential ratio for correcting the conversion of mm to px for the buttons sizes
     # Todo: adapt these ratios to correct the discrepancy between the set mm sizes 
     # and the effective mm sizes on the screen for MacOs 
     # (correction still to be understood)
    buttonsize_mmtopx_ratios = (1,1,1)
    
     # Set the value in mm for the correction of the sizes in milimeters 
     # before use for computing the widgets horizontal positions in pixels 
     # (correction still to be understood)
    mm_size_corr = 1
    
     # Set the maximum lines number for editing the selected folder name
    max_lines_nb = 3 
    
    ############# Tkinter window management #############
    
     # Create the tk window
    win = tk.Tk()
    win.attributes("-topmost", True)
    win.title(titles['main']) 
    
     # Set the fonts to be used
    frame_font = TkFont.Font(family='arial', size=16, weight='bold')
    text_font = TkFont.Font(family='arial', size=12, weight='normal')
    button_font = TkFont.Font(family='arial', size=12, weight='normal')
    
     # Computes the maximum size in mm of the list of titles
    titles_mm_max = str_max_len_mm(titles.values(), frame_font, ppi)
    
     # Computes button sizes in mm and pixels using button label sizes and button_ratio
     # Buttons width is the button heigth added to the labels width to horizontally center the label in the button 
    labels_widthmm = [str_size_mm(buttons_labels[i],button_font, ppi)[0] for i in range(buttons_nb)]
    label_heightmm = str_size_mm(buttons_labels[0],button_font, ppi)[1]
    button_heightmm =  label_heightmm * button_ratio
    buttons_widthmm = (labels_widthmm[0] + button_heightmm, labels_widthmm[1] + button_heightmm)
    buttons_widthpx = (mm_to_px(buttons_widthmm[0],buttonsize_mmtopx_ratios[0]), 
                       mm_to_px(buttons_widthmm[1],buttonsize_mmtopx_ratios[1]))
    button_heigthpx = mm_to_px(button_heightmm,buttonsize_mmtopx_ratios[2])

     # Computes the frame width in pixels from titles maximum size in mm using frame_ratio
    frame_widthmm = titles_mm_max * frame_ratio    
    frame_widthpx = str(mm_to_px(frame_widthmm,1))

     # Computes the window width in pixels from the frame width and buttons width using win_ratio
    win_widthmm = max(frame_widthmm,sum(buttons_widthmm)) * win_ratio 
    win_widthpx = str(mm_to_px(win_widthmm,1))

     # Computes the buttons horizontal positions in pixels 
     # assuming 2 buttons and with correction of size in mm by mm_size_corr value
    padx_ratio = buttons_nb * 2  
    pad_xmm = (win_widthmm - min(frame_widthmm,sum(buttons_widthmm))) / padx_ratio
    buttons_xmm = (pad_xmm, buttons_widthmm[0] + 3 * pad_xmm)
    buttons_xpx = (mm_to_px(buttons_xmm[0] - mm_size_corr,1), mm_to_px(buttons_xmm[1] - mm_size_corr,1))

     # Computes the frames heigth unit
    _, text_heigthmm = str_size_mm('Users/',text_font, ppi)
    frame_unit_heightmm = min(button_heightmm,text_heigthmm) 
    print('frame_unit_heightmm:',frame_unit_heightmm)

     # Computes the buttons vertical position in pixels
    button_ymm = frame_unit_heightmm 
    button_ypx = mm_to_px(button_ymm,1)

     # Computes the frame heigth in mm and in pixels 
    pads_nb = 4  # 2 frame units above and 2 frame units under the edited text 
    max_frame_unit_nb = pads_nb + max_lines_nb  
    frame_heightmm = frame_unit_heightmm * max_frame_unit_nb
    frame_heightpx = str(mm_to_px(frame_heightmm,1))

     # Computes the frame positions in pixels
    frame_xmm = (win_widthmm - frame_widthmm) / 2
    frame_ymm = button_ymm + button_heightmm + 2 * frame_unit_heightmm
    frame_xpx, frame_ypx = mm_to_px(frame_xmm,1), mm_to_px(frame_ymm,1)

    # Computes the window heigth in mm and in pixels 
    # with frame_unit_heightmm separating vertically the widgets
    win_heightmm = button_ymm + button_heightmm + frame_heightmm + 3 * frame_unit_heightmm
    win_heightpx = str(mm_to_px(win_heightmm,1))

     # Set the window geometry
    win_xpx = str(int(DISPLAYS[prime_disp]['x']) + 50)
    win_ypx = str(int(DISPLAYS[prime_disp]['y']) + 50)
    win.geometry(f'{win_widthpx}x{win_heightpx}+{win_xpx}+{win_ypx}')

     # Create the folder result frame and set its geometry 
    folder_result = tk.LabelFrame(master=win,              
                text=titles['result'],
                font=frame_font)
    folder_result.place(x=frame_xpx,
                    y=frame_ypx,
                    width=frame_widthpx,
                    height=frame_heightpx)

     # Create the button for folder selection
    select_button = tk.Button(win,
                          text=buttons_labels[0],
                          font=button_font,
                          command=outdir_folder_choice)
    select_button.place(x=buttons_xpx[0], 
                    y=button_ypx, 
                    width=buttons_widthpx[0], 
                    height=button_heigthpx)

     # Create the help button
    help_button = tk.Button(win,
                        text=buttons_labels[1],
                        font=button_font,
                        command=help)
    help_button.place(x=buttons_xpx[1], 
                  y=button_ypx, 
                  width=buttons_widthpx[1], 
                  height=button_heigthpx)

    win.mainloop()
    
    return out_dir