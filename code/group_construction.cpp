#include <cstring>
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
using namespace std;
#define alpha 1
#define beta 50

int main()
{
    int item=0,groupb=0,grouptot=0,ingroup=0,groupcur=1,tstart=0,tcur,groupb_e=0;    //ingroup:size of current group. groupcur:column number
    string atkip,atkip_start="0",cur,filename="z0.txt";                          //of current string
    const char * tmp;
    char curc[50]; //curc=curchar
    //freopen("ddos_short.csv","r",stdin); //check out what a stream is and why anything other stdin does not work
    //getline(&cur,50,',');
    ifstream infile;
    ofstream outfile;
    infile.open("ddos_long.csv");
    infile.getline(curc,50,',');
    cur=string(curc);
    cout << cur << endl;
    outfile.open("z0.txt");
    while(infile)
    {
        switch(groupcur)
        {
            case 6:
            {
                outfile << cur << ' ';
                //cout << cur << ' ';
                break;
            }
            case 7:
            {
                outfile << cur << ' ';
                //cout << cur << ' ';
                break;
            }
            case 8:
            {
                outfile << cur << ' ';
                break;
            }
            case 9:
            {
                outfile << cur << ' ';
                break;
            }
            case 10:
            {
                //cout << "cur" << cur <<endl;
                tcur=(((cur[11]-'0')*10+(cur[12]-'0'))*60)+((cur[14]-'0')*10)+(cur[15]-'0');
                //tcur=(((cur[8]-'0')*10+(cur[9]-'0'))*60)+((cur[11]-'0')*10)+(cur[12]-'0');
                //cout << "tcur" << tcur << endl;
                break;
            }
            case 12:
            {
                atkip=cur;
                outfile << cur << ' ';
                break;
            }
            case 19:
            {
                outfile << cur << "AA" << endl;
                break;
            }
            case 24:
            {
                if(((tcur-tstart)>-(alpha))&&(tcur-tstart<alpha)&&(atkip==atkip_start)) {ingroup++;}
                else if(ingroup>beta)
                {
                    groupb++;
                    grouptot++;
                    groupb_e+=ingroup;
                    ingroup=1;
                    tstart=tcur;
                    atkip_start=atkip;

                    itoa(groupb,curc,10);
                    filename="z"+string(curc)+".txt";
                    tmp=filename.c_str();
                    outfile.close();
                    outfile.open(tmp);
                }
                else
                {
                    grouptot++;
                    ingroup=1;
                    tstart=tcur;
                    atkip_start=atkip;

                    tmp=filename.c_str();
                    outfile.close();
                    outfile.open(tmp);
                }
                item++;
                if(item%500000==0) {cout << "_";}
                groupcur=0;
            }
        }
        //if(item==100) {break;}
        groupcur++;
        //tmp=getchar();
        //while(tmp!=',') {cur[cur.length()]=tmp;tmp=getchar();}
        infile.getline(curc,50,',');
        cur=string(curc);
    }
    if (ingroup>beta) {groupb++;grouptot++;groupb_e+=ingroup;}
    else grouptot++;
    cout << endl << "groupb" << groupb;
    cout << endl << "average group size:" << item/grouptot;
    cout << endl << "average large group size:" << groupb_e/groupb;
    cout << endl << "number of large groups:" << groupb;
    cout << endl << "number of groups:" << grouptot;
    cout << endl << "item total:" << item;
    infile.close();
    return 0;
}
