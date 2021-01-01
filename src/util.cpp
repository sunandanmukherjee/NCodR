/*
 * util.cpp
 * 
 * Copyright 2013 Nithin C (csb.iitkgp.ac.in)
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 * 
 */

 
#include "util.h"

using namespace std;
using std::string;

template <class T>

std::string to_string (const T& t)
{
    /***************************************************************************
	 * This function will convert any datatype to string
	 **************************************************************************/
	std::stringstream ss;
	ss << t;
	return ss.str();
}

char *str2char(string a)
{
	/***************************************************************************
	 * This function converts a string to char* type..
	 **********************************************************************
	 */
	char *b=new char[a.size()+1];
	b[a.size()]=0;
	memcpy(b,a.c_str(),a.size());
	return b;
}

vector <string> BuildParameterList(const int & argc, char **argv)
{
	vector<string> returnList;
	for (int i = 0; i < argc; i ++) returnList.push_back(argv[i]);
	return returnList;
}

string RemoveMultipleWhiteSpaces(string str)
{
	int i,j,n=str.size();
	for(i=0,j=0;i<n;i++)
	{
		int k=0;
		while(str.substr(i,1)==" ")
		{
			i++;
			k=1;
		}
		if(k)	str.replace(j++,1," ");
		str.replace(j,1,str,i,1);
		j++;
	}
	return(str.substr(0,j));
}

void Print (vector<string> &v)
{
  for (size_t i=0; i<v.size();i++)	cout << v.at(i) << endl;
}

void Print (set<string> &v)
{
  //for (size_t i=0; i<v.size();i++)	cout << v.at(i) << endl;
  for(auto i:v) cout<<i<<endl;
}

void Print (vector<pair<string, int> > v)
{
	for (size_t x = 0; x < v.size(); ++x ) cout << v[x].first << "," << v[x].second << "\n";
}

std::string exec(char* cmd)
{
    FILE* pipe = popen(cmd, "r");
    if (!pipe) return "ERROR";
    char buffer[128];
    std::string result = "";
    while(!feof(pipe)) 
    {
        if(fgets(buffer, 128, pipe) != NULL)
            result += buffer;
    }
    pclose(pipe);
    return result;
}
std::vector<string> readfile(char* fname)
{
	std::vector<std::string> lines;
	std::ifstream fin(fname);
	if (fin)
	{
		std::stringstream is;
		std::string line;
		is<<fin.rdbuf();// this copies the entire contents of the file into the string stream
		while(is)
		{
			std::getline(is,line);
			if(line!="") lines.push_back(line);
		}
		//Print(lines);
	}
	else
	{
		std::cout << "Couldn't open " << fname<< "\n";
		exit(0);
	}
	fin.close();
	return lines;
}

std::vector<std::string> stream2vector(std::stringstream& ss)
{
	std::vector<std::string> lines;
	std::string line;
	while(ss)
	{
		std::getline(ss,line);
		if(line!="")	lines.push_back(line);
	}
	return lines;
}

void Print(time_t rawtime)
{
	std::tm* timeinfo;
	timeinfo = std::localtime(&rawtime);
	char mbstr[100];
	std::strftime(mbstr,100,"%Y-%m-%d-%H-%M-%S",timeinfo);
	std::cout << mbstr <<endl;
}

void Print(std::vector<std::tuple<std::string, std::string, int, int, int, int>> v)
{
	for (size_t i=0; i<v.size();i++)
	{
		auto t=v.at(i);
		std::cout<<std::get<0>(t)<<"\t"<<std::get<1>(t)<<"\t"<<std::get<2>(t)<<"\t"<<std::get<3>(t)<<"\t"<<std::get<4>(t)<<"\t"<<std::get<5>(t)<<endl;
	}
	
}

int countSubstring(const std::string& str, const std::string& sub)
{
	/*******************************************************************
	 * returns count of non-overlapping occurrences of 'sub' in 'str'
	 * Source : http://rosettacode.org/wiki/Count_occurrences_of_a_substring
	 ******************************************************************/
	
    if (sub.length() == 0) return 0;
    int count = 0;
    for (size_t offset = str.find(sub); offset != std::string::npos;
    offset = str.find(sub, offset + sub.length()))
    {
        ++count;
    }
    return count;
}

std::pair<time_t,high_resolution_clock::time_point> findtime()
{
	high_resolution_clock::time_point t1 = high_resolution_clock::now();
	time_t t2=system_clock::to_time_t ( t1 );
	return make_pair(t2,t1);
}

void timetaken(high_resolution_clock::time_point t2,high_resolution_clock::time_point t1)
{
	duration<double> time_span = duration_cast<duration<double>>(t2 - t1);
	std::cout<<"Excecution time = "<<time_span.count()<<" seconds"<<std::endl;
}
