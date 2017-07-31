#include<cstdio>
#include<cstdlib>
#include<cstring>
#include<cmath>

using namespace std;

int n,b[35],cnt;

int main()
{
    scanf("%d",&n);
    if(!n)printf("0");
    else
    {
        while(n)
        {
                cnt++;
                b[cnt]=abs(n%(-2));
                n=(n-b[cnt])/(-2);
        }
    }
    for(int i=cnt;i>=1;i--)
    printf("%d",b[i]);
    return 0;
}
