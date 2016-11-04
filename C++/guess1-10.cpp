#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

void guess()
	{	
		int answer;
		int mistery = rand() % (10 - 1) + 1;
		cout << "Make a guess! [1-10] : ";
		cin >> answer;
		if(answer == mistery)
		{
			cout << "Yes, that's correct!\n";
		}
		else guess();
	}

int main()
{
	srand(time(NULL));
	guess();
	cin.get();
}
