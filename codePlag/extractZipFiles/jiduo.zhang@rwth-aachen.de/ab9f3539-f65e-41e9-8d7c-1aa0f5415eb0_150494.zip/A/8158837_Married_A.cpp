#include <cstdio>
#include <cmath>
#include <cstring>
#include <ctime>
#include <iostream>
#include <algorithm>
#include <set>
#include <vector>
#include <sstream>
#include <queue>
#include <typeinfo>
#include <fstream>
#include <map>
#include <stack>
typedef long long ll;
using namespace std;
//freopen("D.in","r",stdin);
//freopen("D.out","w",stdout);
#define sspeed ios_base::sync_with_stdio(0);cin.tie(0)
#define test freopen("test.txt","r",stdin)  
#define maxn 100007
#define eps 1e-9
int Num;
char CH[20];
const int inf = 0x3f3f3f3f;
const int mod = 1e9 + 7;
const ll infll = 0x3f3f3f3f3f3f3f3fLL;
inline ll read()
{
	ll x = 0, f = 1; char ch = getchar();
	while (ch<'0' || ch>'9'){ if (ch == '-')f = -1; ch = getchar(); }
	while (ch >= '0'&&ch <= '9'){ x = x * 10 + ch - '0'; ch = getchar(); }
	return x*f;
}
inline void P(int x)
{
	Num = 0; if (!x){ putchar('0'); puts(""); return; }
	while (x>0)CH[++Num] = x % 10, x /= 10;
	while (Num)putchar(CH[Num--] + 48);
	puts("");
}
//**************************************************************************************

int main()
{
	int a, b;
	while (scanf("%d%d", &a, &b) == 2)
	{
		int num1[10], num2[10], k1 = 0, k2 = 0, ans = 0;
		while (a) num1[k1++] = a % 10, a /= 10;
		while (b) num2[k2++] = b % 10, b /= 10;
		for (int i = 0; i<k1; i++)
		for (int j = 0; j<k2; j++)
			ans += num1[i] * num2[j];
		printf("%d\n", ans);
	}
	return 0;
}