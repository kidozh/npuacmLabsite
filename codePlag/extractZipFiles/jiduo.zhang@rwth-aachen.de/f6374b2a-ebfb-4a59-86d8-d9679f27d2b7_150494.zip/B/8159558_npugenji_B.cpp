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
    for (i=n;i>=1;i--)
        for (j=i;j<=n;j++)
            dp[i][j]=max(dp[i+1][j]+a[i]*(n-j+i),dp[i][j-1]+a[j]*(n-j+i));
    printf("%lld",dp[1][n]);
    return 0;
}
