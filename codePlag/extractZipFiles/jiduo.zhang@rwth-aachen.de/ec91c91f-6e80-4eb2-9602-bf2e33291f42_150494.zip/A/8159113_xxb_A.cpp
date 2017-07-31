#include<cstdio>
#include<algorithm>
#include<cstring>
using namespace std;
char a[12],b[12];
int main()
{
	int m,n,i,j,sum;
	while(scanf("%s %s",a,b)!=EOF)
	{
		m=strlen(a),n=strlen(b),sum=0;
		for(i=0;i<m;i++)for(j=0;j<n;j++)
		{
			sum+=(a[i]-'0')*(b[j]-'0');
		}
		printf("%d\n",sum);
	}
	return 0;
}