import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg

directory1="//home//victor//Neo4j_version//2_months_benchmark//Deep_analysis//Pa3_0.6//Pa4_0.05//"
directory2="//home//victor//Neo4j_version//2_months_benchmark//Deep_analysis//Pa3_0.6//Pa4_0.1//"
for i in range(1,9):
    picture1=mpimg.imread(directory1+"fingerprint_"+str(i)+".jpeg")
    picture2=mpimg.imread(directory2+"fingerprint_"+str(i)+".jpeg")
    print(picture1.shape)
    print(picture2.shape)
    picture=np.concatenate((picture1,picture2),axis=1)
    print(picture.shape)
    plt.figure(figsize=(16,6))
    plt.imshow(picture)
    plt.savefig(directory1+"fingerprint_combined_"+str(i)+".jpeg",dpi=220)