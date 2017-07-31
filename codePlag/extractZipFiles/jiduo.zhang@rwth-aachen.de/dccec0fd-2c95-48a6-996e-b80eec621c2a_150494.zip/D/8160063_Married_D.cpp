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
const int inf=0x3f3f3f3f;
const int mod=1e9+7;
const ll infll = 0x3f3f3f3f3f3f3f3fLL;
inline ll read()
{
    ll x=0,f=1;char ch=getchar();
    while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
    while(ch>='0'&&ch<='9'){x=x*10+ch-'0';ch=getchar();}
    return x*f;
}
inline void P(int x)
{
    Num=0;if(!x){putchar('0');puts("");return;}
    while(x>0)CH[++Num]=x%10,x/=10;
    while(Num)putchar(CH[Num--]+48);
    puts("");
}
//**************************************************************************************

// int v[1005];
int main()
{
	// int n;
	// ll ans=0;
	// scanf("%d",&n);
	// for(int i=1;i<=n;i++)
	// 	scanf("%d",v+i);
	// int l=1,r=n;
	// for(int cnt=1;cnt<=n;cnt++)
	// 	if(v[l]<v[r])
	// 		ans+=cnt*v[l++];
	// 	else ans+=cnt*v[r--];
	// printf("%lld\n",ans );
	// int num,ans[33],k=0,p=0;
	// scanf("%d",&num);
	// if(num==0) return puts("0"),0;
	// bool pos=(num>0);num=pos?num:-num;
	// while(num) ans[k++]=(num&1),num>>=1;
	// for(int i=0;i<k;i++)
	// {
	// 	if(p) ans[i]+=p;

	// }
	int num,k=0;
	scanf("%d",&num);
	if(num==0) return puts("0"),0;
	bool pos=(num>0);ll ans=num=pos?num:-num;
	for(int i=pos;i<33;i+=2)
		if(ans&(1ll<<i))
			ans+=1ll<<(i+1);
	while((1ll<<(k+1))<=ans) ++k;
	while(k>=0) printf("%d",!!((1ll<<k)&ans) ),--k;
	puts("");
	return 0;
}