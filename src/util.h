/*
 * util.h
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

#ifndef UTIL_H_
#define UTIL_H_

#include <cstdlib>
#include <fstream>
#include <iostream>
#include <cstring>
#include <sstream>
#include <algorithm>
#include <iterator>
#include <unistd.h>
#include <dirent.h>
#include <array>
#include <cmath>
#include <ctime>
#include <ratio>
#include <chrono>
#include <tuple>
#include <set>
#include <vector>

using namespace std;

using std::string;

using namespace std::chrono;

template <class T>

std::string to_string (const T& t);

char *str2char(std::string a);

std::vector <std::string> BuildParameterList(const int & argc, char **argv);

std::string RemoveMultipleWhiteSpaces(std::string str);

std::string exec(char* cmd);

void Print (std::set<std::string> &v);

void Print (std::vector<std::string> &v);

void Print (vector<pair<string, int> > v);

std::vector<std::string> readfile(char* fname);

std::vector<std::string> stream2vector(std::stringstream& ss);

void Print(time_t rawtime);

void Print(std::vector<std::tuple<std::string, std::string, int, int, int, int>> v);

std::pair<time_t,high_resolution_clock::time_point> findtime();

void timetaken(high_resolution_clock::time_point t2,high_resolution_clock::time_point t1);

int countSubstring(const std::string& str, const std::string& sub);

#endif
