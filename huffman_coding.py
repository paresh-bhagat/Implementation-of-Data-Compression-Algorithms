#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random


# In[2]:


def xor(actual, random, j):
    result = ''
    n=len(actual)
    k=0
    for i in range(j,n+j):
        if actual[k] == random[i]:
            result += "0"
        else:
            result += "1"
        k=k+1
    return result


# In[3]:


def random_pattern(k, n):
    output = 0
    for d in random.sample(range(n), k):
        output += (1 << d)
    temp = bin(output)[2:]
    if len(temp) < n:
        temp = temp[::-1]
        temp1 = temp + '0' * (n - len(temp))
        temp1 = temp1[::-1]
        return temp1
    else:
        return temp


# In[4]:


class Nodes:  
    def __init__(self, probability, symbol, left = None, right = None):
           # probability of the symbol  
        self.probability = probability  
  
        # the symbol  
        self.symbol = symbol  
  
        # the left node  
        self.left = left  
  
        # the right node  
        self.right = right  
  
        # the tree direction (0 or 1)  
        self.code = ''  


# In[5]:


def CalculateProbability(the_data):  
    the_symbols = dict()  
    for item in the_data:  
        if the_symbols.get(item) == None:  
            the_symbols[item] = 1  
        else:   
            the_symbols[item] += 1       
    return the_symbols  

the_codes = dict()  
  
def CalculateCodes(node, value = ''):  
    # a huffman code for current node  
    newValue = value + str(node.code)  
  
    if(node.left):  
        CalculateCodes(node.left, newValue)  
    if(node.right):  
        CalculateCodes(node.right, newValue)  
  
    if(not node.left and not node.right):  
        the_codes[node.symbol] = newValue  
           
    return the_codes  

def OutputEncoded(the_data, coding):  
    encodingOutput = []  
    for element in the_data:   
        encodingOutput.append(coding[element])  
          
    the_string = ''.join([str(item) for item in encodingOutput])      
    return the_string   
    


# In[6]:


def HuffmanEncoding(the_data):  
    symbolWithProbs = CalculateProbability(the_data)  
    the_symbols = symbolWithProbs.keys()  
    the_probabilities = symbolWithProbs.values()  
      
    the_nodes = []  
      
    # converting symbols and probabilities into huffman tree nodes  
    for symbol in the_symbols:  
        the_nodes.append(Nodes(symbolWithProbs.get(symbol), symbol))  
      
    while len(the_nodes) > 1:   
        the_nodes = sorted(the_nodes, key = lambda x: x.probability)  
        right = the_nodes[0]  
        left = the_nodes[1]  
      
        left.code = 0  
        right.code = 1  
       
        newNode = Nodes(left.probability + right.probability, left.symbol + right.symbol, left, right)  
      
        the_nodes.remove(left)  
        the_nodes.remove(right)  
        the_nodes.append(newNode)  
              
    huffmanEncoding = CalculateCodes(the_nodes[0])  
    encoded_output = OutputEncoded(the_data,huffmanEncoding)  
    return encoded_output, the_nodes[0]  


# In[7]:


def HuffmanDecoding(encodedData, huffmanTree):  
    treeHead = huffmanTree  
    decodedOutput = []  
    for x in encodedData:  
        if x == '1':  
            huffmanTree = huffmanTree.right     
        elif x == '0':  
            huffmanTree = huffmanTree.left  
        try:  
            if huffmanTree.left.symbol == None and huffmanTree.right.symbol == None:  
                pass  
        except AttributeError:  
            decodedOutput.append(huffmanTree.symbol)  
            huffmanTree = treeHead  
          
    string = "".join(decodedOutput) 
    return string  


# In[8]:


def binarytoascii(str2):
    message = ""
    while str2 != "":
        i = chr(int(str2[:8], 2))
        message = message + i
        str2 = str2[8:]
    return message


# In[9]:


f = open("text_pattern.txt")
original = f.read() 
x = ''.join(format(ord(i), '08b') for i in original)


# In[10]:


test_str = x
chnk_len = 24

res = [test_str[idx : idx + chnk_len] for idx in range(0, len(test_str), chnk_len)]


# In[11]:


# encode the data  
encoded_chunks=[]
tree_chunks=[]
M=0
for value in res:
    encoding, the_tree = HuffmanEncoding(value)  
    encoded_chunks.append(encoding)
    tree_chunks.append(the_tree)
    M = M+len(encoding) 


# In[12]:


print("Space used in bits before compression:", len(x)) 
print("Space used in bits after compression:", M) 


# In[13]:


dist = [0,10,100,200,500,5000]
print("Original text")
print(original)
print()
for d in dist:
    print('d = ', d)

    # generate random binary string of length M' : CHANNEL ERROR
    M_error = random_pattern(d, M)
    # print('random ', rand)
    j=0
    d_temp=[]
    for i in range(0,len(encoded_chunks)):
        
        # take xor of text file and random string : RECEIVED MESSAGE
        y = xor(encoded_chunks[i], M_error, j)
        j=j+len(encoded_chunks[i])
        
        # print('received ', y)
        decoded_str = HuffmanDecoding(y, tree_chunks[i])
        d_temp.append(decoded_str)
    decoded="".join(d_temp)
    final=binarytoascii(decoded)
    print(final)
    print()

