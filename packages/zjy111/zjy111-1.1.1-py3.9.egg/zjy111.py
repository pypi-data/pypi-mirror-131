"""
This is a modle for print a list.
"""

def print_lol(the_list,tab_count=-1):
    
    """
    The function of print_lol is a test function.
    """
    for term in the_list:
        if(isinstance(term,list)):
            if(tab_count == -1):
                print_lol(term)
            else:
                print_lol(term,tab_count + 1)
        else:
            for i in range(tab_count):
                print("\t",end='')
            print(term)
