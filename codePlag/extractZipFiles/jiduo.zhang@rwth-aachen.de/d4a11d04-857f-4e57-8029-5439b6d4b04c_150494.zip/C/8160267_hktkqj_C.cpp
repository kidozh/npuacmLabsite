#include <iostream>
    #include <deque>
    #include <cstdio>
    #include <cstring>
    #include <algorithm>

    using namespace std;

    const int MAXV = 1002;
    const int inf = 0x3f3f3f3f;
    int t[MAXV][MAXV], d1[MAXV], d2[MAXV];
    int que[MAXV<<1];
    bool in[MAXV];
    int n, m, x;

    void spfa(int * d)
    {
        memset(in, false, sizeof(in));
        memset(d + 1, inf, sizeof(int) * n);//memset(d, inf, sizeof(d)) if wrong
        d[x] = 0;
        int tail = -1;
        que[++tail] = x;
        in[x] = true;
        while(tail != -1){
            int cur = que[tail];
            tail--;
            in[cur] = false;
            for(int i = 1; i <= n; i++){
                if(d[cur] + t[cur][i] < d[i]){
                    d[i] = d[cur] + t[cur][i];
                    if(in[i] == false){
                        que[++tail] = i;
                        in[i] = true;
                    }
                }
            }
        }
    }

    void tran()
    {
        int i, j;
        for(i = 1; i <= n; i++){
            for(j = 1; j <= i; j++){
                swap(t[i][j], t[j][i]);
            }
        }
    }

    int main()
    {
        scanf("%d %d %d", &n, &m, &x);
            memset(t, inf, sizeof(t));
            while(m--){
                int a, b, c;
                scanf("%d %d %d", &a, &b, &c);
                t[a][b] = c;
            }
            spfa(d1);
            tran();
            spfa(d2);
            int ans = -1;
            for(int i = 1; i <= n; i++){
                if(d1[i] != inf && d2[i] != inf)
                    ans = max(ans, d1[i] + d2[i]);
            }
            printf("%d\n", ans);
        return 0;
    }