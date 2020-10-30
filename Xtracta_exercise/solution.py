# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 19:58:33 2020

@author: Piao Ye
"""

import pandas as pd
import json

def load_invoice_data(filepath):
    """

    Parameters
    ----------
    filepath : string
        filepath of the invoice.txt file.

    Returns
    -------
    invoice : DataFrame

    """            
    # Reading data from invoice.txt to a pandas DataFrame
    invoice = pd.DataFrame()
    with open(filepath, encoding='utf8') as f:
        for line in f:
            line = line.replace("'", "\"")
            line_dict = json.loads(line)
            invoice = invoice.append(line_dict, ignore_index=True)
    return invoice


def load_suppliers_data(filepath):
    """

    Parameters
    ----------
    filepath : string
        filepath of the suppliernames.txt file.

    Returns
    -------
    supplier_names : list

    """       
    # Reading data from suppliernames.txt to a pandas DataFrame and turn its 2nd
    # column (contains supplier names) to a list
    suppliers = pd.read_csv(filepath)
    supplier_names = suppliers['SupplierName'].to_list()
    return supplier_names

def find_supplier_name(invoice, supplier_names):
    """

    Parameters
    ----------
    invoice : DataFrame
        output of the load_invoice_data function.
    supplier_names : list
        output of the load_suppliers_data function.

    Returns
    -------
    supplier_names_to_find : list

    """
    # Create an empty list to contain supplier names found in the invoice
    supplier_names_to_find = []
    
    # Group the invoice DataFrame by 'page_id' and 'line_id'
    # Reason: supplier names must found in the same line on the same page
    gb = invoice.groupby(["page_id", "line_id"], as_index=False)
    
    # Access each group in the invoice DataFrame after grouping by 'page_id' and 
    # 'line_id' (i.e. each line), and reset the index to be 'pos_id'
    for group_key in gb.groups.keys():
        group = gb.get_group(group_key).set_index('pos_id', drop=False)
        # Determine the number of words in each line
        num_words = int(group['pos_id'].max()) + 1
        # ngrams is a list of lists to contain 1, 2, ..., num_words grams in a line
        ngrams = [[] for n in range(num_words)]
        # Append all ngrams in a line to the ngrams list
        for i in range(num_words):
            for j in range(num_words):
                term = ""
                if i + j < num_words:
                    for k in range(i, i+j+1):
                        term += group.loc[k, 'word']
                        term += " "
                    ngrams[j].append(term.rstrip())
        # Check if any of the ngrams in a line is found in the supplier_names list
        # If yes, append the ngram to the supplier_names_to_find list
        for lst in ngrams:
            for entry in lst:
                if entry in supplier_names:
                    supplier_names_to_find.append(entry)
    return supplier_names_to_find


if __name__ == '__main__':
    invoice = load_invoice_data(r"C:\Users\Piao Ye\github_repos\tracyyp\Xtracta_exercise\invoice.txt")
    supplier_names = load_suppliers_data(r"C:\Users\Piao Ye\github_repos\tracyyp\Xtracta_exercise\suppliernames.txt")
    supplier_names_to_find = find_supplier_name(invoice, supplier_names)
    # Print the supplier name(s) found in the given invoice               
    print("Supplier names found in the invoice are:", supplier_names_to_find)
       