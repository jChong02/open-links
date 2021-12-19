import tkinter as tk
import os
import webbrowser
import re
from functools import partial

#dict used to hold search term - url pairs
searchURLS = {}

#regex to identify if website or search term
regex = re.compile(
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    
#adds search to list of search terms
def handle_add(event):
    searchQuery = ent_search.get()
    if searchQuery:
        url = re.findall(regex, searchQuery)
        if(url):
            searchURLS.update({searchQuery: url[0]})
        else:
            searchURL = "https://www.google.com/search?q=" + searchQuery
            searchURLS.update({searchQuery:searchURL})
    ent_search.delete(0, tk.END)
    update_queries()
    
    
#removes search term from list of search terms
def handle_delete(query):
    deleted = searchURLS.pop(query)
    update_queries()
    

def update_queries():
    clearEmptyError()
    
    #removes frame of search terms if none exist
    if not searchURLS:
        frm_queries.grid_forget()
        return
    
    #removes each search term to refresh
    for widget in frm_queries.winfo_children():
        widget.destroy()

    #adds each search term and corresponding delete button
    count=0
    for query,url in searchURLS.items():
        label = tk.Label(master=frm_queries,text=query)
        delQuery = partial(handle_delete, query)
        btn = tk.Button(master=frm_queries,text="Delete",command=delQuery)
        label.grid(row=count, column=0)
        btn.grid(row=count, column=1)
        count+=1
    frm_queries.grid(row=1,pady=(0,10))
    frm_execute.grid(row=2)
    

def execute_search():
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    
    clearEmptyError() 
    
    if not searchURLS:
        label = tk.Label(master=frm_execute, text="Error: No items to search", fg="Red")
        label.grid()        
    else:
        for url in searchURLS.values():
            webbrowser.get(chrome_path).open_new_tab(url)        
        
    
    
def clearEmptyError():
    for widget in frm_execute.winfo_children() or searchURLS:
        if isinstance(widget, tk.Label):
            widget.destroy()       


window = tk.Tk()
window.grid_columnconfigure(0, weight=1)
window.title("Open links")



frm_search = tk.Frame(master=window)
frm_queries = tk.Frame(master=window, relief=tk.SUNKEN, borderwidth=3)
frm_execute = tk.Frame(master=window)


lbl_search = tk.Label(master=frm_search, text="Enter a search term or a link:")
lbl_search.grid(row=0, column=0)


ent_search = tk.Entry(master=frm_search)
ent_search.bind('<Return>', handle_add)
ent_search.grid(row=1, column=0)


btn_add = tk.Button(master=frm_search, text="Add")
btn_add.grid(row=1, column=1)
btn_add.bind("<Button-1>", handle_add)

btn_executeSearch = tk.Button(master=frm_execute, text="Execute Search",command=execute_search)
btn_executeSearch.grid()


frm_search.grid(row=0,pady=(0,10))

window.mainloop()
