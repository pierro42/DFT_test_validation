from math import fabs as fabs
from scipy.special import erfc as erfc
import numpy as np
import matplotlib.pyplot as plt
from os import path as path
from sys import exit as sysexit


######################################################
# change those :
    
'''
test case number 1 and 2 for NIST SP 800-22 , 3 for custom input
plot_mode can be "standard" or "point"
maximum_size can be a number of bits or None
'''
test_case = 2
input_file = 'data/data.pi'
maximum_size=None
plot_mode="standard"
######################################################




#Code begins here :
filename=''

if test_case == 1:
    epsilon='1001010011'
    expected_N0=4.75
    expected_N1=4
    expected_d=-2.176429
    expected_Pvalue=0.029523
    
elif test_case == 2:
    epsilon='1100100100001111110110101010001000100001011010001100001000110100110001001100011001100010100010111000'
    expected_N0=47.5
    expected_N1=46
    expected_d=-1.376494
    expected_Pvalue=0.168669
    
elif test_case == 3:
    #table to remove any unwanted character
    translation_table = str.maketrans('', '', ''.join(chr(i) for i in range(32)) + ' \t\n\r\x0b\x0c')

       
    filename = path.basename(input_file)
    with open(input_file,'r') as file:
        epsilon = file.read()
        if maximum_size:
            epsilon=epsilon[:maximum_size]
        epsilon = epsilon.translate(translation_table)
        
    test_case=filename    

elif test_case == 4:
    epsilon='101010101010101110101010101010101010101010101010101010101010101'


else:
    sysexit("Wrong test case number")

# FUNCTIONS

def is_within_percent(a, b, n):
    tolerance = abs(b) * (n / 100)
    return abs(a - b) <= tolerance

def Bsep():
    print('='*50)
def sep():
    print('-'*50)



def testVariable(name,value,expected_value,precision,results):
    if is_within_percent(value,expected_value,precision):
        print(name,"within limits (",precision, "%): ")
        print("Expected", expected_value )
        print("Got", value)
        print("test OK")
        results.append((name,"OK"))
    else:
        print(name,"out of bounds (",precision, "%): ")
        print("Expected", expected_value )
        print("Got", value)
        print("test KO")
        results.append((name,"KO"))
    sep()
    


# Computing :

epsilon_length=len(epsilon)


#1 convert 1 and 0 into 1 and -1
X = []
for char in epsilon:
    if char == '0':
        X.append(-1)
    elif char == '1':
        X.append(1)
        
        

#2: APPLY DFT 
S = np.fft.fft(X)

offset=0
#3 calculate modulus of the first n/2 elements (Sprime) into S
Sprime = S[offset:epsilon_length//2]
Sprime_length = len(Sprime)
M = np.abs(Sprime)


#4 compute T = the 95% peak height threshold
T = np.sqrt(np.log(1/0.05)*epsilon_length)

#5 Compute N0 , the expected theoretical 95% number of peaks that are less than T
N0 = 0.95*epsilon_length/2

#6 Compute N1, the actual observed number of peaks of M that are less than T
N1=0
for i in range(Sprime_length):
    if M[i] < T:
        N1 += 1

percentile = N1/Sprime_length*100

#7 Compute d
d = (N1-N0)/np.sqrt(epsilon_length*0.95*0.05/4)

#8 Compute P-value
Pvalue = erfc(fabs(d)/np.sqrt(2))



# Printing the report
Bsep()
print("Test case",test_case)
Bsep()

print("input data:")
if epsilon_length <= 1024:
    print(epsilon)
else:
    print("Epsilon to big to be printed, check ", test_case)
Bsep()

#only do tests for standardized tests cases
if test_case < 3:
    test_results=[]
    precision=0.1 # in percent 
    testVariable("N1",N1,expected_N1,precision,test_results)
    testVariable("N0",N0,expected_N0,precision,test_results)
    testVariable("d",d,expected_d,precision,test_results)
    testVariable("Pvalue",Pvalue,expected_Pvalue,precision,test_results)
    
    
    Bsep()
    print("Test case",test_case, " CONCLUSION")
    Bsep()
    
    for test in test_results:
        print(f'Test result for {test[0]} : {test[1]}')
    Bsep()


# Additionnal data
print(f'percentile:{percentile}')
print(f'Epsilon size:{epsilon_length}')
print(f'First subset of n/2 elements size:{Sprime_length}')
print(f'T:{T}')
print(f'N1:{N1}')
print(f'N0:{N0}')
print(f'd:{d}')
print(f'Pvalue:{Pvalue}')

Bsep()

if Pvalue >=0.01:
    print("TRUE RANDOMNESS")
else:
    print("NOT RANDOM")
    
    
       
    
# Plot the FFT 
plt.figure()

if plot_mode == "standard":
    plt.plot(M)
elif plot_mode == "point":
    plt.plot(M,'.',ms=1)
else:
    sysexit("Wrong plot_mode")
    
plt.title('FFT of case'+ str(test_case))
plt.xlabel('Index')
plt.ylabel('Magnitude')
plt.xlim(right=len(M))
Tline = plt.axhline(y=T, color="black", linestyle="--")

Tline.set_label(r'$\tau \equal \sqrt{log(\frac{1}{0.05})n}\approx$'+str(int(T)))
plt.legend()
plt.show()


    
    