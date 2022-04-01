# References: The conversion from json to tsv was done with the help of the sample code provided
import pymongo
import collections
from pymongo import MongoClient
import json


def tsv2json(input_file,output_file):
    arr = []
    file = open(input_file, 'r')
    a = file.readline()
    #print(a)

    # The first line consist of headings of the record
    # so we will store it in an array and move to
    # next line in input_file.
    titles = [t.strip() for t in a.split('\t')]
    #print(titles)
    for line in file:
        
        d = {}
        for t, f in zip(titles, line.split('\t')):

            # Convert each row into dictionary with keys as titles
            if t in ["primaryProfession", "knownForTitles", "genres", "characters"]:
                print(f.strip())
                if "," in f.strip():
                    d[t] = f.strip().split(",")
                    
                else:
                    d[t] = [f.strip()]
            else:
                d[t] = f.strip()
            #print(d)

        # we will use strip to remove '\n'.
        arr.append(d)

        # we will append all the individual dictionaires into list
        # and dump into file.
    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(json.dumps(arr, indent=4))

# Driver Code
title_rating_input = 'title.ratings.tsv'
title_rating_output = 'title.ratings.json'

tsv2json(title_rating_input,title_rating_output)

name_basics_input = 'name.basics.tsv'
name_basics_output = 'name.basics.json'

tsv2json(name_basics_input,name_basics_output)

title_basics_input = 'title.basics.tsv'
title_basics_output = 'title.basics.json'

tsv2json(title_basics_input,title_basics_output)

title_principals_input = 'title.principals.tsv'
title_principals_output = 'title.principals.json'

tsv2json(title_principals_input,title_principals_output)


