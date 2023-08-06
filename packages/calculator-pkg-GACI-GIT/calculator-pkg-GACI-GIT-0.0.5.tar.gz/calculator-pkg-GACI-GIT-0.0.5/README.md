## Gacilator

This is a calculator package created to pass my assignment. 

## Features
- make basic everyday calculations like addition and subtraction!
- Gacilator will store your last equation results in its memory -- so you don't have to! 
- you can clear your memory anytime you want
- magic

## Installation
Gacilator has no dependancies to run. 
Simply install it:

```shell
pip install calculator-pkg-GACI-GIT
```

## Example Usage
```shell
from gacilator import gacilator

calculatorObject = gacilator.calculator()
print(calculatorObject.addition(5))
#returns 5 

print(calculatorObject.addition(10))
#returns 15

```

## Available functions
- addition (adds number to the number stored in memory, e.g **calculatorObject.addition(5)**) 
- subtraction (subtracts number from the number stored in memory, e.g **calculatorObject.subtraction(5)**) 
- multiplication (multiplies number by the number stored in memory, e.g **calculatorObject.multiplication(5)**) 
- division (divides number by the number stored in memory, e.g **calculatorObject.division(5)**) 
- n root (takes root of n e.g **calculatorObject.nroot(5)**)
- memory reset (resets memory e.g **calculatorObject.reset**)
