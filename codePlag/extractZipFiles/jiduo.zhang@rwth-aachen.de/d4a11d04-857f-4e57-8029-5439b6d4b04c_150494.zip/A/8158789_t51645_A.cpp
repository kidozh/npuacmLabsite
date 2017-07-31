#include<iostream>
#include <stdio.h>
#include <algorithm>
#include <math.h>
#include<stdlib.h>
#include <string.h>
#include<queue>
#include<set>
#include<map>
#include<stack>
#include<time.h>
using namespace std;
#define MAX_N 200000005
#define inf 0x7fffffff
#define LL long long
#define ull unsigned long long
#define mod 10007
LL INF=9e18;

int main()
{
    char A[15], B[15];
    while(scanf("%s%s",A,B)!=EOF) {
        int la = strlen(A);
        int lb = strlen(B);
        int sum = 0;
        for(int i=0;i<la;i++) {
            for(int j=0;j<lb;j++) {
                sum = sum + (A[i]-'0') * (B[j]-'0');
            }
        }
        printf("%d\n",sum);
    }
}
