#include<iostream>
#include<algorithm>
#include<cstdlib>
#include<cstdio>
#include<cmath>
#include<string>
#include<cstring>
#include<climits>
#include<queue>
#include<stack>
#include<map>
#include<set>
#define N 2000200
#define M 4000400
using namespace std;
typedef long long ll;
inline int read()
{
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-'0';ch=getchar();}
	return x*f;
}
int n,m,k,c[N],head[N],pos;
int rk[N],f[N],cnt[N],tot;
int find(int x){return x==f[x]?x:find(f[x]);}
struct edge{int x,y,next;}e[M];
void add(int cc,int u,int v)
{
	e[++tot].x=u,e[tot].y=v;
	e[tot].next=head[cc],head[cc]=tot;
}
ll ans;
struct node
{
	int x,y,rk1,rk2,ct1,ct2;
}st[N];int top;
void make(int l,int r)
{
	for(int i=l;i<=r;i++)
	{
		for(int j=head[i];j;j=e[j].next)
		{
			int x=e[j].x,y=e[j].y;
			int fx=find(x),fy=find(y);
			if(fx==fy)continue;top++;
			st[top].x=fx,st[top].y=fy,st[top].rk1=rk[fx],st[top].rk2=rk[fy],st[top].ct1=cnt[fx],st[top].ct2=cnt[fy];
			ans+=(ll)cnt[fy]*cnt[fx];
			if(rk[fx]<=rk[fy])
			{
				f[fx]=fy;
				rk[fy]=max(rk[fy],rk[fx]+1);
				cnt[fy]+=cnt[fx];
			}
			else
			{
				f[fy]=fx;
				rk[fx]=max(rk[fx],rk[fy]+1);
				cnt[fx]+=cnt[fy];
			}
		}
	}
}
void back(int bt)
{
	while(top!=bt)
	{
		rk[st[top].x]=st[top].rk1;
		rk[st[top].y]=st[top].rk2;
		cnt[st[top].x]=st[top].ct1;
		cnt[st[top].y]=st[top].ct2;
		ans-=(ll)st[top].ct1*st[top].ct2;
		f[st[top].x]=st[top].x;
		f[st[top].y]=st[top].y;top--;
	}
}
void cdq(int l,int r)
{
	if(l==r)
	{
		printf("%lld\n",ans);
		return;
	}int mid=(l+r)>>1,now=top;
	make(mid+1,r);cdq(l,mid);back(now);
	make(l,mid);cdq(mid+1,r);back(now);
}
int main()
{
	while(~scanf("%d",&n))
	{
		top=tot=ans=pos=0;
		memset(head,0,sizeof(head));
		m=read(),k=read();
		for(int i=1;i<=m;i++)
		{
			int x=read(),y=read();
			c[i]=read();add(c[i],x,y);
		}for(int i=1;i<=n;i++)
			f[i]=i,cnt[i]=1,rk[i]=1;
		cdq(1,k);
	}
}