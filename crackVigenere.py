import freqsumSquare
from pycipher import Vigenere
import random

def shiftBy(c, n):
    return chr(((ord(c) - ord('a') + n) % 26) + ord('a'))

file = open('challenge2.txt','r')
cipherText = file.read()
file.close()

normal_freqs = {'a': 0.080642499002080981, 'c': 0.026892340312538593, 'b': 0.015373768624831691, 'e': 0.12886234260657689, 'd': 0.043286671390026357, 'g': 0.019625534749730816, 'f': 0.024484713711692099, 'i': 0.06905550211598431, 'h': 0.060987267963718068, 'k': 0.0062521823678781188, 'j': 0.0011176940633901926, 'm': 0.025009719347800208, 'l': 0.041016761327711163, 'o': 0.073783151266212627, 'n': 0.069849754102356679, 'q': 0.0010648594165322703, 'p': 0.017031440203182008, 's': 0.063817324270355996, 'r': 0.06156572691936394, 'u': 0.027856851020401599, 't': 0.090246649949305979, 'w': 0.021192261444145363, 'v': 0.010257964235274787, 'y': 0.01806326249861108, 'x': 0.0016941732664605912, 'z': 0.0009695838238376564}
count = 0
keyLength = 15
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
everyNthChar = [None] * keyLength
count = 0
keyGuess = [None] * keyLength
second_keyGuess = [None] * keyLength
closest_to = 100.0

for char in cipherText:
    if count > 14:
        break
    everyNthChar[count] = char
    count = count + 1
    
count = 0
i = 0

for letter in cipherText:
    if count > 14:
        everyNthChar[i] = everyNthChar[i] + letter
    
    count = count + 1
    i = i + 1
    if i == 15:
        i = 0


i = 0
frequency = {}
while i < 15:
    for ascii in range(ord('a'), ord('a')+26):
        frequency[chr(ascii)] = float(everyNthChar[i].count(chr(ascii)))/len(everyNthChar[i])
    closest_to = 10.0
    sum_freqs_squared = 0.0
    for ltr in frequency:
        sum_freqs_squared += frequency[ltr]*frequency[ltr]#will be close to .065 if english

    for possible_key in range(1,26):
        sum_f_sqr = 0.0
        closeTosum_f_Sqr = 0.0
        for ltr in normal_freqs:
            caesar_guess = shiftBy(ltr, possible_key)
            sum_f_sqr += normal_freqs[ltr]*frequency[caesar_guess]
            closeTosum_f_Sqr = abs(sum_f_sqr - .065)
        if abs(sum_f_sqr - .065) < .005:
            keyGuess[i] = alphabet[possible_key]
           # print "Key is probably: ", possible_key, " f_sqr is ",sum_f_sqr
        elif closeTosum_f_Sqr < closest_to:
            closest_to = closeTosum_f_Sqr
            second_keyGuess[i] = alphabet[possible_key]
    i = i+1

i = 0
for key in keyGuess:
    if key == None:
        keyGuess[i] = second_keyGuess[i]
    i = i+1

print 'key is: ', keyGuess
deciphered = Vigenere(keyGuess).decipher(cipherText)
print 'plaintext: ', deciphered
