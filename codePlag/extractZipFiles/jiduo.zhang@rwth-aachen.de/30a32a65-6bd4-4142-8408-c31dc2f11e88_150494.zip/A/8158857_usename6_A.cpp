#include <stdio.h>
#include <stdlib.h>
#include<string.h>
char a[50];
char b[50];
int main()
{
    int n,m,i,j,sum;
    while(scanf("%s%s",a,b)!=EOF)
    {
        sum=0;
        n=strlen(a);
        m=strlen(b);
        for(i=0;i<n;i++)
        {
            for(j=0;j<m;j++)
            {
                sum+=(a[i]-'0')*(b[j]-'0');
            }
        }
        printf("%d\n",sum);
    }
    return 0;
}