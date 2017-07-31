#include <iostream>
#include <queue>
#include <cstdio>
#include <algorithm>
using namespace std;
long long dp[2020][2020];
int a[2020];
int main()
{
    int n,i,j;
    scanf("%d",&n);
    for (i=1;i<=n;i++)
    {
        scanf("%d",&a[i]);
        dp[i][i]=a[i];
    }
    for (i=1;i<=n;i++)
        for (j=i;j>=1;j--)
          dp[j][i]=max(dp[j+1][i]+a[j]*(n-i+j),dp[j][i-1]+a[i]*(n-i+j));
    printf("%lld",dp[1][n]);
    return 0;
}
