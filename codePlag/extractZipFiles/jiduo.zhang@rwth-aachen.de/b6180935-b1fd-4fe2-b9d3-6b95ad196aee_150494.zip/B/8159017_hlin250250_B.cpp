#include <iostream>
#include<cstdio>
#include<cstdlib>
#include<algorithm>
#include<cmath>
#include<cstring>
using namespace std;
const int N = 2333;
int dp[N][N];
int tmp[N];
int main()
{
    int n;
    while(~scanf("%d", &n))
    {
        memset (dp, 0, sizeof(dp));
        for (int i = 1; i <= n; ++i)
        {
            scanf("%d", &tmp[i]);
            dp[i][i] = tmp[i];
        }
        for (int i = n; i >= 1; --i)
        {
            for (int j = i; j <= n; ++j)
            {
                dp[i][j] = max(dp[i + 1][j] + tmp[i] * (n - (j - i + 1) + 1), dp[i][j - 1] + tmp[j] *(n - (j - i + 1) + 1) );
            }
        }
        printf("%d\n", dp[1][n]);
    }
    return 0;
}
