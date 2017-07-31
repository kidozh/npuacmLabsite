//By Sean Chen
#include <iostream>
#include <cstdio>
#include <cstring>
#include <queue>
#include <vector>
#define inf 0x3f3f3f3f
using namespace std;
struct edge{
    int e,dis;
};
struct cmp{
    bool operator()(edge a,edge b)
    {
        return a.dis>b.dis;
    }
};

int Map1[1005][1005],Map2[1005][1004];
int visit[1005];
int n,m,x,a,b,dis;
void shortest1(int pos)
{
    queue <int> q;
    int temp;
    for (int i=1;i<=n;i++)
    {
        if (i!=pos && Map1[pos][i]!=inf)
        {
            q.push(i);
        }
    }
    while (q.size())
    {
        memset(visit,0,sizeof(visit));
        temp=q.front();
        q.pop();
        for (int i=1;i<=n;i++)
        {
            if (Map1[temp][i]+Map1[pos][temp]<Map1[pos][i])
            {
                //cout<<i<<' ';
                Map1[pos][i]=Map1[temp][i]+Map1[pos][temp];
                if (!visit[i])
                {
                    visit[i]=1;
                    q.push(i);
                }
            }
        }
    }
    return;
}
void shortest2(int pos)
{
    queue <int> q;
    int temp;
    for (int i=1;i<=n;i++)
    {
        if (i!=pos && Map2[pos][i]!=inf)
        {
            q.push(i);
        }
    }
    while (q.size())
    {
        memset(visit,0,sizeof(visit));
        temp=q.front();
        q.pop();
        for (int i=1;i<=n;i++)
        {
            if (Map2[temp][i]+Map2[pos][temp]<Map2[pos][i])
            {
                //cout<<i<<' ';
                Map2[pos][i]=Map2[temp][i]+Map2[pos][temp];
                if (!visit[i])
                {
                    visit[i]=1;
                    q.push(i);
                }
            }
        }
    }
    return;
}
int main()
{
    scanf("%d%d%d",&n,&m,&x);
    memset(Map1,inf,sizeof(Map1));
    memset(Map2,inf,sizeof(Map2));
    for (int i=1;i<=m;i++)
    {
        scanf("%d%d%d",&a,&b,&dis);
        Map1[a][b]=dis;
        Map2[b][a]=dis;
    }
    for (int i=1;i<=n;i++)
    {
        Map1[i][i]=0;
        Map2[i][i]=0;
    }
    /*for (int j=1;j<=n;j++)
        {
            for (int k=1;k<=n;k++)
                if (Map[j][k]!=inf)
                    printf("%5d",Map[j][k]);
                else
                    printf("    0");
            printf("\n");
        }*/
    shortest1(x);
    shortest2(x);
    int ans=0;
    for (int i=1;i<=n;i++)
    {
        if (Map1[x][i]+Map2[x][i]>ans)
            ans=Map1[x][i]+Map2[x][i];
    }
    printf("%d\n",ans);
    return 0;
}