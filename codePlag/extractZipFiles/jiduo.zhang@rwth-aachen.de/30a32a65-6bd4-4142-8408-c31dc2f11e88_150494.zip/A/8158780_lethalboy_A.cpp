#include<iostream>
#include<algorithm>
#include<cstring>
#include<string>
#include<cstdio>
#define N 20020
#define ll long long
using namespace std;
char ch[N],ss[N];
int a[N],b[N];
ll ans;
int main()
{
	scanf("%s%s",ch+1,ss+1);
	int n=strlen(ch+1),m=strlen(ss+1);
	for(int i=1;i<=n;i++)a[i]=ch[i]-'0';
	for(int i=1;i<=m;i++)b[i]=ss[i]-'0';
	for(int i=1;i<=n;i++)
		for(int j=1;j<=m;j++)
			ans+=a[i]*b[j];
	printf("%lld\n",ans);
}