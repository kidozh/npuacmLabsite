#include <iostream>
#include<cstdio>
#include<cstdlib>
using namespace std;
int main()
{
    int a,b,n,s,i,j,m;
    scanf("%d%d",&a,&b);
    s=0;
    while(a)
    {
        i=a%10;
        m=b;
        while(m)
        {
            j=m%10;
            s=s+i*j;
            m=m/10;
        }
        a=a/10;
    }
    printf("%d",s);
    return 0;
}
