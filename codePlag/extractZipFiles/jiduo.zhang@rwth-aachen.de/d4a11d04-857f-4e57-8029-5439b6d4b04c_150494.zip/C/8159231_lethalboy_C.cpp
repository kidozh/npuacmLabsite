#include<iostream>
#include<algorithm>
#include<cstring>
#include<string>
#include<queue>
#include<cstdio>
#define N 3020
#define M 2000020
#define inf 1<<29
#define ll long long
using namespace std;
int n,m,x,y,c,ret;
bool vis[N];
int dis[N],t,ans[N];
queue<int>Q;
int head[N],pos;
struct node{int x,y,c;}p[M];
struct edge{int to,next,c;}e[M];
void add(int a,int b,int c)
{pos++;e[pos].to=b,e[pos].c=c,e[pos].next=head[a],head[a]=pos;}
void spfa(int s)
{
	for(int i=1;i<=n;i++)vis[i]=0,dis[i]=inf;
	Q.push(s);dis[s]=0;vis[s]=1;
	while(!Q.empty())
	{
		int u=Q.front();Q.pop();vis[u
		]=0;
		for(int i=head[u];i;i=e[i].next)
		{
			int v=e[i].to;
			if(dis[v]>dis[u]+e[i].c)
			{
				dis[v]=dis[u]+e[i].c;
				if(!vis[v]){Q.push(v);vis[v]=1;}
			}
		}
	}
}
int main()
{
	scanf("%d%d%d",&n,&m,&t);
	for(int i=1;i<=m;i++)
	{
		scanf("%d%d%d",&x,&y,&c);
		p[i].x=x,p[i].y=y,p[i].c=c;add(x,y,c);
	}spfa(t);for(int i=1;i<=n;i++)ans[i]=dis[i];
	pos=0;memset(head,0,sizeof(head));
	for(int i=1;i<=m;i++)
		add(p[i].y,p[i].x,p[i].c);
	spfa(t);for(int i=1;i<=n;i++)ans[i]+=dis[i];
	for(int i=1;i<=n;i++)ret=max(ret,ans[i]);
	printf("%d\n",ret);
}