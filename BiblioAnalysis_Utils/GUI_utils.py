__all__ = ['item_selection','cooc_selection','merge_database_gui']

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
    ("keywords", 11),
    ("titlewords", 12),
    ("authorskeywords", 13),
]

TREE_MAP_ITEM_HELP_TEXT = '''Select the item you want to deal with.

With MACOS, to exit you have to kill manually the menu window.''' 


COOC_SELECTION_HELP_TEXT = '''In a cooccurrence graph two authors, keywords, sujects 
or more generally two 'items' are linked by an edge if two
authors have coothered an article, if two keywords
names belong to the same article...

To build a cooccurrence graph, you have to select:
                                 - the item used to build cooccurrences graph (default='Authors')
                                 - the minimum size of the node (integer, default=1)
                                 
The node size is the total number of occurences of an author, keyword name,... in the corpus.

With MACOS, to exit you have to kill manually the menu window.''' 

MERGE_DATABASE_HELP_TEXT = '''Merge several databases (wos/scopus) in one database.
You have to choose:
    the database type (wos/scopus)
    the name of the merged database (without extension)
    the input dfolder where the databases are stored
    the output folder where the merged database will be stored
With MACOS, to exit you have to kill manually the menu window.''' 

def item_selection() :
    
    '''
    selection of items for treemaps
    
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
        tk.Button(menu, text="Quit", command=tk_root.destroy).grid(column=0, row=1, padx=8, pady=4)
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
    
    from .BiblioCooc import AUTHORIZED_ITEMS_DICT
    
    global ITEM_CHOICE, minimum_size_node
     
    tk_root = tk.Tk()
    tk_root.title("Graph cooccurrence GUI") 
    
    item_choice = ttk.LabelFrame(tk_root, text=' Label selection ')
    item_choice.grid(column=0, row=0, padx=8, pady=4)
    
    size_choice = ttk.LabelFrame(tk_root, text=' Sieze choice ')
    size_choice.grid(column=1, row=0, padx=8, pady=4)


    
    ITEM_CHOICE = 'AU'  # Default value
    def choice(text, v):
        global ITEM_CHOICE
        ITEM_CHOICE = AUTHORIZED_ITEMS_DICT[text]
    
    minimum_size_node = 1 # Default value
    def submit(): 
        global minimum_size_node
        minimum_size_node = size_entered.get()
    
    def help():
        messagebox.showinfo("cooc selection info", COOC_SELECTION_HELP_TEXT)
        
        
    #                               Choice of the item for the cooccurrence graph
    # -------------------------------------------------------------------------------------------
    item = [(x,i) for i,x in enumerate(AUTHORIZED_ITEMS_DICT.keys())]
    varitem = tk.IntVar()
    #varitem.set(item[0][1])

    ttk.Label(item_choice , 
             text='Choose an item for the co-occurrence graph:').grid(column=0, row=1, padx=8, pady=4)
    
    idx_row = 2
    for  txt, val in item:
        tk.Radiobutton(item_choice, text=txt, variable=varitem, value=val,
            command=lambda t = txt, v=varitem: choice(t, v)).grid(column=0, row=idx_row+2, padx=8, pady=4,sticky=tk.W)
        idx_row += 1
     
    #                                Minmum node size selection
    # -------------------------------------------------------------------------------------------
    name = tk.StringVar()
    ttk.Label(size_choice , 
             text='Choose the minimum \n size of the nodes:').grid(column=0, row=0, padx=8, pady=4)
    size_entered = ttk.Entry(size_choice, width=30, textvariable=name)
    size_entered.grid(column=0, row=1, sticky=tk.W) 
    

    submit_button = ttk.Button(size_choice, text="Submit", command=submit)   
    submit_button.grid(column=1, row=1, padx=8, pady=4) 
    help_button = ttk.Button(size_choice, text="HELP", command=help)
    help_button.grid(column=0, row=2, padx=8, pady=4)
    
    if os.name == 'nt':
        tk.Button(size_choice, text="Quit", command=tk_root.destroy).grid(column=0, row=3, padx=8, pady=4)
    
    tk_root.mainloop()
    
    try:
        minimum_size_node = int(minimum_size_node)
    except: # Takes a default value
        minimum_size_node = 1
    
    
    return ITEM_CHOICE, int(minimum_size_node)
    
def merge_database_gui() :
    
    '''
    Selection of items for cooccurrences graph treatment
    
    Arguments: none
    
    Returns:
        database (string): database type (scopus or wos)
        filename (str): name of the merged database
        in_dir (str): name of the folder where the databases are stored
        out_dir (str): name of the folder where the merged databases will be stored

    '''
    # Standard library imports
    import os
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
    from tkinter import filedialog
    from pathlib import Path

    
    global database, filename, in_dir, out_dir
     
    tk_root = tk.Tk()
    tk_root.title("Graph cooccurrence GUI") 
    
    item_choice = ttk.LabelFrame(tk_root, text=' Database selection ')
    item_choice.grid(column=0, row=0, padx=8, pady=4)
    
    folder_choice = ttk.LabelFrame(tk_root, text=' Folders selection ')
    folder_choice.grid(column=1, row=0, padx=8, pady=4)


    
    database = 'wos'  # Default value
    def choice(text, v):
        global database
        database = text
    
    filename = "essai" # Default value
    def submit(): 
        global filename
        filename = size_entered.get()
        if database == "wos":
            filename = filename + '.txt'
        else:
            filename = filename + '.csv'
    
    def indir_folder_choice():
        global in_dir
        in_dir = filedialog.askdirectory(initialdir=str(Path.home()), title="Select in_dir folder")                                         

    
    def outdir_folder_choice():
        global out_dir
        out_dir = filedialog.askdirectory(initialdir=str(Path.home()), title="Select in_dir folder")   
    
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
        tk.Button(folder_choice, text="Quit", command=tk_root.destroy).grid(column=0, row=6, padx=8, pady=4)
    
    tk_root.mainloop()
    
    
    return database, filename, in_dir, out_dir

