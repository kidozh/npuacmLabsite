#include<stdio.h>
#include<string.h>
#include<iostream>
#include<set>
#include<math.h>
#include<map>
#include<queue>
#include<stack>
#include<algorithm>
using namespace std;
#define maxn 2222
int v[maxn];
int dp[maxn][maxn];
int main(){
	int n;
	scanf("%d",&n);
	for(int i=1;i<=n;i++) scanf("%d",&v[i]);
	dp[1][0]=v[1];
	dp[0][1]=v[n];
	for(int i=0;i<=n;i++){
		for(int j=0;j<=n;j++){
			if(i>=1) dp[i][j]=max(dp[i-1][j]+v[i]*(i+j),dp[i][j-1]+v[n-j+1]*(i+j));
			else dp[i][j]=max(dp[i][j],dp[i][j-1]+v[n-j+1]*(i+j));
		}
	}
	int ans=-1;
	for(int i=0;i<=n;i++){
			ans=max(ans,dp[i][n-i]);
	}
	printf("%d\n",ans);
}