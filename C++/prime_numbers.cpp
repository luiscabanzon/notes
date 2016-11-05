#include <iostream>
using namespace std;

bool isDivisible(int a, int b)
	{
		return a % b == 0;
	}

bool isPrime(int x)
	{	
		bool prime = true;
		for(int i = 2; i < x; i++)
		{
			if(isDivisible(x, i)) prime = false;			
		}
		return prime;
	}

int main()
{	
	for(int n = 2; n <= 1000000; n++)
	{
		if(isPrime(n)) cout << n << '\n';
	}
}
