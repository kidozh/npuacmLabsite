
//By Sesan Chen
#include <iostream>
#include <cstdio>
using namespace std;

int main()
{
    int T,A,B,t,po,temp;

    scanf("%d%d",&A,&B);
    po=0;
    while(A)
    {
        t=A%10;
        temp=B;
        while(temp)
        {
            po+=temp%10*t;
            temp/=10;
        }
        A/=10;
    }
    printf("%d\n",po);

    return 0;
}
