#include<cstdio>
#include<cstring>
#include<cstdlib>
#include<cmath>
#include<algorithm>
using namespace std;
int map[1005][1005];
int map2[1005][1005];
int d[1005];
int d2[1005];
int n,m,x;
int head,tail;
int que[100000];
int book[1005];
void spfa(int v)
{
	head=0;
	tail=0;
	for(int i=1;i<=n;i++)
	{
		d[i]=99999999;
	}
	d[v]=0;
	que[tail]=v;
	book[v]=1;
	tail++;
	while(head!=tail)
	{
		int p=que[head];
		for(int i=1;i<=n;i++)
		{
			if(d[i]>d[p]+map[p][i])
			{
				//printf("%d %d:::%d\n",p,i,map[p][i]);
				d[i]=map[p][i]+d[p];
				if(book[i]==0)
				{
				que[tail]=i;
				tail++;
				book[i]=1;
				}
			}
					
		}
		book[p]=0;
		head++;
	//	for(int i=1;i<=n;i++)
	//	{
	//		printf("%d ",d[i]);
	//	}
	//	printf("\n");
	}
}
void spfa2(int v)
{
	memset(book,0,sizeof(book));
	head=0;
	tail=0;
	for(int i=1;i<=n;i++)
	{
		d2[i]=99999999;
	}
	d2[v]=0;
	que[tail]=v;
	book[v]=1;
	tail++;
	while(head!=tail)
	{
		int p=que[head];
		for(int i=1;i<=n;i++)
		{
			if(d2[i]>d2[p]+map2[p][i])
			{
				d2[i]=map2[p][i]+d2[p];
				if(book[i]==0)
				{
				que[tail]=i;
				tail++;
				book[i]=1;
				}
			}
					
		}
		book[p]=0;
		head++;
	}
}
int main()
{
	//freopen(".in","r",stdin);
	//freopen(".out","w",stdout);

	scanf("%d%d%d",&n,&m,&x);
	int a,b,t;
	for(int i=1;i<=n;i++)
	{
		for(int j=1;j<=n;j++)
		{
			map[i][j]=99999999;
			map2[i][j]=99999999;
		}
		map[i][i]=0;
		map2[i][i]=0;
	}
	for(int i=1;i<=m;i++)
	{	
		scanf("%d%d%d",&a,&b,&t);
		map[a][b]=t;
		map2[b][a]=t;
	}
//	for(int i=1;i<=n;i++)
//	{
//		for(int j=1;j<=n;j++)
//		{
//			printf("%10d",map[i][j]);
//			
//		}
//		printf("\n");
//	}
	spfa(x); 
	spfa2(x);
	int max=0;
	int ans;
	
	for(int i=1;i<=n;i++)
	{
	//	printf("%d %d\n",d[i],d2[i]);
		ans=d[i]+d2[i];
		if(ans>max)
		max=ans;
	}
	printf("%d",max);
}
