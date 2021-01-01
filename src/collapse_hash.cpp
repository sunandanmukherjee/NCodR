/*
 * File:   collapse_hash.cpp
 * 
 * To remove duplicate sequences from the fasta files. The input file is a list 
 * with the absolute or relative paths of the sequence files. The program runs for 
 * all the sequence files to remove the duplicates from all the files.
 * The first sequence entery is retained when duplicates are encountered.
 * The input file is assumed to be in a multiple sequence fasta file. 
 * For each sequence a fasta header followed by the sequence in a single
 * line is expected. 
 * 
 * Copyright 2014 Nithin C (csb.iitkgp.ac.in)
 * Acknowledgments: Srinivasan S for the suggestion to use hashes to reduce the
 * RAM use associated with loading the entire file. 
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
# include "util.h"
# include <functional>
# include <typeinfo>
# include "sha256.h"

using namespace std::chrono;
const int numCPU = sysconf( _SC_NPROCESSORS_ONLN );
SHA256 sha256;
int main(int argc, char** argv) 
{
	vector<string> parameterList = BuildParameterList(argc,argv);
	if(parameterList.size()!=2)
		{
			cout<<"Incorrect Useage:"<<endl;
			cout<<"Correct useage is: "<<parameterList.at(0)<<" list.txt"<<endl;
			return 1;
		}
	cout<<numCPU<<" processors detected"<<endl;
	
	time_t starttime,endtime;
	high_resolution_clock::time_point t1 = high_resolution_clock::now();
	starttime=system_clock::to_time_t ( t1 );
	cout<<"Process started at "<<ctime(&starttime)<<endl;
	
	vector<string> list=readfile(argv[1]);
	ofstream out;
	
	set<string> hashes;
	for(auto i : list)
	{
		cout <<"Processing "<< i << "\n"; 
		stringstream ss;
		vector<string> file=readfile(str2char(i));
		cout<<"Number of sequences in "<< i <<" is "<<file.size()/2<<endl;
		size_t count=0;
		out.open(str2char(i+".uniq.fa"),ios::trunc);
		for(size_t j=0;j<file.size();++j)
		{
			string id= file.at(j);
			++j;
			string sequence=file.at(j);
			std::string myHash2 = sha256(sequence);
			auto ret= hashes.emplace(myHash2);
			if(ret.second)
			{
				ss<<id<<endl<<sequence<<endl;
				count++;
			}
			if(count==100000)
			{
				
				out<<ss.str();
				ss.str("");
				count=0;
			}
		}
		out<<ss.str();
		ss.str("");
		out.close();
		//Print(hashes);
		cout<<"No of unique hashes="<<hashes.size()<<endl;
	} 
		
	high_resolution_clock::time_point t2 = high_resolution_clock::now();
	duration<double> time_span = duration_cast<duration<double>>(t2 - t1);
	endtime=system_clock::to_time_t ( t2 );
	cout<<"Process finished at "<<ctime(&endtime)<<endl;
	cout<<"Excecution time = "<<time_span.count()<<" seconds"<<endl;
	
	return 0;
}
