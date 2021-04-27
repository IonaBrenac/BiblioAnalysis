__all__ = ['item_selection','cooc_selection']

def item_selection() :
    '''
    selection of items for treemaps
    
    Arguments: none
    
    Returns:
        ITEM_CHOICE (string): spectrum/interp spectrum/full spectrum/interp full spectrum

    '''
    import tkinter as tk
    global ITEM_CHOICE
    
    tk_root = tk.Tk()

    item = [
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
    
    ITEM_CHOICE = "subjects"
    def choice(text, v):
        global ITEM_CHOICE
        ITEM_CHOICE = text
        
        
    #
    # choice of the item for treemap
    #
    varitem = tk.IntVar()
    varitem.set(item[0][1])

    tk.Label(tk_root, text='Choose the item for treemap then close the window:').pack(anchor = tk.W)

    for txt, val in item:
        tk.Radiobutton(tk_root, text = txt, variable = varitem, value=val,
            command=lambda t = txt, v = varitem: choice(t, v)).pack(anchor=tk.NW)
    
    #tk.Button(tk_root, text="Quit", command=tk_root.destroy).pack() # works only for Windows
    tk_root.mainloop()
    
    
    return ITEM_CHOICE

def cooc_selection() :
    
    '''
    selection of items for cooccurrences graph treatment
    
    Arguments: none
    
    Returns:
        ITEM_CHOICE (string): item acronyme

    '''
    import tkinter as tk
    
    from .BiblioCooc import AUTHORIZED_ITEMS_DICT
    
    global ITEM_CHOICE
    
    tk_root = tk.Tk()

    item = [(x,i) for i,x in enumerate(AUTHORIZED_ITEMS_DICT.keys())]
    
    ITEM_CHOICE = "subjects"
    def choice(text, v):
        global ITEM_CHOICE
        ITEM_CHOICE = AUTHORIZED_ITEMS_DICT[text]
        
        
    #
    # choice of the item for treemap
    #
    varitem = tk.IntVar()
    varitem.set(item[0][1])

    tk.Label(tk_root, text='Choose the item for treemap then close the window:').pack(anchor = tk.W)

    for txt, val in item:
        tk.Radiobutton(tk_root, text = txt, variable = varitem, value=val,
            command=lambda t = txt, v = varitem: choice(t, v)).pack(anchor=tk.NW)
    
    #tk.Button(tk_root, text="Quit", command=tk_root.destroy).pack() # works only for Windows
    tk_root.mainloop()
    
    
    return ITEM_CHOICE

