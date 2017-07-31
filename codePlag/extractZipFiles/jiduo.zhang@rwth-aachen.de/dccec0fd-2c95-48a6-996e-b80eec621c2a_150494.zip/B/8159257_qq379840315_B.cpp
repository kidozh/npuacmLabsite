#include<iostream>
#include<cmath>
#include<cstdio>
#include<iomanip>
#include<cstring>
#include<stdlib.h>
#include<string>
#include<algorithm>
#include<queue>
using namespace std;
int s[3000];
int dp[3000][3000];
int main()
{
	int n;
	scanf("%d",&n);
			for(int i=1;i<=n;i++)
			scanf("%d",&s[i]);
		memset(dp,0,sizeof dp);
		dp[1][0]=s[1];
		dp[0][1]=s[n];
		int sum=-1;
		for(int i=0;i<=n;i++)
		{
			for(int j=0;j<=n;j++)
			{
				if(i>=1&&j>=1)dp[i][j]=max(dp[i-1][j]+s[i]*(i+j),dp[i][j-1]+s[n-j+1]*(i+j));
				else if(j>=1) dp[i][j]=max(dp[i][j],dp[i][j-1]+s[n-j+1]*(i+j));
				else if(i>=1)dp[i][j]=max(dp[i-1][j]+s[i]*(i+j),dp[i][j]);
			}
		}
		for(int i=0;i<=n;i++)
		{
			if(dp[i][n-i]>sum)sum=dp[i][n-i];
		}
		printf("%d\n",sum);
	return 0;
}
