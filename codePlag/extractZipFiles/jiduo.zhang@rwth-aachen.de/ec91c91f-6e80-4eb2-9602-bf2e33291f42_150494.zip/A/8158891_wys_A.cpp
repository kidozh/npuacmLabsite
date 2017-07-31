#include <iostream>
#include<cstdio>
#include<cstring>
#include<algorithm>
using namespace std;
long long a,b;
int k=0,f=0,A[100],B[100];
int main()
{
    scanf("%lld%lld",&a,&b);
    while(a)
    {
        A[k++]=a%10;
        a=a/10;
        //printf("%d ",A[k-1]);
    }
    f=0;
    while(b)
    {
        B[f++]=b%10;
        b=b/10;// printf("%d ",B[f-1]);
    }
    int sum=0;
    for(int i=0;i<f;i++)
    {
        for(int j=0;j<k;j++)
        {
            sum=sum+A[j]*B[i];
        }
    }
    cout << sum << endl;
    return 0;
}
