#include<iostream>
#include<string>
using namespace std;
int main()
{
	string a1,a2;
	cin>>a1>>a2;
	int tot=0;
	for (int i=0;i<a1.length();i++)
		for (int j=0;j<a2.length();j++)
			tot+=(a1[i]-'0')*(a2[j]-'0');
	cout<<tot<<endl;
}