/*
 * PrintAllKLengthStrings.java
 * 
 * This program is modified version of the function available at
 * https://www.geeksforgeeks.org/print-all-combinations-of-given-length/
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

/***********************************************************************
 * Java program to print all possible strings of length k passed 
 * as command line argument
***********************************************************************/
class PrintAllKLengthStrings 
{
	/******************************************************************
	 * Main method
	 ******************************************************************/
    public static void main(String[] args) 
    {             
        char set[] = {'A', 'U', 'C', 'G'};
        int firstArg=0;
		if (args.length > 0) 
        {
			try 
			{
				firstArg = Integer.parseInt(args[0]);
			}
			catch (NumberFormatException e)
			{
				System.err.println("Argument must be an integer");
				System.exit(1);
			}
		}
		else
		{
		System.out.println("Incorrect useage. Pass the Window size as a command line argument");
		System.exit(1);
		}
        int k = firstArg;
        printAllKLength(set, k);        
    } 
    /*******************************************************************
     * The method that prints all possible strings of length k.  It is
     * mainly a wrapper over recursive function printAllKLengthRec()
     ******************************************************************/
    static void printAllKLength(char set[], int k) 
    {
        int n = set.length;        
        printAllKLengthRec(set, "", n, k);
    }
    /*******************************************************************
     * The main recursive method to print all possible strings of length k
     ******************************************************************/
    static void printAllKLengthRec(char set[], String prefix, int n, int k) 
    {
        if (k == 0) 
        {
			/***********************************************************
			 *Base case: k is 0, print prefix
			 **********************************************************/
            System.out.println(prefix);
            return;
        }
        
        for (int i = 0; i < n; ++i) 
        {
			/***********************************************************
			 * One by one add all characters from set and recursively 
			 * call for k equals to k-1
			 **********************************************************/
			String newPrefix = prefix + set[i]; // Next character of input added
            printAllKLengthRec(set, newPrefix, n, k - 1); // k is decreased, because we have added a new character
        }
    }
}
