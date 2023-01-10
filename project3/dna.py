import csv
import sys

def read_dna(dna_filename):
   """
   Reads the DNA file
 
   This function reads the DNA sequence from the given `dna_filename`
   file. It returns the DNA sequence read from the file as a string.
 
   Parameters:
     dna_filename      The DNA file name
 
   Returns:
     str   A string that is the DNA sequence read from the file.
   """
   with open(dna_filename) as file:
    dna = file.read()
    return dna
 
def dna_length(dna_filename):
   """
   Returns the length of a DNA sequence in the file `dna_filename`
 
   Parameters:
     dna_filename     The DNA file name
 
   Returns:
     int   An integer length of the DNA sequence
   """
   return len(read_dna(dna_filename))
   
def read_strs(str_filename):
   """
   Reads the STRs from the given `str_filename` file
 
   The STR file is a CSV file containing STR repeats for certain
   people. An example of this file looks like this:
 
     name,AGAT,AATG,TATC
     Alice,5,2,8
     Bob,3,7,4
     Charlie,6,1,5
 
   This function must read the file using the `csv` module and return
   a list of dictionary objects that look like this:
 
     [{'name': 'Alice', 'AGAT': '5', 'AATG': '2', 'TATC': '8'},
      {'name': 'Bob', 'AGAT': '3', 'AATG': '7', 'TATC': '4'},
      {'name': 'Charlie', 'AGAT': '6', 'AATG': '1', 'TATC': '5'}]
 
   Parameters:
     str_filename      The STR file name
 
   Returns:
     list of dicts   A list of dictionary objects read from the CSV file
   """
    
   with open(f'{str_filename}', newline='') as csvfile:
    read_str = []
    reader = csv.DictReader(csvfile)
    for row in reader:
      read_str.append(row)
    return read_str
def get_strs(str_profile):
   """
   Returns a tuple of (STR, repeats) pairs
 
   Given a dictionary representation of an STR profile that looks
   like this:
 
     {'name': 'Alice', 'AGAT': '5', 'AATG': '2', 'TATC': '8'}
 
   return a tuple that looks like this:
 
     [('AGAT', 5), ('AATG', 2), ('TATC', 8)]
 
   Note: the repeat is an `int`, not a `string`.
 
   Parameters:
     str_profile      A STR profile in dictionary form
 
   Returns:
     list of tuples   A list of (STR, repeats) pairs
   """
   profile = []
   total= []
   for suspect in str_profile:
    if suspect != 'name':
      profile.append(suspect)
      profile.append(int(str_profile[suspect]))
      new_profile = tuple(profile)
      profile.pop(0)
      profile.pop(0)
      total.append(new_profile)
      
   return total
def longest_str_repeat_count(str_frag, dna_seq):
   """
   Finds the longest match of a given STR DNA fragment in the given
   DNA sequence.
 
   This function returns the longest repeated occurance of the given
   STR fragment, `str_frag`, in the DNA sequence `dna_seq`. For
   example, given the STR AGAT and the DNA sequence:
 
   AGACGGGTTACCATGACTATCTATCTATCTATCTATCTATCTATCTATCACGTACGTACGTA
   TCGAGATAGATAGATAGATAGATCCTCGACTTCGATCGCAATGAATGCCAATAGACAAAA
 
   this function returns 5.
 
   Hints:
 
   1. You will want to loop over the `dna_seq` character by
      character using a while loop with an index
   2. You may find using string slicing convenient for this
      function. For example, `dna_seq[i:i+4]` will evaluate to a
      substring of `dna_seq` starting from i to i+4 exclusive.
   3. Do not use the `count` string method. It doesn't return the
      longest match, it returns the count. This would also be
      cheating.
 
   Parameters:
     str_frag     A fragment of DNA in a STR profile (e.g., AGAT)
     dna_seq      A DNA sequence
 
   Returns:
     int          The longest repeated occurance of the STR fragment
   """
   i = 0
   instances = 0
   repetitions = 0
   while i < (len(dna_seq)):
    if dna_seq[i:i+4] == str_frag:
      instances+=1
      i+=4
    else:
      if instances > repetitions:
        repetitions = instances
      instances = 0
      i+=1
   if instances > repetitions:
    return instances
   return repetitions

def find_match(str_profile, dna_seq):
   """
   Find a match given a specific STR profile
 
   This function compares the repeat values for each STR dna fragment
   X in the given `str_profile` to the count of that same X dna
   fragment in the provided DNA sequence `dna_seq`.
 
   For example, if we have a profile like this (a list of tuples):
 
     [('AGAT', 5), ('AATG', 2), ('TATC', 8)]
 
   We want to determine if the number of repeats for the STR
   fragments AGAT, AATG, and TATC for this profile, which is 5, 2,
   and 8, are the same number of repeats in the DNA sequence. If the
   repeat count in the DNA sequence for AGAT, AATG, and TATC are
   identical to this profile, then we have matched the profile to the
   DNA sequence.
 
   Hints:
 
     1. You want to use the `longest_str_repeat_count` function to
        find the longest count of repeats for each STR fragment in
        the DNA sequence. This will require you to iterate over the
        `str_profile` list.
 
   Parameters:
     str_profile  A list of tuples representing a person's STR profile
 
   Returns:
     boolean      `True` if a match is found; `False` otherwise
   """
   matches = 0
   for tuple in str_profile:
    if tuple[1] == longest_str_repeat_count(tuple[0],dna_seq):
      matches+=1
   return matches == 3

def dna_match(str_filename, dna_filename):
   """
   Compares STRs to a DNA sequence
 
   This function reads the STRs in the `str_filename` file
   and the DNA sequence in the `dna_filename` file and compares
   the STRs to the DNA sequence to determine who the DNA sequence
   likely belongs to.
 
   Parameters:
     str_filename      The STR file name
     dna_filename      The DNA file name
 
   Returns:
     str   A string that is either the person's name in the STR file
           that matches the DNA sequence in the DNA file or
           'No match' if a match does not exist.
   """
   
   dna_as_str = read_dna(dna_filename)
   csv_as_list = read_strs(str_filename)
   for dictionary in csv_as_list:
    profile = get_strs(dictionary)
    match = find_match(profile,dna_as_str)
    if match == True:
      return dictionary['name']
    else:
      pass
   return "No match"

if __name__ == '__main__':
   #print("hello")
   #print(read_dna('dna_1.txt'))
   #print(read_strs('str_profiles.csv'))
   #profiles = read_strs('str_profiles.csv')
   #print(profiles)
   #print(get_strs(profiles[0]))
   #print(get_strs(profiles[0])[0])
   #assert(get_strs(profiles[0])[0]) == ('AGAT', 5)
   #print(longest_str_repeat_count('AATG','AACCCTGCGCGCGCGCGATCTATCTATCTATCTATCCAGCATTAGCTAGCATCAAGATAGATAGATGAATTTCGAAATGAATGAATGAATGAATGAATGAATG'))
   print(dna_match(sys.argv[1],sys.argv[2]))
