import sys
import getopt
#from nltk.corpus import words
from datetime import datetime
import os
import string
from sys import exit
from collections import Counter

def main(args):
    opts, args = getopt.getopt(args, 'l:n:k:h', ['e_letters=','n_letters','k_letters', 'help'])
	
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('option -l,--e_letters= excluded letters: option -n,--n= included letters: option -k, --k_letters=known letters (spaces should be underscores)')
            exit()
        if opt in ('-l', '--e_letters'):
            l=arg
        if opt in ('-n', '--n_letters'):
            n=arg
        if opt in ('-k', '--k_letters'):
            k=arg
    
    if 'l' not in locals():
        l=input('Please enter excluded letters: ')    
    if 'n' not in locals():
        n=input('Please enter included letters: ') 
    if 'k' not in locals():
        k=input('Please enter known letters (empty spaces should be underscores): ') 
        
    out_print=input('Write remaining words to .txt file? (Y/N) ')
    out_next=input('Suggest next word? (Y/N) ')
    
    print('Excluded letters are: ' + l)
    print('Included letters are: ' + n)
    print('Known letters are: ' + k)
    
    l=l.lower()
    n=n.lower()
    k=k.lower()
    

    l_list=list(l)
    n_list=list(n)
    k_list=list(k)
    
    
    if len(k_list) !=5 and len(k_list) !=0:
        print('Please enter 5 letters for known letters, unknown spaces should be underscores')
        exit
    if out_print!='Y' and out_print!='N':
        print('Please enter "Y" or "N" for printing remaining words to text file')
        exit
    if out_next !='Y' and out_next !='N':
        print('Please enter "Y" or "N" for suggesting next word')
        exit
        
    out_list=calc_remaining_words(l_list,n_list,k_list)
    fname='wordle_'+ datetime.today().strftime('%Y%m%d')+'.txt' 
    
    if out_print=='Y':
        with open(fname, 'w') as f:
            for j in out_list:
                f.write(j)
    
    if out_next=='Y':
        letter_count=count_letters(out_list)
        next_word=find_next_word(letter_count,out_list)
        print('Recommended words are: ')
        print(*next_word)
    
def calc_remaining_words(l_list,n_list,k_list):

    dupe_dict=dict(Counter(n_list))
    lowers=list(string.ascii_lowercase)    
    possible_letters=[]
    
    for j in lowers:
        if j not in l_list:
            possible_letters.append(j)
    
    fname='wordle_'+ datetime.today().strftime('%Y%m%d')+'.txt' 
    
    with open('words_alpha.txt','r') as f:
        word_list=f.read().splitlines()
    
   
    out_list=[]
    for j in word_list:
        
        flag=True
        
        w=list(str.lower(j))
        
        if len(w)!=5:
            continue
        elif any(x in l_list for x in w):
            continue
        elif any(x not in w for x in n_list ):
            continue
        
        w_dict=Counter(w)
        
        for letter, count in dupe_dict.items():
            if w_dict[letter]<count:
                flag=False
                break
            
        for i in range(len(k_list)):
            if k_list[i]=='_':
                continue
            elif k_list[i]!=w[i]:
                flag=False
                break
        
        if flag:
            out_list.append(j+'\n')

    return out_list

def count_letters(word_list):
    mega_string=''
    for i in range(len(word_list)): 
        mega_string=''.join([mega_string,word_list[i][0:-1]])
    mega_list=list(mega_string)
    return dict(Counter(mega_list))

def find_next_word(letter_count,word_list):
    
    score={}
    
    for i in range(len(word_list)):
        w=word_list[i][0:-1]
        w_list=list(str.lower(w))
        temp=list(set(w_list))
        score[word_list[i]]=sum(letter_count[x] for x in temp)
    
    high_score=max(list(score.values()))
    
    recommended_words=[k for k,v in score.items() if v == high_score]
    
    return recommended_words
        
if __name__ == '__main__':
    main(sys.argv[1:]) #Send list of arguments

#main(['-c','e','-l','stpr'])    

