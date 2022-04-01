import json
import sys
from tracemalloc import start
import pymongo
from pymongo import MongoClient
#from tsv_2_json import tsv2json
from load_json import connectPort, loadData
import re

    
    
def search_titles(client,db):
    listTconst = []  
    keywords=list(map(str, input("Enter keywords: ").split()))  #it will create a list of all keywords separated by space
    
    p_titles = []
    kk=False

    for k in keywords: #converting string year to int
        try:
            x = int(k)
        except ValueError:
            p_titles.append(k)
            

    cYears = list(set(keywords) - set(p_titles)) 
    col_name = db["title_basics"]
    printed = False
    count = 1
    for i in range(len(keywords)):
        results = col_name.find({'primaryTitle': {'$regex': keywords[i], "$options": 'i'}})#finding keys
        
        for result in results:  
            
            #check result
            unknown = True
            
            for keyword in keywords:
                if keyword.lower() not in result["primaryTitle"].lower(): #comparison
                    unknown = False

            
            if unknown == True and result["tconst"] not in listTconst:# checking if keywords match
                print("\nRESULT {}:".format(count))
                count+=1
                for key, value in result.items(): #printing results
                    print(key, ' : ', value)
                    printed = True
                    listTconst.append(result["tconst"])
    
    for i in range(len(cYears)):
        results = col_name.find({'startYear': {'$regex': cYears[i]}}) #finding keyowrds for start year

        for result in results:  
            print("\nRESULT {}:".format(count))
            
            for key, value in result.items():
                print(key, ' : ', value)#printing output
                count+=1
   
    print("\n\n")
    if printed == False:
        print("No results are there !\n Try with other keywords") #if all keywords not match no results
    elif printed == True:
        while kk== False:
            try:#try and except for other input other than the displayed output
                movie_title = input("Enter a movie title: ")
                #movie_title=movie_title.title() #capitalize
                
                results = col_name.find({'primaryTitle': movie_title})
                

                result_dict = {}

                for i in results: #if primary title is same as movue title get t const
                    if i["primaryTitle"] == movie_title:
                        result_dict[i["primaryTitle"]] = i["tconst"]
                    
                tconst = result_dict[movie_title]
                #print("tconsts are:", len(tconst))    
    
                

                colratings = db["title_ratings"]#making collection

                new_results = colratings.find({'tconst': {'$regex': tconst}}) #finfding t const
                new_results_dict = {}
                for i in new_results:
                    if i["tconst"] == tconst:
                        new_results_dict["averageRating"] = i["averageRating"] #getting the average ratings
                        new_results_dict["numVotes"] = i["numVotes"]

                
                print("AVERAGE RATING: ", new_results_dict['averageRating'])#average rating
                print("NUMBER OF VOTES: ", new_results_dict['numVotes'] )


        

                title_principals_coll = db["title_principals"]
                results = title_principals_coll.find({"tconst": tconst})
                dictN = {}

                for result in results:
                    dictN[result["nconst"]] = result["characters"] #getting n const for names of characters

                
                print('\n')
                print("\nNAMES OF CAST/CREW MEMBERS WHO WORKED AND THEIR CHARACTERS: ")
                for nconst in dictN:
                    colbasics = db["name_basics"]
                    results = colbasics.find({"nconst": nconst})#getting n const for names
                    for result in results:
                        if dictN[nconst] == ['\\N']:
                            print(result["primaryName"]) #getting name of cast
                        else: 
                            print(result["primaryName"], dictN[nconst])#getting name
                print("\n")
                kk = True
            except:
                print("MOVIE NOT PRESENT IN ABOVE MOVIES.\nEnter a movie from above the mentioned movies.") 
                kk =False #if false run again
           
    menu(client,db)
    
    
def searchgenres(client ,db):
    
    colname = db["title_basics"]
    
    genre= input("Enter a genre: ")
    
    regx = re.compile(genre, re.IGNORECASE) #case insensitive
    vote= int(input("Enter minimum number of votes: "))
    
    
    tconst_genres=[]
    result1= colname.find({"genres":regx}) #finding all genres
    for result in result1:
       # print(result['primaryTitle'])
        tconst_genres.append(result['tconst']) #appending t const for all genres into a list
        
    #print("tconst : ",len(tconst_genres))    
   
   
   
    tconst=[]
    colratings = db["title_ratings"]
    #sortedresults=colratings.find().sort("averageRating",1)
    result1= colratings.find({"$expr" : {"$gte" : [{"$toInt" :"$numVotes"} , vote]}})#as votes are strong convert them into a int
    
    for result in result1:
        tconst.append(result['tconst']) #adding t const for all votes in to a list

    #print("tconsts are:", len(tconst))    
    
    count= 1
    temp = set(tconst)
    list3 = [value for value in tconst_genres if value in temp]#finding intersection of 2 lists
    print(len(list3))
    colname = db["title_basics"]
    for i in range(len(list3)):
        result_names=colname.find({"tconst": list3[i]}) #finding common movie
        for result in result_names:
            print(count,".)",result["primaryTitle"])#print the names of desdired movie
            count= count+1
            #print(result["primaryTitle"])


    menu(client,db)


def search_members(client, db, name):
    
        colname = db["name_basics"]
        coltitle = db["title_basics"]
        colprincipals = db["title_principals"]
        count=1

        regx = re.compile(name, re.IGNORECASE)
        results1 = colname.find({"primaryName": regx})#finding nmame
        for result in results1:
            print("Profession: ",result["primaryProfession"])
            nconst = result["nconst"] #geting n  const for names
        try:
            results2 = colprincipals.find({"nconst": nconst})
            for result in results2:
                tconst = result["tconst"]#getting tconst for title
                results3 = coltitle.find({"tconst": tconst}) 
        
                count=count+1
                
                for i in results3:
                    print("RESULT",count)
                    count=count+1
                    print("Title: ",i["primaryTitle"]) #print titles
                    print("Job: ",result["job"])
                    print("Characters: ",end = ' ')
                    for z in result["characters"]:
                        print(z)  
        except:
            print("NO SUCH CAST/CREW MEMBER FOUND TRY AGAIN!")            
                
        menu(client,db)        
                
def addmovie(client,db):
    
    colname = db["title_basics"]
    ID=[]
    unique_id= False
    while unique_id == False:
        mid= str(input("Enter a unique movie ID: "))
        results1 = colname.find({"tconst": mid})#check if uniquw id
        for result in results1:
            ID.append(result["tconst"])
        if mid in ID:
            unique_id=False
            
            
            print("MOVIE ID ALREADY EXITS!\n")
            #mid= str(input("Enter a new unique movie ID :"))
        else:
            unique_id=True    
            
    
        if unique_id :
            title=str(input("Enter movie title : ")) 
            start_year=int(input("Enter movie start year : "))
            running_time=int(input("Enter movie running time  : "))
            genres= list(map(str, input("Enter genres: ").split())) #making list of of multiple genres
            #print("List of genres: ", genres)
            movie="movie"
            
            #inserting 
            colname.insert_one({ "tconst" : mid, "titleType": movie, "primaryTitle": title, "originalTitle": title, "isAdult": "\\N", "startYear": start_year,"endYear":"\\N","runtimeMinutes":running_time,"genres":genres})
            
            print("MOVIE ADDED SUCCESSFULLY !")
    menu(client,db)       

   

def add_member(client, db):
    mid = input("Enter cast/crew member id: ").strip()
    tid = input("Enter title_id: ").strip()
    na = []
    ta = []
    tp = []
    orderlist = []
    category = input("Enter category: ").strip()
    colname = db["name_basics"]

    coltitle = db["title_basics"]  
    for name in colname.find({"nconst": mid}):#checkimg mid
        na.append(name) #adding to list
         
    for title in coltitle.find({"tconst": tid}):
        ta.append(title)
        
    while (len(na) == 0) or (len(ta) == 0): #when empty
        
        mid = input("Incorrect input. Enter cast/crew member id: ").strip()
        tid = input("Enter title_id: ").strip()  
        for name in colname.find({"nconst": mid}):
            na.append(name)
                    
        for title in coltitle.find({"tconst": tid}):
            ta.append(title)    

    principal = db["title_principals"]

    for title_p in principal.find({"tconst": tid}):
        tp.append(title_p)
    if (len(tp) == 0):
        order = 1
        
    else:

        order_query = list(principal.find({"tconst": tid}).sort("ordering")) #sort the ordering 

        for i in range(len(order_query)):
            orderlist.append(int((order_query)[i]['ordering']))#get alkl the orderings of tcosnst
                            
        order = max(orderlist)#gets the max oprder
        
        order = int(order) + 1
    #insert
    principal.insert_one({ "tconst" : tid, "ordering": order, "nconst": mid, "category": category, "job": "\\N", "characters": "\\N"})
    menu(client,db)

def menu(client,db): 
    picked = False
    while picked == False:
        inp = input("Choose an option:\n1.Search for titles\n2.Search for genres\n3.Search for cast/crew members\n4.Add a movie\n5.Add a cast/crew member\n6.exit the program\n")
        if inp == str(1):
            picked = True
            #keys = input("Enter title: ") 
            search_titles(client, db) #if 1 
            
        elif inp == str(2):
            picked=True
            searchgenres(client,db) #if 2
        elif inp == str(3):
            picked = True
            name = input("Enter name: ")
            search_members(client, db, name)  #if 3
        elif inp == str(4):
            picked = True
            addmovie(client,db)#if 4
        elif inp == str(5):
            picked = True
            add_member(client, db) #if 5
        elif inp == str(6):
            sys.exit()
        else:
            print("Please enter a valid option: ") #if 6   
                   
def main():
    
    # title_rating_input = 'title.ratings.tsv'
    # title_rating_output = 'title.ratings.json'

    # tsv2json(title_rating_input,title_rating_output)

    # name_basics_input = 'name.basics.tsv'
    # name_basics_output = 'name.basics.json'

    # tsv2json(name_basics_input,name_basics_output)

    # title_basics_input = 'title.basics.tsv'
    # title_basics_output = 'title.basics.json'

    # tsv2json(title_basics_input,title_basics_output)

    # title_principals_input = 'title.principals.tsv'
    # title_principals_output = 'title.principals.json'

    # tsv2json(title_principals_input,title_principals_output)q
    
    # obtain DB port number
    if len(sys.argv) != 2:
        print("No port given")
        exit(0)
    portNo = sys.argv[1]
    dbName = "291db"
    
    # setup connection to MongoDB
    client, db = connectPort(portNo, dbName)
    # get collections 
    collection = db.list_collection_names()   
    
    # client, db, = loadData(client, db, collection)
    
    menu(client,db)




main()