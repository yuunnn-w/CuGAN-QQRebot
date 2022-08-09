#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
int Matching(char* input,char* other,char* Key)
{

    double score = 0.0;
    char key[100];
    char Q[500];
    char input1[500];
    memset(Q,0x00,sizeof(Q));
    strcpy(Q,other);
    strcat(Q,"\0");
    memset(key,0x00,sizeof(key));
    strcpy(key,Key);
    strcat(key,"\0");
    memset(input1,0x00,sizeof(input1));
    strcpy(input1,input);
    strcat(input1,"\0");
    int ql=strlen(Q);
    int il=strlen(input1);
    int l=fmax(ql,il);
    if(l==ql)
    {
        int match[ql];
        memset(match,0x00,sizeof(match));
        int index=0;
        for(int j=0;j<ql;j++)
        {
            for(int k=index;k<il;k++)
            {
                if(Q[j]==input1[k])
                {
                    match[j]=1;
                    index=k+1;
                    break;
                }
            }
        }
        score=0;
        for(int j=0;j<ql;j++)
        {
            if(j==0)
            {
                if(match[j]==1)score=score+3;
                else score=score-2;
            }
            else
            {
                if(match[j]==1)score=score+3;
                else score=score-2;
                if(match[j-1]==1)score=score+2.5;
            }
        }
    }
    else if(l==il)
    {
        int match[il];
        memset(match,0x00,sizeof(match));
        int index=0;
        for(int j=0;j<il;j++)
        {
            for(int k=index;k<ql;k++)
            {
                if(Q[k]==input1[j])
                {
                    match[j]=1;
                    index=k+1;
                    break;
                }
            }
        }
        score=0;
        for(int j=0;j<il;j++)
        {
            if(j==0)
            {
                if(match[j]==1)score=score+3;
                else score=score-2;
            }
            else
            {
                if(match[j]==1)score=score+3;
                else score=score-2;
                if(match[j-1]==1)score=score+2.5;
            }
        }
    }
    if(strlen(input)>=strlen(key))
    {
        char buf[300];
        memset(buf,0x00,sizeof(buf));
        for(int k=0;k<strlen(input1);k++)
        {
            memset(buf,0x00,sizeof(buf));
            if(k+strlen(key)>strlen(input1))break;
            for(int j=k;j<k+strlen(key);j++)
            {
                buf[j-k]=input1[j];
            }
            strcat(buf,"\0");
            if(strcmp(buf,key)==0)
            {
                //printf("关键词加分:%s\n",W->word[i].key);
                score=score+5;
                break;
            }
        }
    }
    srand((unsigned)time(NULL)+rand());
    srand(rand());
    double a=(rand()/(double)RAND_MAX)*10-5.0;
    score=score+a;
    return score;
}