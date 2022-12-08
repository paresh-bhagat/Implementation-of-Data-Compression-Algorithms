#!/usr/bin/env python
# coding: utf-8

# In[14]:


import random


# In[15]:


def xor(actual, random, n):
    result = ''
    for i in range(n):
        if actual[i] == random[i]:
            result += "0"
        else:
            result += "1"
    return result


# In[16]:


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


# In[17]:


def error(str1, str2, n):
    count = 0
    for i in range(n):
        if str1[i] != str2[i]:
            count += 1
        else:
            continue
    return count


# In[18]:


def decode(str):
    message = ""
    while str != "":
        i = chr(int(str[:8], 2))
        message = message + i
        str = str[8:]
    return message


# In[19]:


# read text file
f = open("text_pattern.txt")
original = f.read()
n=len(original)


# In[20]:


# convert text file to binary string
x = ''.join(format(ord(i), '08b') for i in original)
M = len(x)


# In[21]:


dist = [0,10, 100, 200, 500, 1000, 5000]
for d in dist:
    print('For d = ', d )
    # generate random binary string of length M : CHANNEL ERROR
    M_error = random_pattern(d, M)
    # print(rand)
    # take xor of text file and random string :TRANSMITTED MESSAGE
    y = xor(x, M_error, M)
    decoded_str = decode(y)
    e = error(original, decoded_str, n)
    print('Percentage of modified characters with respect to input file = ', 100* (e/M), '%')
    print()
print()
print("Space used in bits:", M)   

