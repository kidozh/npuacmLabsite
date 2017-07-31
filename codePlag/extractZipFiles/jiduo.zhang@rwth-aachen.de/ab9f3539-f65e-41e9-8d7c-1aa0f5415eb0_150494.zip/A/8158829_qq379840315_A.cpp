#include<iostream>
#include<cmath>
#include<cstdio>
#include<iomanip>
#include<cstring>
#include<stdlib.h>
#include<string>
#include<algorithm>
#include<queue>
using namespace std;
char a[1000],b[1000];
long long  s[20],sum;
int main()
{
	int x;
	while(scanf("%s %s",a,b)!=EOF)
	{
		memset(s,0,sizeof s);
		int lena=strlen(a),lenb=strlen(b);
		sum=0;
		for(int i=0;i<lena;i++)
		{
			x=a[i]-'0';
			if(s[x]==0)
			{
				for(int j=0;j<lenb;j++)
				{
					s[x]+=x*(b[j]-'0');
				}
			}
			sum+=s[x];
		}
		printf("%lld\n",sum);
	}
	return 0;
}
