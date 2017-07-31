#include <iostream>
#include<stdio.h>
#include<algorithm>
#include<string.h>
using namespace std;
int a[2005];
int dp[2005][2005];
int main()
{
    int n;
    scanf("%d",&n);
    int ans=0;
    for(int i=1;i<=n;i++)
    {
        scanf("%d",&a[i]);
    }
    memset(dp,0,sizeof(dp));
    for(int i=0;i<=n;i++)
    {
        for(int j=0;j+i<=n;j++)
        {
         if(i==0&&j==0) dp[0][0]=0;
         else if(i==0) dp[i][j]=dp[i][j-1]+(i+j)*a[n-j+1];
         else if(j==0) dp[i][j]=dp[i-1][j]+(j+i)*a[i];
         else dp[i][j]=max(dp[i-1][j]+(i+j)*a[i],dp[i][j-1]+(i+j)*a[n-j+1]);
        }
    }

    for(int i=1;i<=n;i++)
    {
        ans=max(ans,dp[i][n-i]);
    }
    printf("%d\n",ans);
    return 0;
}
