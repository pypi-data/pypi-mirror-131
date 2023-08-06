#!/bin/bash

# extracts the function names of python script that are passed via command args.Example Usage: ./function_extractor.sh ../sila2lib_implementations/RegloICC/RegloICCService/*/*servicer.py
# In this example all servicer.py scripts are listed with their respective functions

# define desired output file and location
out='test_auto_func_creator_out.py'
echo 'output file name and location is specified to be:' $out
echo 'However there will be a same terminal output'

# remove the out file if it is already existent (needed because tee -a is append)
if [ -f $out ]; then rm $out; fi

# parse command line arguments and loop over them (files)
# does string modifications to extract python functions
files="$@"
for i in $files
do
# extract the Servicer names from the filenames
class_name=$(echo $i | sed 's!../.*/!!g' | sed 's!_.*.py!!g')
echo 'class Test'$class_name':' | tee -a $out
echo '""" Test all' $class_name  'Get functions """' | tee -a $out

# read file line by line to fill the created class with test functions (def)
while read -r line
do
function_name=$(echo $line | egrep "def " | sed 's/def //g' | sed 's/(self.*//g' )	
echo $line | egrep "def " | sed 's/def /def test_/g' | sed 's/(self.*/(self):/g' | tee -a $out

# append response and assert statements if current line is a function
if [[ $line == *"def "* ]]
then	
echo '    response = self.sila_client.'$class_name'_'$function_name'()' | tee -a $out
echo '    assert response is not None' | tee -a $out
echo '    assert isinstance(response)' | tee -a $out
echo '' | tee -a $out

fi
done <$i
done

# optional: opens the file with xed editor
xed $out
