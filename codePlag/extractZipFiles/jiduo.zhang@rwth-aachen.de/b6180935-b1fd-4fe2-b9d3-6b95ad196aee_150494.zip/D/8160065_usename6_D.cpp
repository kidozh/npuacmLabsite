#include <stdio.h>
#include <stdlib.h>
#include<string.h>
#include<math.h>
#define N 100000
int a[N];
int main()
{
    int n,i;
    scanf("%d",&n);
    {
        if(!n)printf("%d\n",0);
        else
        {
            i=0;
            while(n)
            {
                a[i]=n%-2;
                n/=-2;
                if(a[i]<0)
                {
                    a[i]+=2;
                    n++;
                }
                i++;
            }
            i--;
            for(;i>=0;i--)
                printf("%d",a[i]);
        }
    }
    return 0;
}