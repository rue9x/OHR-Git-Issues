'''
OHRRPGCE Git Repo Issue Updoot Tabulator
Made for TMC and James, with love.
Rue Lazzaro 7/4/2020
'''

import requests
import os
from pathlib import Path
from io import StringIO
from html.parser import HTMLParser
import sys

issues_url = 'https://api.github.com/repos/ohrrpgce/ohrrpgce/issues'
issues_params = {'state':'open'}
issues_headers = {'accept': 'application/vnd.github.squirrel-girl-preview'}



class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def sort_and_prepare_return_final_list(collection,sortmode):
    final_list = list()
    
    sort_by_mostupvotes = sorted(collection, key=lambda x: (collection[x]['upvotes']), reverse=True)
    sort_by_leastupvotes = sorted(collection, key=lambda x: (collection[x]['upvotes']),reverse=False)
    sort_by_mostdownvotes = sorted(collection, key=lambda x: (collection[x]['downvotes']), reverse=True)
    sort_by_leastdownvotes = sorted(collection, key=lambda x: (collection[x]['downvotes']),reverse=False)
    sort_by_score_highest =sorted(collection, key=lambda x: (collection[x]['score']), reverse=True)
    sort_by_score_lowest =sorted(collection, key=lambda x: (collection[x]['score']), reverse=False)

    if sortmode == "highest_score":
        for each_id in sort_by_score_highest:
            final_list.append(collection[str(each_id)])
    elif sortmode == "lowest_score":
        for each_id in sort_by_score_lowest:
            final_list.append(collection[str(each_id)])
    elif sortmode == "most_upvotes":
        for each_id in sort_by_mostupvotes:
            final_list.append(collection[str(each_id)])
    elif sortmode == "least_upvotes":
        for each_id in sort_by_leastupvotes:
            final_list.append(collection[str(each_id)])
    elif sortmode == "most_downvotes":
        for each_id in sort_by_mostdownvotes:
            final_list.append(collection[str(each_id)])
    elif sortmode == "least_downvotes":
        for each_id in sort_by_leastdownvotes:
            final_list.append(collection[str(each_id)])
    else:
        # I guess let's default to highest score?
        for each_id in sort_by_score_highest:
                final_list.append(collection[str(each_id)])

    return final_list


def get_issues(URL=issues_url,PARAMS=issues_params,HEADERS=issues_headers):
    r = requests.get(url = URL, params = PARAMS, headers=HEADERS) 
    issues_r_data = r.json()

    return issues_r_data

def dictify_git(issues_r_data):
    issues_data = dict()
    for each in issues_r_data:
        issue_url = each["url"]
        comments_url = each["comments_url"]
        issue_id = issue_url
        issue_id = issue_id.replace('https://api.github.com/repos/ohrrpgce/ohrrpgce/issues/',"")
        issue_id = issue_id.replace("/comments","")

        try:
            issue_upvotes = each["reactions"]["+1"]
        except:
            issue_upvotes = 0
        
        try:
            issue_downvotes = each["reactions"]["-1"]
        except:
            issue_downvotes = 0

        label = "bug"
        try:
            for each_label in each["labels"]:
                if "feature" in each_label["name"]:
                    label = "new_feature"
        except:
            pass
        title = each["title"]
        title = title.replace(","," ")
        title = title.replace("\\","")
        title = strip_tags(title)
        issues_data[str(issue_id)] = dict()
        issues_data[str(issue_id)]["issue_id"] = issue_id
        issues_data[str(issue_id)]["title"] = title
        issues_data[str(issue_id)]["upvotes"] = issue_upvotes
        issues_data[str(issue_id)]["downvotes"] = issue_downvotes
        issues_data[str(issue_id)]["label"] = label
        issues_data[str(issue_id)]["url"] = 'https://github.com/ohrrpgce/ohrrpgce/issues/'+str(issue_id)
        
        issues_data[str(issue_id)]["score"] = issue_upvotes - issue_downvotes
    return issues_data

def write_csv(final_list: list, writefolder='',writefile='OHR-issues.csv',which_label='bug'):
    try:
        with open(writefolder+writefile,'w') as file_out:
            file_out.write("ID,title,up,down,url\n")
            print ("Wrote headers...")
    except:
        print ("Couldn't write file to "+writefolder+"! Exiting!")
        quit()

    with open(Path(writefolder+writefile),'a') as file_out:
        for each_line in final_list:              
            if which_label in each_line["label"]:
                # Split this into multiple lines to make it more readable.
                issue_id = each_line["issue_id"]
                title = each_line["title"]
                upvotes = each_line["upvotes"]
                downvotes = each_line["downvotes"]
                visit_url = each_line["url"]
                writedata = f'{issue_id},{title},{upvotes},{downvotes},{visit_url}\n'
                file_out.write(str(writedata))
                print ("Wrote "+str(issue_id)+" to "+writefile)
    print ("Done writing CSV")

def write_html(final_list: list, writefolder='',writefile='ohr-issues.html'):
    with open(Path(writefolder+writefile),'w') as file_out:
        style_text = \
            "<style>\n"+\
            "table, th, td {\n"+\
            "border: 1px solid black;\n"+\
            "}\n"+\
            "</style>\n\n"

        header_text = \
        "<head> \n" + \
        "<title> OHRRPGCE Issues </title> \n" + \
        "<h1> OHRRPGCE Issues </h1> <p>\n"+  \
        "</head>\n" 
        
        file_out.write(style_text+header_text)
        file_out.write("<body>\n<h2> Issues </h2> \n <p> \n <table id=\"issue_table\" width=\"1000px\">\n")
    with open(Path(writefolder+writefile),'a') as file_out:  
        file_out.write(f"\t<tr id=\"headers\">\n \t\t<td>issue_id</td>\n \t\t<td>title</td>\n \t\t<td>upvotes</td>\n \t\t<td>downvotes</td>\n \t\t<td>url</td>\n</tr>")             
        for each_line in final_list:
            print (each_line["label"])
            if each_line["label"] == "bug":
                issue_id = each_line["issue_id"]
                title = each_line["title"]
                upvotes = each_line["upvotes"]
                downvotes = each_line["downvotes"]
                visit_url = each_line["url"]
                file_out.write(f"\t<tr id=\"{issue_id}\">\n \t\t<td>{issue_id}</td>\n \t\t<td>{title}</td>\n \t\t<td>{upvotes}</td>\n \t\t<td>{downvotes}</td>\n \t\t<td><a href=\"{visit_url}\" target=\"_blank\">{visit_url}</a></td>\n</tr>")
                print ("Wrote "+str(issue_id))
        file_out.write("</table>\n\n")
                
        file_out.write("\n<h2> Features </h2> \n <table id=\"feature_table\" width=\"1000px\">\n")
        file_out.write(f"\t<tr id=\"headers\">\n \t\t<td>issue_id</td>\n \t\t<td>title</td>\n \t\t<td>upvotes</td>\n \t\t<td>downvotes</td>\n \t\t<td>url</td>\n</tr>")             
        
        for each_line in final_list:
            if each_line["label"] == "new_feature":
                issue_id = each_line["issue_id"]
                title = each_line["title"]
                upvotes = each_line["upvotes"]
                downvotes = each_line["downvotes"]
                visit_url = each_line["url"]
                file_out.write(f"\t<tr id=\"{issue_id}\">\n \t\t<td>{issue_id}</td>\n \t\t<td>{title}</td>\n \t\t<td>{upvotes}</td>\n \t\t<td>{downvotes}</td>\n \t\t<td><a href=\"{visit_url}\" target=\"_blank\">{visit_url}</a></td>\n</tr>")
                print ("Wrote "+str(issue_id))
        file_out.write("</table>\n</body>")
        
def main(fn,sortmode,outputtype):
    git_data = get_issues()
    issues_dict = dictify_git(git_data)
    issues_sorted_dict_list = list()
    issues_sorted_dict_list = sort_and_prepare_return_final_list(issues_dict,sortmode)
    if outputtype == "html":
        write_html(issues_sorted_dict_list,'',fn)
    if outputtype == "csv":
        fn2 = fn
        fn2 = fn.replace(".csv","-features.csv")
        write_csv(issues_sorted_dict_list,'',fn,"bug") # Bug to filter only labels with 'bug'
        write_csv(issues_sorted_dict_list,'',fn2,"feature") # Feature to get 'feature' requests.

def show_help():
    print ("\n")
    print ("Syntax: python3 "+__file__+" path_and_filename sortmode html/csv")
    print ("Where 'path_and_filename is windows or linux friendly folder structure with write access, with a file ending in CSV or HTML")
    print ("Where sortmode is any of the following: ")
    print ("highest_score, lowest_score")
    print("most_upvotes,least_upvotes")
    print("most_downvotes,least_downvotes")
    print ("Where html/csv is html OR csv")
    print ("Note: CSV mode has 2 output files. One will be your original filename. The second is your filename with '-features' appended to it for the feature requests.")
    print ("\n")
    quit()

try:
    if os.path.exists(os.path.dirname(sys.argv[1])) == False or len(sys.argv) < 4:
        show_help()
        quit()
    else:
        fnOK = True
except:
    show_help()
    quit()

fn = sys.argv[1]
sortmode = sys.argv[2]
outputtype = sys.argv[3]

acceptable_sortmodes = [
    'highest_score',
    'lowest_score',
    'most_upvotes',
    'least_upvotes',
    'most_downvotes',
    'least_downvotes'
]
print (sortmode in acceptable_sortmodes)
if outputtype == "csv" or outputtype == "html":
    if outputtype == "csv":
        if fn[-4:] == ".csv":
            outputOK = True
        else:
            print ("Output isn't a csv file.")
            show_help()
            quit()
    if outputtype == "html":
        if fn[-5:] == ".html":
            outputOK = True
        else:
            print ("Output isn't a html file.")
            show_help()
            quit()

if sortmode in acceptable_sortmodes: 
    sortOK = True

if fnOK == True and outputOK == True and sortOK == True:
    print ("gooo")
    main(fn,sortmode,outputtype)
