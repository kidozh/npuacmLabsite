#include<iostream>
#include<cstdlib>
#include<cstdio>
#include<cmath>
#include<cstring>
#include<queue>
#include<stack>
#define N 2002000
using namespace std;
int n;
int st[N],top;
int main()
{
	scanf("%d",&n);
	if(n==0)printf("0\n");
	else
	{
		while(n!=1)
		{
			if(abs(n)%2)
			{
				st[++top]=1;
				n=(n-1)/-2;
			}
			else
			{
				st[++top]=0;
				n=n/-2;
			}
		}putchar('1');while(top)printf("%d",st[top--]);
	}
}