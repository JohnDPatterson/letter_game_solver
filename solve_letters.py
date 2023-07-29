import sys
import getopt
#from nltk.corpus import words
from datetime import datetime
import os
import string
from sys import exit



def main(args):
    opts, args = getopt.getopt(args, 'l:c:h', ['letters=', 'central=', 'help'])
	
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('option -l,--letters= not central letters: option -c,--central= central letter')
            exit()
        if opt in ('-l', '--letters'):
            l=arg
        if opt in ('-c','--central'):
            c=arg
        
    if 'c' not in locals():
        c=input('Please enter central letter: ')
    
    if 'l' not in locals():
        l=input('Please enter other letters: ')    
        
    print('Central letter is: ' + c)
    print('Other letters are: ' + l)
    
    c=c.lower()
    l=l.lower()
    
    lowers=list(string.ascii_lowercase)    

    l_list=list(l)
    
    other_letters=[]
    for j in lowers:
        if j not in l_list and j!=c:
            other_letters.append(j)
    
    fname='words_'+ datetime.today().strftime('%Y%m%d')+'.txt' 
    
    with open('words_alpha.txt','r') as f:
        word_list=f.read().splitlines()
    
   
    out_list=[]
    pangrams=[]
    for j in word_list:
       
        w=list(str.lower(j))
        
        if c not in w:
            continue
        elif len(w)<4:
            continue
        elif len(set(w).intersection(other_letters)) > 0:
            continue
        if set(l_list).issubset(w):
            pangrams.append(j)
        
        out_list.append(j+'\n')
    
    with open(fname, 'w') as f:
        for j in out_list:
            f.write(j)
    print('Pangrams Are: ')
    for j in pangrams:
        print(j)    
    
if __name__ == '__main__':
    main(sys.argv[1:]) #Send list of arguments

#main(['-c','e','-l','stpr'])    

