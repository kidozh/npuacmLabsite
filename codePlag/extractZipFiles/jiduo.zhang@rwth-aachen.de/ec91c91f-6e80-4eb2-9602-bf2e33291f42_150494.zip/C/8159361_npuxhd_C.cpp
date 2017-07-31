#include <iostream>
#include<stdio.h>
#include<algorithm>
#include<string.h>
#include<queue>
#include<string.h>
using namespace std;
const int inf=9999999;
int map[2][1005][1005];

int n,m,x;
int dis[1008];
int ans[1008];
bool vis[1008];
void spfa(int t)
{
    for(int i=1;i<=n;i++)
    {
        dis[i]=inf;
        vis[i]=0;
    }
    vis[x]=1;
    dis[x]=0;
    queue<int> que;
    que.push(x);
    while(!que.empty())
    {
        int temp;
        temp=que.front();
        que.pop();
        for(int i=1;i<=n;i++)
        {
            if(dis[temp]+map[t][temp][i]<dis[i])
            {
                dis[i]=dis[temp]+map[t][temp][i];
                if(!vis[i])
                {
                    que.push(i);
                    vis[i]=1;
                }

            }

        }
        vis[temp]=0;
    }
    for(int i=1;i<=n;i++)
    {
        ans[i]+=dis[i];
    }
}


int main()
{
    scanf("%d%d%d",&n,&m,&x);
    for(int i=1;i<=n;i++)
    {
        for(int j=1;j<=n;j++)
        {
            if(i==j) map[0][i][j]=0;
            else map[0][i][j]=inf;
        }
    }
    memset(ans,0,sizeof(ans));
    while(m--)
    {
        int a,b,c;
        scanf("%d%d%d",&a,&b,&c);
        map[0][a][b]=c;
    }
    int ma=0;
    spfa(0);
    for(int i=1;i<=n;i++)
    {
        for(int j=1;j<=n;j++)
        {
           map[1][i][j]=map[0][j][i];
        }
    }
    spfa(1);
    for(int i=1;i<=n;i++)
    {
        ma=max(ma,ans[i]);
    }
    printf("%d\n",ma);
    return 0;
}