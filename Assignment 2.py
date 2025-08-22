#Task1
s="Hello"
result=s.lower()
print("Input:",s)
print("Output:", result)

#Example2
s="here"
result=s.lower()
print("Input:",s)
print("Output:", result)

#Example3
s="LOVELY"
result=s.lower()
print("Input:",s)
print("Output:", result)

#Task2
s="HeLLo WoRLd"
result=s.swapcase()
print("Input:",s)
print("Output:", result)

#Task3
s="HelloWorld"
result=''.join(filter(lambda char: char.islower(), s ))
print("Input:",s)
print("Output:", result)

#Task4
s="EngiNEEr"
uppercase_count=0
lowercase_count=0
for char in s:
    if 'A'<=char<='Z':
        uppercase_count+=1
    elif 'a'<=char<= 'z':
        lowercase_count+=1
        print("Input:",s)

print('uppercase: ',uppercase_count,' ','lowercasecount ',lowercase_count)

#Task5
s="Data-Driven@2025!"
result=" "
for char in s:
    if('A'<=char<='Z') or ('a'<=char<='z'):
        result+=char
        print("Input:",s)
        print("Output:",result)

#Task6
a=3
b=4
c=5
s=(a+b+c)/2
area=(s*(s-a)*(s-b)*(s-c))**0.5
print("Input:a=",a,",b=",b,",c=",c)
print("Output:",area)

#Task7
names=["Gyan","Nathaniel","Enoch","Jason","Affum"]
print("Names Table:")
for name in names:
    print("|"+name.center(15)+"|")
    print("-"*20)
    print("\nAlternative using ljust():")
    print("_"*20)
    for name in names:
         print("|"+name.ljust(15)+"|")
         print("-"*20)
         print("|"+name.ljust(15)+"|")
         print("_"*20)
         for name in names:
            print("|"+name.rjust(15)+"|")
            print("_"*20)


#Task 8
import string
s="Hello,World!"
cleaned=s.strip()
cleaned=cleaned.translate(str.maketrans('','',string.punctuation))
cleaned=cleaned.replace(" "," ")
print("Input:", repr(s))
print("Output:",cleaned)
