#include<vector>
#include<cstdio>
#include<queue>

using namespace std;

const int MAXN = 1005;
const int INF = 100000000;

struct Node{
    int v, w;
};

int N, M, X;
int dis1[MAXN];
int dis2[MAXN];
int mark[MAXN];
vector<Node>graph[MAXN];
vector<Node>nGraph[MAXN];

void getDis(int u, vector<Node> g[], int dis[]){
    for(int i = 1; i <= N; ++i){
        dis[i] = INF;
        mark[i] = 0;
    }
    queue<int> q;
    dis[u] = 0;
    q.push(u);
    mark[u] = 1;
    while(!q.empty()){
        int v = q.front();
        q.pop();
        mark[v] = 0;
        for(int i = 0; i < (int)g[v].size(); ++i){
            Node now = g[v][i];
            if(dis[now.v] > dis[v] + now.w){
                dis[now.v] = dis[v] + now.w;
                if(!mark[now.v]){
                    q.push(now.v);
                    mark[now.v] = 1;
                }
            }
        }
    }
}

int main(){
    scanf("%d%d%d", &N, &M, &X);
    for(int i = 1; i <= M; ++i){
        int u, v, w;
        scanf("%d%d%d", &u, &v, &w);
        graph[u].push_back({v, w});
        nGraph[v].push_back({u, w});
    }
    getDis(X, graph, dis1);
    getDis(X, nGraph, dis2);
    int tempAns = 0;
    for(int i =1; i <= N; ++i){
        tempAns = max(tempAns, dis1[i] + dis2[i]);
    }
    printf("%d\n", tempAns);
    return 0;
}