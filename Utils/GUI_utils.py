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

def treemap_item(item_treemap, file_name_treemap):
    
    # Standard library imports
    import pandas as pd
    import sys
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib import colors
    from pathlib import Path

    # 3rd party imports
    import squarify    # pip install squarify (algorithm for treemap)
        
    df = pd.read_csv(file_name_treemap, sep= ',')
    all_sizes = list(df['count'])
    total_size = len(all_sizes)
    if total_size != 0 : 
        
        request = "Enter the number of items to be used for the treemap " + \
                  "(min = 1, max = " + str(total_size) + "): "
        size_limit = int(input(request))
        sizes = all_sizes[0:size_limit]
        all_labels = list(df['item'])
        labels = all_labels[0:size_limit]
        all_alias = [str(i) for i in range(len(labels))]
        alias = all_alias[0:size_limit]
    
        fig = plt.gcf()
        ax = fig.add_subplot()
        fig.set_size_inches(10, 8)
        norm = colors.Normalize(vmin=min(sizes), vmax=max(sizes))
        colors = [cm.viridis(norm(value)) for value in sizes]
        squarify.plot(sizes=sizes, label=alias, alpha=1, color = colors)
        plt.axis('off')
        plt.title('Frequences for '+ str(size_limit) + ' ' + item_treemap + ' over ' + \
                   str(total_size),fontsize=23,fontweight="bold")
        plt.show()
    
        print(f'{"alias":<6}{item_treemap:<60}{"frequency"}')
        for i in range(0, len(alias)):
            print(f'{alias[i]:<6}{labels[i]:<60}{sizes[i]}')
    
    else:
        print("The selected item is empty")

