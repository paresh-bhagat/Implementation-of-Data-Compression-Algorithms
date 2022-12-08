#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import random
import string
import decimal
from decimal import Decimal

class ArithmeticEncoding:
    def __init__(self, frequency_table, save_stages=False):
        self.save_stages = save_stages
        if(save_stages == True):
            print("")

        self.probability_table = self.get_probability_table(frequency_table)

    def get_probability_table(self, frequency_table):
        
        total_frequency = sum(list(frequency_table.values()))

        probability_table = {}
        for key, value in frequency_table.items():
            probability_table[key] = value/total_frequency

        return probability_table

    def get_encoded_value(self, last_stage_probs):
        last_stage_probs = list(last_stage_probs.values())
        last_stage_values = []
        for sublist in last_stage_probs:
            for element in sublist:
                last_stage_values.append(element)

        last_stage_min = min(last_stage_values)
        last_stage_max = max(last_stage_values)
        encoded_value = (last_stage_min + last_stage_max)/2

        return last_stage_min, last_stage_max, encoded_value

    def process_stage(self, probability_table, stage_min, stage_max):
        stage_probs = {}
        stage_domain = stage_max - stage_min
        for term_idx in range(len(probability_table.items())):
            term = list(probability_table.keys())[term_idx]
            term_prob = Decimal(probability_table[term])
            cum_prob = term_prob * stage_domain + stage_min
            stage_probs[term] = [stage_min, cum_prob]
            stage_min = cum_prob
        return stage_probs

    def encode(self, msg, probability_table):
        msg = list(msg)

        encoder = []

        stage_min = Decimal(0.0)
        stage_max = Decimal(1.0)

        for msg_term_idx in range(len(msg)):
            stage_probs = self.process_stage(probability_table, stage_min, stage_max)

            msg_term = msg[msg_term_idx]
            stage_min = stage_probs[msg_term][0]
            stage_max = stage_probs[msg_term][1]

            if self.save_stages:
                encoder.append(stage_probs)

        last_stage_probs = self.process_stage(probability_table, stage_min, stage_max)
        
        if self.save_stages:
            encoder.append(last_stage_probs)

        interval_min_value, interval_max_value, encoded_msg = self.get_encoded_value(last_stage_probs)

        return encoded_msg, encoder, interval_min_value, interval_max_value

    def process_stage_binary(self, float_interval_min, float_interval_max, stage_min_bin, stage_max_bin):
        stage_mid_bin = stage_min_bin + "1"
        stage_min_bin = stage_min_bin + "0"

        stage_probs = {}
        stage_probs[0] = [stage_min_bin, stage_mid_bin]
        stage_probs[1] = [stage_mid_bin, stage_max_bin]

        return stage_probs

    def decode(self, encoded_msg, msg_length, probability_table):
        decoder = []

        decoded_msg = []

        stage_min = Decimal(0.0)
        stage_max = Decimal(1.0)

        for idx in range(msg_length):
            stage_probs = self.process_stage(probability_table, stage_min, stage_max)

            for msg_term, value in stage_probs.items():
                if encoded_msg >= value[0] and encoded_msg <= value[1]:
                    break

            decoded_msg.append(msg_term)

            stage_min = stage_probs[msg_term][0]
            stage_max = stage_probs[msg_term][1]

            if self.save_stages:
                decoder.append(stage_probs)

        if self.save_stages:
            last_stage_probs = self.process_stage(probability_table, stage_min, stage_max)
            decoder.append(last_stage_probs)

        return decoded_msg, decoder


# In[2]:


def floattobinary(float_num, num_bits=None):
    float_num = str(float_num)
    if float_num.find(".") == -1:
        # No decimals in the floating-point number.
        integers = float_num
        decimals = ""
    else:
        integers, decimals = float_num.split(".")
    decimals = "0." + decimals
    decimals = Decimal(decimals)
    integers = int(integers)

    result = ""
    num_used_bits = 0
    while True:
        mul = decimals * 2
        int_part = int(mul)
        result = result + str(int_part)
        num_used_bits = num_used_bits + 1

        decimals = mul - int(mul)
        if type(num_bits) is type(None):
            if decimals == 0:
                break
        elif num_used_bits >= num_bits:
            break
    if type(num_bits) is type(None):
        pass
    elif len(result) < num_bits:
        num_remaining_bits = num_bits - len(result)
        result = result + "0"*num_remaining_bits

    integers_bin = bin(integers)[2:]
    result = str(integers_bin) + "." + str(result)
    return result

def binarytofloat(bin_num):
    if bin_num.find(".") == -1:
        # No decimals in the binary number.
        integers = bin_num
        decimals = ""
    else:
        integers, decimals = bin_num.split(".")
    result = Decimal(0.0)

    # Working with integers.
    for idx, bit in enumerate(integers):
        if bit == "0":
            continue
        mul = 2**idx
        result = result + Decimal(mul)

    # Working with decimals.
    for idx, bit in enumerate(decimals):
        if bit == "0":
            continue
        mul = Decimal(1.0)/Decimal((2**(idx+1)))
        result = result + mul
    return result


# In[3]:


def xor(actual, random, j):
    result = '0.'
    n=len(actual)-2
    k=2
    for i in range(j,n+j):
        if actual[k] == random[i]:
            result += "0"
        else:
            result += "1"
        k=k+1
    return result


# In[4]:


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


# In[5]:


def binarytoascii(str2):
    message = ""
    while str2 != "":
        i = chr(int(str2[:8], 2))
        message = message + i
        str2 = str2[8:]
    return message


# In[6]:


f = open("text_pattern.txt")
original = f.read() 
x = ''.join(format(ord(i), '08b') for i in original)


# In[7]:


test_str = x
chunk_len = 24
res = [test_str[idx : idx + chunk_len] for idx in range(0, len(test_str), chunk_len)]


# In[8]:


# Encode the data  

AE_object=[]
binary_codes=[]
M=0
for value in res:
    frequency_table = {'0': 1, '1': 1}

    AE = ArithmeticEncoding(frequency_table=frequency_table)

    original_msg = value
    
    # Encode the message
    encoded_msg, encoder , interval_min_value, interval_max_value = AE.encode(msg=original_msg, probability_table=AE.probability_table)
    
    
    # Get the binary code out of the floating-point value
    binary_code = floattobinary(encoded_msg)
    
    binary_codes.append(binary_code)
    AE_object.append(AE)
    M = M+len(binary_code)-2


# In[9]:


print("Space usage in bits before compression:", len(x))  
print("Space usage in bits after compression:",  M)  


# In[10]:


dist = [0,10,100,200,500,5000]
print("Original text")
print(original)
print()

for d in dist:
    print('d = ', d)

    # generate random binary string of length M' : CHANNEL ERROR
    M_error = random_pattern(d, M)
    
    j=0
    d_temp=[]
    for i in range(0,len(AE_object)):
        
        # take xor of text file and random string :TRANSMITTED MESSAGE
        y = xor(binary_codes[i], M_error, j)
        j=j+len(binary_code)-2
        encoded_msg = binarytofloat(y)
        
        # Decode the message
        decoded_msg, decoder = AE_object[i].decode(encoded_msg=encoded_msg, msg_length=chunk_len,
                                         probability_table=AE_object[i].probability_table)
        decoded_msg = "".join(decoded_msg)
        d_temp.append(decoded_msg)

    decoded="".join(d_temp)
    final=binarytoascii(decoded)
    print(final)
    print()


# In[ ]:




