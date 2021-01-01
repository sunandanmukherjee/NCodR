/*
 * repeats.cpp
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
#include <filesystem>

using namespace std::chrono;
int main(int argc, char** argv) 
{
	/*************************************************************
	 * Command Line arguments are parsed below
	 *************************************************************/
	vector<string> parameterList = BuildParameterList(argc,argv);
	if(parameterList.size()!=2)
	{
		cout<<"Incorrect Useage:"<<endl;
		cout<<"Correct useage is: "<<parameterList.at(0)<<" fastafile.fa"<<endl;
		return 1;
	}
	/*************************************************************
	 * Process start time is calculated below
	 *************************************************************/
	time_t starttime,endtime;
	high_resolution_clock::time_point t1 = high_resolution_clock::now();
	starttime=system_clock::to_time_t ( t1 );
	cout<<"Process started at "<<ctime(&starttime)<<endl;
	/*************************************************************
	 * Main code is below
	 *************************************************************/
	ifstream file(argv[1]);
	vector<string> sequences;
	string line;
	while (getline(file,line)) sequences.push_back(line);
	//Print(sequences);
	system("javac -classpath \".\" PrintAllKLengthStrings.java");
	stringstream ss;
	vector<string> permutations;
	for(unsigned int i=1;i<=6;i++)//Iterates for window size 1-6
	{			
		ss<<exec(str2char("java -classpath \".\" PrintAllKLengthStrings "+ to_string(i)));
		copy(istream_iterator<string>(ss), istream_iterator<string>(),back_inserter(permutations));
		ofstream out(str2char("windowsize"+to_string(i)+".tsv"),ios::trunc);
		out<<"id\tseq";
		for(auto k : permutations) out<<"\t"<<string(k);
		out<<endl;
		string id,seq;
		for (unsigned int j=0; j<sequences.size()-1;j=j+2)
		{
			id=sequences.at(j);
			seq=sequences.at(j+1);
			std::transform(seq.begin(), seq.end(),seq.begin(), ::toupper);

			std::replace( seq.begin(), seq.end(), 'T', 'U');
			out<<id<<"\t"<<seq;
			for(unsigned int k=0; k<permutations.size();++k) out<<"\t"<<double(countSubstring(seq,permutations.at(k)))/seq.size()*100;
			out<<endl;
		}
		permutations.clear();
		ss.str("");
		ss.clear();
	}
	/*************************************************************
	 * Process end time is calculated below
	 *************************************************************/
	high_resolution_clock::time_point t2 = high_resolution_clock::now();
	duration<double> time_span = duration_cast<duration<double>>(t2 - t1);
	endtime=system_clock::to_time_t ( t2 );
	cout<<"Process finished at "<<ctime(&endtime)<<endl;
	cout<<"Excecution time = "<<time_span.count()<<" seconds"<<endl;
	return 0;
}

