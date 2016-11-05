#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

enum Cell {empty, mine};

Cell getCell() 
{
	Cell cell;
	int dice = rand() % (6 - 1) + 1;
	if(dice < 3){
		cell = mine;
	}
	else cell = empty;
	return cell;
};

Cell getBoard(int n)
{
	Cell board[n][n];
	for(int i = 0; i < n; i++)
	{
		for(int j = 0; j < n; j++)
		{
			board[i][j] = getCell();
		}
	}
	board;
};


bool check(Cell cell)
{
	bool isClear;
	if(cell == empty)
	{
		cout << "Clear! You can continue\n";
		isClear = true;
	}
	else
	{
		cout << "PUM!!!\n";
		isClear = false;
	}
	/*switch(cell)
	{
		case empty :cout << "Clear! You can continue\n"; isClear = true;
		case mine : cout << "PUM!!!\n"; isClear = false;
	}*/
	return isClear;
}

int main()
{
	srand(time(NULL));
	int n = 3;
	Cell board[n][n];
	for(int i = 0; i < n; i++)
	{
		for(int j = 0; j < n; j++)
		{
			board[i][j] = getCell();
		}
	}
	
	for(int i = 0; i < n; i++)
	{
		cout << "\n";
		for(int j = 0; j < n; j++)
		{
			if(board[i][j] == empty){cout << 0;}
			else {cout << 1;};
		}
		cout << "\n";
	}
	
	while (true)
	{
		int x;
		int y;
		cout << "Choose a cell (row):";
		cin >> x;
		cout << "Choose a cell (column):";
		cin >> y;
		Cell input = board[x - 1][y - 1];
		if(check(input)) continue;
		else break;
	}
}
