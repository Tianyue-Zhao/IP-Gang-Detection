def cmp(directory,pa1,pa2,pa3):
#algorithm and functionality
    from neo4j.v1 import GraphDatabase,basic_auth

    totby = [0] * (pa1+1)
    totpa = [0] * (pa1+1)
    maxby = [0] * (pa1+1)
    maxpa = [0] * (pa1+1)
    size=[0]*(pa1+1)
    target = ['a'] * (pa1+1)
    uri="bolt://127.0.0.1:7687"
    driver=GraphDatabase.driver(uri,auth=basic_auth("neo4j","nsfocus2016"))

    #directory="//home//victor//Neo4j_version//"
    raw_data_all=open(directory+"raw_data_all.txt",'w')
    raw_data=open(directory+"raw_data.txt",'w')
    progress=open(directory+"progress.txt",'w')

    with driver.session() as session:
        for i in range(0, pa1 + 1):
            current_group_data = session.run(
                "match(current_group:groups{id:\"" + str(i) + "\"}) return current_group")
            for item in current_group_data:
                try:
                    tmp = item["current_group"]
                    current_group_data = item["current_group"]
                    # print("Hey!")
                except:
                    print("Hey!")
            current_group_data = current_group_data.properties
            totby[i] = current_group_data["totby"]
            totpa[i] = current_group_data["totpa"]
            maxby[i] = current_group_data["maxby"]
            maxpa[i] = current_group_data["maxpa"]
            size[i]=current_group_data["size"]
            target[i]=current_group_data["target"]
        print('B')
        for i in range(0,pa1+1):
            #time.sleep(2)
            if(i%40==0): #configuration needed here as well. This is the progress indicator and rest/sleep part.
                progress.write(str(i)+' ')
                print('_')
                time.sleep(1)
            count={}
            sources=session.run("match(current_group:groups)-[:CONTAINS]->(sources:ips) where (current_group.id=\""+str(i)+"\") return sources.ip")
            for item in sources:
                response=session.run("match(current_ip:ips)-[:BELONGS_TO]->(similar:groups) where (current_ip.ip=\""+item["sources.ip"]+"\") and (not similar.id=\""+str(i)+"\") return similar.id")
                for group in response:
                    group=int(group["similar.id"])
                    if(group in count):
                        count[group]+=1
                    else:
                        count[group]=1
            count=count.items()
            for item in count:    #count records the number of times each group appeared
                #in the outer circle, so here each item is a group.
                other_group=item[0]
                if(size[i]>size[other_group]):  #computing raw score
                    #score=float(item[1])/float(other_size)
                    score=float(item[1])/float(size[other_group])
                else:
                    #score=float(item[1])/float(current_size)
                    score=float(item[1])/float(size[i])

                software_score=0
                if ((totby[i] == totby[other_group]) and (totby[i] != "NO")):  # taking into account the software parameters
                    software_score += 1
                if ((totpa[i] == totpa[other_group]) and (totpa[i] != "NO")):
                    software_score += 1
                if ((maxby[i] == maxby[other_group]) and (maxby[i] != "NO")):
                    software_score += 1
                if ((maxpa[i] == maxpa[other_group]) and (maxpa[i] != "NO")):
                    software_score += 1
                if (target[i] == target[other_group]):
                    software_score += 1

                raw_data_all.write(' '.join([str(i),str(item[0]),str(score),str(software_score)])+'\n')
                # saving raw score for later convenience

                score+=software_score*pa2
                if(score>pa3):
                    #raw_data.write(str(i)+' '+str(item[0])+' '+str(score)+' '+str(software_score)+'\n')
                    raw_data.write(' '.join([str(i),str(item[0]),str(score)])+'\n')
                    #saving complete scores that are above the threshold for later reference in the main function

    raw_data_all.close()
    raw_data.close()
    progress.close()

def simple_threshold(directoryin,directoryout,pa1,pa2,pa3):
    from neo4j.v1 import GraphDatabase, basic_auth
    raw_data_all=open(directoryin+"raw_data_all.txt",'r')
    raw_data=open(directoryout+"raw_data.txt",'w')
    for line in raw_data_all:
        if (line == '\n'):
            break
        stripped = line.strip('\n')
        a, b, score, software_score = stripped.split(' ')
        score = float(score)
        software_score = int(software_score)

        score += software_score * pa2
        if (score > pa3):
            raw_data.write(' '.join(a, b, str(
                score)) + '\n')  # saving complete scores that are above the threshold for later reference in the main function
            # print("OMG",i,item[0],score)

#this is the clustering program that calculates the similarity scores between OAEs and combines OAEs with high similarities to form
#preliminary gangs. use -raw option to actually calculate all over again, and don't use any options to simply run with different threshold.

import time
import argparse
arguments=argparse.ArgumentParser()
arguments.add_argument("-raw",nargs='?',dest="read_only",type=int,const=0,default=1)
args=arguments.parse_args()
#argument parser for -raw argument specifying whether to calculate all over again or not.

print("B")
B_set=[-1]*17351   #configuration here!
pa1 = 4000    #the number of OAEs to be processed
pa2 = 0.025    #the reward for matching software parameters
pa3 = 0.6    #the combining threshold

#directoryout=input("please enter the directory to put the files in\n")
#directoryout="//home//victor//Neo4j_version//2_months_benchmark//Pa3_0.6//"
directoryout="//home//victor//Neo4j_version//test_4000//"
#this is where the generated raw_data.txt and resut files go, no matter if
#a new raw_data_all file is generated or not

if(args.read_only==0):  #start over again and generate a new raw_data_all file
    cmp(directoryout,pa1,pa2,pa3)
else:    #read the raw_data_all from an existing file.
    #This is for changing the threshold parameter quickly.
    #directoryin=input("please enter the directory to read the raw data all file from\n")
    directoryin="//home//victor//Neo4j_version//2_months_benchmark//"
    simple_threshold(directoryin,directoryout,pa1,pa2,pa3)

print("cmp done!\n")
raw_data=open(directoryout+"raw_data.txt",'r')


for line in raw_data:
    if(line=='\n'):
        continue
    line=line.strip('\n')
    i,j,tmp=line.split(' ')
    i=int(i)
    j=int(j)

    if(B_set[i]==-1):    #union-set
        if(B_set[j]==-1):
            B_set[j]=i
            B_set[i]=-2
        else:              #B_set i=-1, j!=-1
            B_set[i]=j
    elif(B_set[j]==-1): #B_set i!=-1, j=-1
        B_set[j]=i
    elif(B_set[i]<-1):   #B_set i<-1,j!=-1
        if(B_set[j]<-1):
            B_set[j]=i    #probably ok here
        else:
            tmp=B_set[j]  #changed this
            while(B_set[tmp]!=-2):
                tmp=B_set[tmp]
            if(tmp!=i):
                B_set[i]=j
    elif(B_set[j]>-1):  #B_set i and j both greater than -1
        tmp1=B_set[j]   #tree top of j
        while(B_set[tmp1]!=-2):
            tmp1=B_set[tmp1]
        tmp2=B_set[i]   #tree top of i
        while(B_set[tmp2]!=-2):
            tmp2=B_set[tmp2]
        if(tmp1!=tmp2):
            B_set[tmp1]=tmp2
    else:               #B_set i geater than -1, j smaller than -1
        tmp=B_set[i]
        while(B_set[tmp]!=-2):
            tmp=B_set[tmp]
        if(tmp!=j):
            B_set[j]=i

print("Done comparing!")
for i in range(0,pa1+1):
    if(B_set[i]>-1):
        tmp=B_set[i]
        while(B_set[tmp]>-2):
            tmp=B_set[tmp]
        B_set[tmp]-=1
        B_set[i]=tmp

outfile1=open(directoryout+"simple_gang.txt",'w')
outfile2=open(directoryout+"specific_gang.txt",'w')
for i in range(0,pa1+1):
    if(B_set[i]<-1):
        outfile1.write(str(-B_set[i]-1))
        outfile1.write('\n')
        #outfile2.write("gang of ")
        outfile2.write(str(i)+',')
        #outfile2.write(':')
        for j in range(0,pa1+1):
            if(B_set[j]==i):
                outfile2.write(str(j))
                outfile2.write(',')
        outfile2.write('\n')
outfile1.close()
outfile2.close()
raw_data.close()
