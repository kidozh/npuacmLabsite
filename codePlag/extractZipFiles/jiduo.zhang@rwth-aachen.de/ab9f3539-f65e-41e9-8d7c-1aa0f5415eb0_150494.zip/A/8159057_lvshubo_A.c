#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int f(char c)
{
    return c-'0';
}
int main()
{
    char a[20],b[20];
    int n1,n2,i,j,res;
    while(scanf("%s%s",a,b)!=EOF)
    {
        n1=strlen(a);
        n2=strlen(b);
        for(i=0,res=0;i<n1;i++)
            for(j=0;j<n2;j++)
                res+=f(a[i])*f(b[j]);
        printf("%d\n",res);
    }
    return 0;
}
