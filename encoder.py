
# open CMU.in.IPA.txt
# read each line
# split each line by ,
# create a dictionary with key as the first element and value as the second element
# values are stored as a list of strings
# for each key, create a list of strings
# keys with key(x) format value is added to the list of strings for key
# save as json

import json
import csv


def read_csv(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

# read the csv file
data = read_csv('CMU.in.IPA.txt')

# print(data)

# remove [\t] from start of each line
data = [(line[0],line[1].replace('\t', '')) for line in data if line.__len__() > 1]

# print(data)

# create a dictionary with key as the first element and value as the second element
ipa_dict = {}
for line in data:

    # remove trailing (x) where x is 1,2,3, or 4
    key = line[0].split('(')[0]

    if key not in ipa_dict:
        ipa_dict[key] = []

    ipa_dict[key].append(line[1])

# print(ipa_dict)

# get a list of all characters that appear in the key values
all_chars = []
for key in ipa_dict:
    for val in ipa_dict[key]:
        for char in val:
            if char not in all_chars:
                all_chars.append(char)

# print(all_chars)


# create a two step greedy tokenizer
# first step: tokenize from english text to ipa
# second step: tokenize from ipa to all_chars

class ipa_tokenizer():
    def __init__(self, ipa_dict, all_chars):
        self.ipa_dict = ipa_dict
        self.all_chars = all_chars
        self.max_ipa_len = max([len(val) for key in ipa_dict for val in ipa_dict[key]])
        self.context_size = all_chars.__len__() + 256

        self.all_char_to_token = {
            char: i for i, char in enumerate(all_chars)
        }

       

    def tokenize(self, text):
        # first step: tokenize from english text to ipa
        ipa_text = self.tokenize_to_ipa(text.lower())
        print(ipa_text)

        # second step: tokenize from ipa to all_chars
        all_chars_text = self.tokenize_to_all_chars(ipa_text)
        print(all_chars_text)
        return all_chars_text

    def tokenize_to_ipa(self, text):
        ipa_text = ''
        i = 0
        temptext = text
        while len(temptext) > 0:
            curslice = self.max_ipa_len
            for j in range(curslice, 0, -1):
                if temptext[:j] in self.ipa_dict:
                    print(temptext[:j])
                    ipa_text += self.ipa_dict[temptext[:j]][0]
                    temptext = temptext[j:]
                    break
                elif j == 1:
                    ipa_text += temptext[:j]
                    temptext = temptext[j:]

        return ipa_text

    def tokenize_to_all_chars(self, text):
        all_char_tokens = []
        for o in text:
            if o in self.all_chars:
                all_char_tokens.append(self.all_char_to_token[o])
            else:
                # get bytes of the character
                char_bytes = o.encode('utf-8')
                for byte in char_bytes:
                    all_char_tokens.append(byte + all_chars.__len__())

        return all_char_tokens


tokenizer = ipa_tokenizer(ipa_dict, all_chars)

tokenizer.tokenize('Philosophy')