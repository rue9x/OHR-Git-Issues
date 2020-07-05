# OHR-Git-Issues
OHRRPGCE Git Repo Issue Updoot Tabulator
Made for TMC and James, with love.
Rue Lazzaro 7/4/2020

This uses the requests library to call out to the github API to gather issues information for the OHRRPGCE engine. An internet connection is required, as well as Python 3.

Syntax: python3 ohrissues.py path_and_filename sortmode html/csv

Where 'path_and_filename is windows or linux friendly folder structure with write access, with a file ending in CSV or HTML

Where sortmode is any of the following:

highest_score, lowest_score

most_upvotes,least_upvotes

most_downvotes,least_downvotes

Where html/csv is html OR csv

Note: CSV mode has 2 output files. One will be your original filename. The second is your filename with '-features' appended to it for the feature requests.


This is intended for use with the OHRRPGCE (Official Hamster Republic Role Play Game Creation Engine) Github account to better track their +1 and -1 issues for prioritization. If you would like to use it with your project, that's totally okay! Drop me a line if you make any cool or meaningful changes.
