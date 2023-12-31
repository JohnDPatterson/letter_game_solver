import sys
import getopt
#from nltk.corpus import words
from datetime import datetime
import os
import string
from sys import exit
from collections import Counter
from argparse import ArgumentParser

# p = ArgumentParser()
# p.add_argument('-c', '--continue', action='store_true')
# p.add_argument('-l','--e_letters')
# p.add_argument('-k','--known_letters')
# p.add_argument('-h')

def main(args):
    opts, args = getopt.getopt(args, 'cl:k:h', ['continue','e_letters=','k_letters', 'help'])
	
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('option -c,--cont continue game:-l,--e_letters= excluded letters:: option -k, --k_letters=known letters (spaces should be underscores)')
            exit()
        if opt in ('-c','--continue'):
            cont=True
        if opt in ('-l', '--e_letters'):
            l=arg
        if opt in ('-k', '--k_letters'):
            k=arg

    if 'cont' not in locals():
        cont=input('Continue game? (Y/N) ')
        if cont !='Y' and cont !='N':
            print('Please enter "Y" or "N" for continue game')
            exit
        if cont=='Y':
            cont=True
        else:
             cont=False   
        
    if 'l' not in locals():
        if cont:
            l=input('Please enter new excluded letters: ')    
        else:
            l=input('Please enter excluded letters: ')    
    if 'k' not in locals():
        k=input('Please enter known letters (empty spaces should be underscores): ') 
    
    n=[]    
    for i in range(5):
        if cont:
            temp=input('Please enter new letters in word but not in position ' + str((i+1)) + ': ')
        else:
            temp=input('Please enter letters in word but not in position ' + str((i+1)) + ': ')
        n.append(list(temp.lower()))
        
    out_print=input('Write remaining words to .txt file? (Y/N) ')
    out_next=input('Suggest next word? (Y/N) ')
    
    
    if cont:
        print('Continued game...')
        
    print(('User Inputs are: '))
    if l:
        print('Excluded letters are: ' + l)
    if k:
        print('Known letters are: ' + k)
        
    for i in range (5):
        if n[i]:
            print('Letters in word but not in position ' + str((i+1)) + ' are: ' + ''.join(n[i]))
    
    l=l.lower()
    k=k.lower()
    

    l_list=list(l)
    k_list=list(k)
    
    if len(k_list) !=5 and len(k_list) !=0:
        print('Please enter 5 letters for known letters, unknown spaces should be underscores')
        exit
    if out_print!='Y' and out_print!='N':
        print('Please enter "Y" or "N" for printing remaining words to text file')
    if out_next !='Y' and out_next !='N':
        print('Please enter "Y" or "N" for suggesting next word')
     
    dupe_dict=create_dupe_dict(n)   
     
    out_list=calc_remaining_words(l_list,n,k_list,dupe_dict,cont)
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
    
    cont=input('Continue game? (Y/N) ')
    if cont !='Y' and cont !='N':
        print('Please enter "Y" or "N" for continue game')
        exit
    if cont=='Y':
        cont=True
    else:
         cont=False       
    
    if cont:
        main(['-c'])

    
def calc_remaining_words(l_list,n,k_list,dupe_dict,cont):
    
    n_all=sum(n,[])

    
    lowers=list(string.ascii_lowercase)    
    possible_letters=[]
    

    
    for j in lowers:
        if j not in l_list:
            possible_letters.append(j)
    
    if cont:
        fname='wordle_'+ datetime.today().strftime('%Y%m%d')+'.txt' 
        if not os.path.isfile(fname):
            print('No file from today. Please start new game')
            exit
    else:
        fname='words_alpha.txt'
    
    with open(fname,'r') as f:
        word_list=f.read().splitlines()
    
   
    out_list=[]
    for j in word_list:
        
        flag=True
        
        w=list(str.lower(j))
        
        if len(w)!=5:
            continue
        elif any(x in l_list for x in w):
            continue
        elif any(x not in w for x in n_all ):
            continue
        
        w_dict=Counter(w)
        
        for letter, count in dupe_dict.items():
            if w_dict[letter]<count:
                flag=False
                break
        if flag:    
            for i in range(len(k_list)):
                if k_list[i]=='_':
                    continue
                elif k_list[i]!=w[i]:
                    flag=False
                    break
        if flag:
            for i in range(5):
                if w[i] in n[i]:
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
    
    high_score=max((list(score.values())))
    
    recommended_words=[k for k,v in score.items() if v == high_score]
    
    return recommended_words

def create_dupe_dict(n):
    n_all=sum(n,[])
    n_u=list(set(n_all))
    dupe_dict={}
    
    for i in n_u:
        dupe_dict[i]=int(input('How many instances are there of ' + i + '? '))
    
    return dupe_dict
        
        
if __name__ == '__main__':
    main(sys.argv[1:]) #Send list of arguments

#main(['-c','e','-l','stpr'])    

