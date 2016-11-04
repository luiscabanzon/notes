#include <iostream>
using namespace std;

int *biggerArray(int* pointer, int size)
{
	int *new_pointer = new int[size + 1];
	for(int j = 0; j < size; j++) 
	{
		new_pointer[j] = pointer[j];
	}
	delete pointer;
	return new_pointer;
}


int main()
{
	int x = 1;
	int y;
	int *pointer = new int[x];
	while (true)
	{
		cout << "Gimme a number! : ";
		cin >> y;
		pointer = biggerArray(pointer, x);
		pointer[x] = y;
		x++;
		cout << "OK, we have so far:\n";
		for(int i = 0; i < x; i++)
		{
			cout << pointer[i];
		}
		cout << "\n";
	}
}
