//By Sean Chen
#include <iostream>
#include <cstdio>
using namespace std;
int dp[2005][2005],a[2005];
int n;
int max(int a,int b)
{
    if (a>b)
        return a;
    return b;
}
int main()
{
    
	scanf("%d",&n);
	for(int i=1;i<=n;i++)
        scanf("%d",&a[i]);
	for(int i=1;i<=n;i++)
        dp[i][i]=n*a[i];
	for(int i=n-1;i>0;i--)
        for(int j=i+1;j<=n;j++)
            dp[i][j]=max(dp[i+1][j]+(n-j+i)*a[i],dp[i][j-1]+(n-j+i)*a[j]);
	printf("%d\n",dp[1][n]);
	return 0;
}
