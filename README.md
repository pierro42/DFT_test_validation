# NIST Discrete Fourier Transform (Spectral) Test

This code is a python implementation based on NIST SP 800-22 Revision 1a §2.6.

[Link to the PDF](https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-22r1a.pdf)

It is inspired by [this repo](https://github.com/stevenang/randomness_testsuite)

## How does it works

### Inputs

Simply modify the following code : 

```
test_case = 2
input_file = 'data/data.pi'
maximum_size=None
plot_mode="standard"
```

- Test case 1 and 2 for NIST SP 800-22
- Test case 3 for custom file input
- Test case 4 for custom string of zeroes and 1
- plot_mode can be "standard" or "point"
- maximum_size can be a number of bits or None

### Example output

```
==================================================
Test case 2
==================================================
input data:
1100100100001111110110101010001000100001011010001100001000110100110001001100011001100010100010111000
==================================================
N1 out of bounds ( 0.1 %): 
Expected 46
Got 48
test KO
--------------------------------------------------
N0 within limits ( 0.1 %): 
Expected 47.5
Got 47.5
test OK
--------------------------------------------------
d out of bounds ( 0.1 %): 
Expected -1.376494
Got 0.4588314677411235
test KO
--------------------------------------------------
Pvalue out of bounds ( 0.1 %): 
Expected 0.168669
Got 0.6463551955394902
test KO
--------------------------------------------------
==================================================
Test case 2  CONCLUSION
==================================================
Test result for N1 : KO
Test result for N0 : OK
Test result for d : KO
Test result for Pvalue : KO
==================================================
percentile:96.0
Epsilon size:100
First subset of n/2 elements size:50
T:17.30818382602285
N1:48
N0:47.5
d:0.4588314677411235
Pvalue:0.6463551955394902
==================================================
TRUE RANDOMNESS
```

FFT plot :

![DFT](https://github.com/user-attachments/assets/d4d2bb43-01c3-4e4b-ae5c-24dc5200717c)

## Why ?

Because I've made a random number generator that was somehow failing this NIST test, and as you can see the python implementation doesn't allow to correlate results with the paper, on both examples given in the latter.

## Any idea ?

In the case 1 , if i put the truncating `offset` variable to 1 in:

```python
#3 calculate modulus of the first n/2 elements (Sprime) into S
Sprime = S[offset:epsilon_length//2]
```

I can get the same results as the paper :
```
==================================================
Test case 1  CONCLUSION
==================================================
Test result for N1 : OK
Test result for N0 : OK
Test result for d : OK
Test result for Pvalue : OK
==================================================
percentile:100.0
Epsilon size:10
First subset of n/2 elements size:4
T:5.473328305111973
N1:4
N0:4.75
d:-2.1764287503300346
Pvalue:0.02952321594993795
==================================================
TRUE RANDOMNESS
```

But, in the case 2, i have to put the `offset` variable to 2 in order to get eh same values as the paper:

```
==================================================
Test case 2  CONCLUSION
==================================================
Test result for N1 : OK
Test result for N0 : OK
Test result for d : OK
Test result for Pvalue : OK
==================================================
percentile:95.83333333333334
Epsilon size:100
First subset of n/2 elements size:48
T:17.30818382602285
N1:46
N0:47.5
d:-1.3764944032233704
Pvalue:0.16866861888781504
==================================================
TRUE RANDOMNESS
```
