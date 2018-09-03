# IP Gang Detection

This repository contains my work from my internship with NSFOCUS.

**Please note that the code in this repository is owned by NSFOCUS and should only be used for academic purposes.**

The work is summarized in the conference paper "Detection of IP Gangs: Strategically Organized Bots", which was presented at the 18th International Conference on Data Mining. The paper is available on page 254 of [the proceedings.](https://link.springer.com/book/10.1007/978-3-319-95786-9)

## What the code does
The purpose of the algorithm is best described in the methods section of [the paper.](https://link.springer.com/book/10.1007/978-3-319-95786-9)
The functionality of each piece of code is briefly described here:
1. The packaging module
- group_construction.cpp: C++ code that scans through the initial raw DDoS log and creates Organized Attack Events (OAEs).
- neo4j_csv_formatting.py: utility script that takes OAEs and creates csv files that can be imported by the Neo4j database using [this command.](https://neo4j.com/docs/operations-manual/current/tools/import/)
2. The clustering module
- find_gang_neo4j.py: core clustering code, uses Neo4j (the python api) to rapidly cluster OAEs into OAE clusters, using an algorithm inspired by but distinct from single-linkage clustering.
3. The analysis module
- clean_up_neo4j.py: extracts IP addresses from the OAE clusters, and removes the IP addresses that are not active enough to be of interest. The lists of IP addresses output by this code are the detected IP Gangs.
- visualization.py: uses matplotlib to create *attack fingerprints*, plots that describe the behavior of each gang.
- combine_images.py: utility script that puts fingerprints generated with different configurations side-by-side for comparison. Also uses matplotlib.

## Additional fingerprints
21 IP Gangs were found, as described in the paper, and 21 fingerprints were created.
Due to space constraints, not all fingerprints were included in the paper. All 21 fingerprints are in the "fingerprints" folder of this repository.
