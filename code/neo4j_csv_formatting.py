directory="//Users//Victor//Documents//groups_zz//" #directory to the zz files
directory="//media//victor//SSD//IP_Gang//Complexity_analysis//groups_zz//"
outgroups=open("groups.csv",'w')
outips=open("ips.csv",'w')
outrelationships=open("relationships.csv",'w')
outrelationships_reverse=open("relationships_reverse.csv",'w')

outgroups.write("id:ID(groups),target,time,totby,totpa,maxby,maxpa,size,\n")
outips.write("ip:ID(ips),\n")
outrelationships.write(":START_ID(ips),:END_ID(group),\n")
outrelationships_reverse.write(":START_ID(group),:END_ID(ips),\n")

#Note: the documentation for the "neo4j-admin import" command are here: https://neo4j.com/docs/operations-manual/current/tools/import/ and https://neo4j.com/docs/operations-manual/current/tutorial/import-tool/
#The exact command I used was:
#bin/neo4j-admin import --mode=csv --database="graph.db" --id-type=string --nodes:groups="/Users/Victor/Documents/neo4j-community-3.2.2/import/groups.csv" --nodes:ips="/Users/Victor/Documents/neo4j-community-3.2.2/import/ips.csv" --relationships:BELONGS_TO="/Users/Victor/Documents/neo4j-community-3.2.2/import/relationships.csv" --relationships:CONTAINS="/Users/Victor/Documents/neo4j-community-3.2.2/import/relationship_reverse.csv"

count=0

for i in range(0,4001): #configuration: set the range to the number of OAEs you want to import plus one
    filename="zz"+str(i)+".txt"
    f=open(directory+filename)
    targ=f.readline()
    time=f.readline()
    totby=f.readline()
    totpa=f.readline()
    maxby=f.readline()
    maxpa=f.readline()
    time=int(time)
    time=str(time)
    targ=targ.strip('\n\r')
    totby=totby.strip('\n\r')
    totpa=totpa.strip('\n\r')
    maxby=maxby.strip('\n\r')
    maxpa=maxpa.strip('\n\r')
    outgroups.write(str(i))
    outgroups.write(',')
    outgroups.write(targ)
    outgroups.write(',')
    outgroups.write(time)
    outgroups.write(',')
    outgroups.write(totby)
    outgroups.write(',')
    outgroups.write(totpa)
    outgroups.write(',')
    outgroups.write(maxby)
    outgroups.write(',')
    outgroups.write(maxpa)
    outgroups.write(',')
    for line in f:
        if(line=='\n\r'):
            continue
        line=line.strip('\n\r')
        #count+=1
        #outips.write(str(count))
        #outips.write(',')
        a,b,c,d,e=line.split(' ')
        if(e[len(e)-3]=='r'):
            e=e.strip(e[len(e)-2]+e[len(e)-1])
            print("Hey!")
            print(e)
        outips.write(e)
        outips.write(',\n')
        #outrelationships.write(str(count))
        #outrelationships.write(',')
        outrelationships.write(e)
        outrelationships.write(',')
        outrelationships.write(str(i))
        outrelationships.write(",\n")
        outrelationships_reverse.write(str(i))
        outrelationships_reverse.write(',')
        outrelationships_reverse.write(e)
        outrelationships_reverse.write(",\n")
        count+=1
    outgroups.write(str(count))
    outgroups.write(',\n')
    f.close()
    count=0
outgroups.close()
outips.close()
outrelationships.close()

outrelationships_reverse.close()


