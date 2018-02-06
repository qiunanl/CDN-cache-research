#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
 
using namespace std;

int main()
{
    
    ifstream fin("../OPTA/1G.csv");
    string line;
    int i = 0;
    while (getline(fin, line))   //整行读取，换行符“\n”区分，遇到文件尾标志eof终止读取  
    {  
        cout << line << endl; //整行输出  
        string prob = line.erase(line.find_last_not_of(" \t\r\n") + 1);   
        cout << i << ":"<< prob << "@@@"; 
        i++;  
    }  
    //cout << "hello world" << endl;
    return 0;

}

