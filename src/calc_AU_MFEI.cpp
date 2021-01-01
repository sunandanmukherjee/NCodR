/* 
 * File:   calc_AU_MFEI.cpp
 * 
 * To check the AU content of all sequences in a fasta file 
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
 */

#include "util.h"

using namespace std;
using namespace std::chrono;
/*******************************************************************************
 * Functions are declared here
 ******************************************************************************/
double AU(std::string details,std::string seq);
double mfei(std::string seq, double mfe);
/*******************************************************************************
 * Main Function
 ******************************************************************************/
int main(int argc, char* argv[]) 
{
	/**************************************************************************
	 * Reads the command line arguments passed to the program, stores to vector.
	 * Program returns exit status 1 if number of arguments is incorrect
	 *************************************************************************/
	vector<string> parameterList = BuildParameterList(argc,argv);
	//Print(parameterList);
	if(parameterList.size()<2 || parameterList.size() > 3 )
	{
		cout<<"Incorrect Useage:"<<endl;
		cout<<"Correct useage is: "<<parameterList.at(0)<<" vienna_file_name [Output_file_name]"<<endl;
		return 1;
	}
	time_t starttime,endtime;
	high_resolution_clock::time_point t1 = high_resolution_clock::now();
	starttime=system_clock::to_time_t ( t1 );
	cout<<"Process started at "<<ctime(&starttime)<<endl<<endl;
    
	cout<<"Input file = "<<parameterList.at(1)<<endl;
    
	/**************************************************************************
	 * Reads the sequence file and stores into a vector of strings
	 * Input filename is obtaines from command line argument
	 *************************************************************************/
	ifstream infile;
	vector<string> lines;
	infile.open(str2char(parameterList.at(1)));
	if(infile.is_open())
	{
		for(std::string line; std::getline(infile,line);) lines.push_back( line );
	}
	else cout<<"unable to open "<<parameterList.at(1)<<endl;
	infile.close();
	unsigned int no_of_strings=lines.size();
	cout<<"Number of sequences = "<<no_of_strings/3<<endl;
	/**************************************************************************
	 * Calculates AU, MFEI
	 *************************************************************************/
	 ofstream fout;
     std::string outfile_name ;
     if (parameterList.size() == 3) 
     {
         outfile_name = parameterList.at(2);

     }
     else 
     {
         outfile_name = parameterList.at(1).substr(0, parameterList.at(1).find_last_of(".")) + "_AU_MFEI.tsv";         
     }
     cout<<"Output file = " << outfile_name << endl;
	 fout.open(outfile_name,ios::trunc);
     
	 fout<<"Sequence Descriptor\tSequence\tPercent AU\tMFEI\tSequence Length"<<endl;
	 for (unsigned int i=0; i<lines.size()-2;i=i+3)
	 {
         std::string seq = lines.at(i+1);
         std::transform(seq.begin(), seq.end(),seq.begin(), ::toupper);
         std::replace( seq.begin(), seq.end(), 'T', 'U');
		 double au=AU(lines.at(i),seq);
		 string vienna=lines.at(i+2);
		 double dG=atof(str2char(vienna.substr(vienna.find_last_of("(")+1,vienna.find_last_of(")")-vienna.find_last_of("(")-1)));
		 double MFEI=mfei(seq,dG);
		 fout<<lines.at(i)<<"\t"<<seq<<"\t"<<au<<"\t"<<MFEI<<"\t"<<seq.size()<<endl;
	 }
	 fout.close();
     
	 high_resolution_clock::time_point t2 = high_resolution_clock::now();
	 duration<double> time_span = duration_cast<duration<double>>(t2 - t1);
	 endtime=system_clock::to_time_t ( t2 );
	 cout<<endl<<"Process finished at "<<ctime(&endtime)<<endl;
	 cout<<"Excecution time = "<<time_span.count()<<" seconds"<<endl;
	 return 0;
}
/*******************************************************************************
 * Functions are defined here
 ******************************************************************************/


double AU(std::string details,std::string seq)
{
	double A,U,length;
	double percent;
	string s;
	s=seq;
	A=std::count(s.begin(),s.end(),'A');
	U=std::count(s.begin(),s.end(),'U');
	length=s.size();	
	percent=(A+U)/length*100;
	return percent;
}

double mfei(std::string seq, double mfe)
{
	double G,C,length,percent,amfe,mfei;
	string s=seq;
	G=std::count(s.begin(),s.end(),'G');
	C=std::count(s.begin(),s.end(),'C');
	length=s.size();
	percent=(G+C)/length*100;
	amfe=-mfe/length*100;
	mfei=amfe/percent;
	return mfei;
}
