//By Sean Chen
#include <iostream>
#include <cstdio>
#include <cstring>

using namespace std;

int n;
int ans[100005],tp;
int main()
{
    scanf("%d",&n);
    while(n)
    {
        int k=n%(-2);
        int t=n/(-2);
        if (k<0)
        {
            k+=2;
            t++;
        }
        n=t;
        tp++;
        ans[tp]=k;
    }
    for (int i=tp;i>=1;i--)
        printf("%d",ans[i]);
    if (tp==0)
        printf("0");
    return 0;
}