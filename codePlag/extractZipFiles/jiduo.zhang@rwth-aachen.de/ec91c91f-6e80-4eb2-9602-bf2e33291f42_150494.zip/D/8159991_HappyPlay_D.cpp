#include<vector>
#include<cstdio>
#include<cmath>

using namespace std;

const int MAXN = 105;

int n;
int var[MAXN];

int main(){
    scanf("%d", &n);
    if(!n){
        puts("0");
    }
    else{
        int m = n < 0 ? -n  :  n;
        int tot = 0;
        while(m){
            var[tot++] = m & 1;
            m >>= 1;
        }
        for(int i = 0; i < MAXN - 1; ++i){
            var[i + 1] += var[i] / 2;
            var[i] %= 2;
            if(var[i] && n < 0 && !(i % 2)){
                ++var[i + 1];
            }
            if(var[i] && n > 0 && i % 2){
                ++var[i + 1];
            }
        }
        /*for(int i = 0; i < MAXN - 1; ++i){
                var[i + 1] += var[i] / 2;
                var[i] %= 2;
        }*/
        int j = MAXN - 1;
        for(; j >= 0 && !var[j]; --j);
        for(; j >= 0; --j){
            printf("%d", var[j]);
        }
        puts("");
    }
    return 0;
}