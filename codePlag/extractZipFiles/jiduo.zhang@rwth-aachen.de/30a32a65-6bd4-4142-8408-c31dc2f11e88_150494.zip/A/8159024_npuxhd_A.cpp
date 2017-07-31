#include <iostream>
#include<stdio.h>
#include<algorithm>
#include<string.h>
using namespace std;
char s1[100000],s2[100000];
int a[100000];
int main()
{
    scanf("%s%s",s1,s2);
    int len2,len1,k,i,j,temp1,temp2;
    len1=strlen(s1);
    len2=strlen(s2);
    memset(a,0,sizeof(a));
    for(i=0;i<len1;i++)
    {
        temp1=s1[i]-'0';
        for(j=0;j<len2;j++)
        {
            temp2=s2[j]-'0';
            k=0;
            a[0]+=(temp1*temp2);
            while(a[k]>=10)
            {
               a[k+1]+=(a[k]/10);
               a[k]=a[k]%10;
               k++;
            }
        }
    }
    int sus=0;
    for(int i=k+10;i>=0;i--)
    {
        if(a[i]==0&&sus==0) continue;
        else
        {
            sus++;
            printf("%d",a[i]);
        }

    }
    printf("\n");
    return 0;
}