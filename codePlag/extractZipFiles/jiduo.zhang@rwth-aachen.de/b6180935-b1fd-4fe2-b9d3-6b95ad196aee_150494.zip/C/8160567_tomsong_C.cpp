#include<cstdio>
#include<cstring>
#include<algorithm>
using namespace std;
int map[1010][1010],n;
int way[1010],dis[1010];
void fun(int x)
{
    int visit[1010],i,j,min,next=x;
    memset(visit,0,sizeof(visit));
    for(i=1; i<=n; ++i)
        dis[i]=map[x][i];
    visit[x]=1;
    for(i=2; i<=n; ++i)
    {
        min=0x3f3f3f3f;
        for(j=1; j<=n; ++j)
        {
            if(!visit[j]&&dis[j]<min)
            {
                min=dis[j];
                next=j;
            }
        }
        visit[next]=1;
        for(j=1; j<=n; ++j)
        {
            if(!visit[j]&&dis[j]>dis[next]+map[next][j])
                dis[j]=dis[next]+map[next][j];
        }
    }
}
int main()
{
    int m,x,i,j,a,b,t,ans=0;
    while(scanf("%d%d%d",&n,&m,&x)!=EOF)
    {
        for(i=1; i<=n; ++i)
        {
            for(j=1; j<=n; ++j)
            {
                if(i!=j)
                    map[i][j]=0x3f3f3f3f;
                else
                    map[i][j]=0;
            }
        }
        while(m--)
        {
            scanf("%d%d%d",&a,&b,&t);
            if(t<map[a][b])
                map[a][b]=t;
        }
        fun(x);
        for(i=1; i<=n; ++i)
            way[i]=dis[i];
        for(i=1; i<=n; ++i)
        {
            for(j=i+1; j<=n; ++j)
            {
                int cnt;
                cnt=map[j][i];
                map[j][i]=map[i][j];
                map[i][j]=cnt;
            }
        }
        fun(x);
        for(i=1; i<=n; ++i)
        {
            if(i!=x)
                ans=max(ans,way[i]+dis[i]);
        }
        printf("%d\n",ans);
    }
    return 0;
}
