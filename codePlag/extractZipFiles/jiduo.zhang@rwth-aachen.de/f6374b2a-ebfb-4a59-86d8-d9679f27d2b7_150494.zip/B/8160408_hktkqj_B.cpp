#include<cstdio>  
#define max(a,b) ((a)>(b)?(a):(b))  
#define SIZE 2008
int dp[SIZE][SIZE];  
int main()  
{  
    int n,i,j,a[SIZE];  
    scanf("%d",&n);  
    for(i=1;i<=n;i++)  
        scanf("%d",a+i);  
    for(i=n;i>0;i--)
        for(j=i;j<=n;j++)  
        {
        	int day=n+i-j;
            dp[i][j]=max(dp[i+1][j]+a[i]*day,dp[i][j-1]+a[j]*day);  
    	}
    printf("%d\n",dp[1][n]);  
}  