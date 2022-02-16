#Compare constituency trees and get a similarity/accuracy estimate. 
#Winterlight Labs, Gouming Martens, 15 February 2022

#import os
#import pandas as pd
from collections import deque

# Create dataframe
#df = pd.DataFrame()

# Read in data, load in data
#dep = pd.read_excel('de_annotation_validation_depparses.xlsx')
syntax1 = "[S [NP [N John ]] [VP [V eats ] [NP [DET an ] [NP [N apple ]]]]]"
syntax2 = "[S [NP [N John ]] [VP [V eats ] ] [NP [DET an ] [N apple ]]]"
syntax3 = "[S [NP John ] [VP eats an apple ]]"
syntax_labels= ['S','VP','NP','N','V','DET','ROOT', 'PRON', 'ADV', 'ADVP','VERB','NOUN','INTJ','CCONJ','AUX']

################## define functions ###############

#====================getIndex=========================
# Function to find index of closing
# bracket for a given opening bracket.
def getIndex(s, i):
  
    # If input is invalid.
    if s[i] != '[':
        return 0
  
    # Create a deque to use it as a stack.
    d = deque()
  
    # Traverse through all elements
    # starting from i.
    for k in range(i, len(s)):
  
        # Pop a starting bracket
        # for every closing bracket
        if s[k] == ']':
            d.popleft()
  
        # Push all starting brackets
        elif s[k] == '[':
            d.append(s[i])
  
        # If deque becomes empty
        if not d:
            return k
    return 0

#====================trimStr=========================
# Create string without brackets and node labels
def trimStr(string,lab):
    
    for i in range(len(lab)):
        
        # Retrieve labels from syntax_labels list
        label = str('['+lab[i]+' ')
        
        # Remove all node labels and opening brackets
        short = string.replace(label, '')
        string = short
    
    # Remove all closing brackets and replace double spaces with single spaces
    short = short.replace('] ]',']]').replace(']','').replace('  ',' ')
    
    # Return a string without brackets and node labels 
    # and remove space after each constituent
    return short[:-1]

#=====================onstitList===========================
# Create from string a list of all consituents
def constitList(s):
    # Create empty list
    c = []
    
    # Go over string
    for i in range(len(s)):
        
        # Look for opening brackets
        if s[i] == '[':
            
            # Get the index of closing bracket
            end = getIndex(s,i)
            
            # Extract the constituent for that specific bracketing
            constituent = trimStr(s[i:end],syntax_labels)
            
            # Add constituent to empty list
            c += [constituent]
    
    # Return list of constituents
    return c

# #=====================labelList===========================
# # create from string a list of all constituency node labels 
# # in same order as constituency list
# def labelList(s,label):
#     d = []
#     for i in range(len(s)):
#         if s[i] == '[':
#             j = i + 1
#             while s[j] != ' ':
#                 j += 1
#             for k in range(len(label)):
#                 if s[i+1:j] == label[k]:
#                     d += [label[k]]
#     return print(d)

# labelList(syntax2,syntax_labels)    

#=====================scoreSyntax===========================
# Compare list of consituents and give a similarity score.
def scoreSyntax(s1,s2):
    
    # Create numeric variable
    score = 0
    
    # Create constituent lists from strings
    list1 = constitList(s1)
    list2 = constitList(s2)
    
    print('-------------------------------------------')
    print('List 1:\n '+ str(list1)+'\n')
    print('List 2:\n '+ str(list2)+ '\n')
    
    # Get difference in length between two lists
    dif = len(list2) - len(list1) 
    
    # If difference >= 0, keep difference 0
    # This is to make sure lists of unequal lengths (due to missing constituents) 
    # can still be given a sensible score
    if dif <= 0:
        dif = 0
    
    # Loop over both lists
    for i in range(len(list1)):
        for j in range(len(list2)):
            
            # if one item matches an item in the other list, increase the score
            if list1[i] == list2[j]:
                score += 1
                
                # and remove that item from the second list 
                del list2[j]
                
                #exit current loop and continue to the next item
                break
    
    # Return the similarity/accuracy score by dividing the total number 
    # of matches over the length of the list minus the differences in length
    # between the two lists
    return print(score/((len(list1)+dif)))

scoreSyntax(syntax2,syntax1)
scoreSyntax(syntax1,syntax3)
