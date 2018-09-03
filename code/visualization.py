import matplotlib.pyplot as plt
import numpy as np
directoryin=("//home//victor//Neo4j_version//2_months_benchmark//Pa3_0.6//")
directoryout=("//home//victor//Neo4j_version//2_months_benchmark//Deep_analysis//Botnet_final//Pa4_0.15//")
maxdraw=5000    #the maximum number of ip addresses to draw on each fingerprint graph
sizes=[]
infile=open(directoryin+"ip_hash.txt")
#count=0 #to count how many ip addresses we have drawn
current_size=0 #the size of the current fingerprint
for line in infile:    #each line represents the activity of an ip address. Each number in a line is
                #the id of an OAE. at the end of a gang, there is a mark in the form of "gang_end\[id of gang]"
    if(line=='\n'):
        break    #another possible scoring method: break the 17350 groups into smaller chunks
    if(line[0]=='g'): #and calculate the dirtribution of the number of times
        line,gangid=line.split('\\')
        axis=[0,0,0,17350] #axis feature for matplotib, in terms of: [xmin,xmax,ymin,ymax]
        axis[1]=current_size
        plt.axis(axis)
        plt.xlabel("ID number of bot")
        plt.ylabel("ID number of OAE")
        #plt.figure(figsize=(90,int(current_size/100)))      individual ip addresses in a gang
        plt.title("Attack fingerprint of a gang")         #attack in each chunk. If there is a
        plt.savefig(directoryout + "fingerprint_"+gangid+".jpeg",dpi=220) #obvious peak,
        plt.close()                         #everything is good, but if there is not an obvious peak,
        current_size=0                      #or if there are multiple peaks, the gang is not good.
        print("Hey!")
        continue
    if(current_size<maxdraw):
        line=line.strip(" \n") #there is always a stray \n at the end
        #the real business starts here
        if(not line.endswith('empty')): #empty is an marker signalling that the ip address
            activity=np.array(map(int,line.split(' '))) #should not be plotted
            tmp=[]
            tmp.append(current_size)
            tmp=tmp*int(activity.shape[0])    #this step ensures the dimensions of tmp and activity are
            plt.plot(tmp,activity,"r.",markersize=2)         #the same
        current_size+=1
#plt.show()
infile.close()
