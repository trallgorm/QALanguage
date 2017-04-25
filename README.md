# QALanguage

# Summary

This language allows a developer to create tests that are not only executable, but human readable as well. A developer is able to write a testcase for a program (currently limited to webapps) which can then be executed automatically. For example here is a typical example of this language. The part before the | character is the instruction and the part after the | character is the expected result

# Example

main :
step 1 : go to https://www.youtube.com/ | current URL should be https://www.youtube.com/

step 2 : enter "test" into textfield with title "masthead-search-term" | textfield with title "masthead-search-term" should have value "test"

step 3 : if there is button with value "search-btn" go to step 5 otherwise go to step 4 |

step 4 : exit |

step 5 : click button with value "search-btn" | current webpage should contain "Talko"

step 6 : refresh current webpage | current URL should be https://www.youtube.com/results?search_query=test

step 7 : do step 6 10 times |

step 8 : do refreshwebpage 5 times |

step 9 : enter 6 minus 2 into textfield with title "masthead-search-term"|

step 10 : enter "doogaga" plus "doo" into textfield with title "masthead-search-term" |

step 11: go to step 3 |



refreshwebpage :

step 1 : refresh current webpage | current URL should be https://www.youtube.com/results?search_query=test

step 2 : go to step 6 |



refresh13 :

step 1 : refresh current webpage | current URL should be https://www.youtube.com/results?search_query=test

step 2 : exit |

step 3 : go to step 1 |

# Output

A python script which runs through the steps automatically and tells the user which step of the testcase failed, if any.

# Benefits

This language could potentially be a huge time saver for QA professionals. Because the testcases can simply be executed automatically, QA personnel does not need to do any of it. And if a testcase fails, anyone can look at it and see what went wrong, as it is designed to be as human readable as possible.

# Usage 

Write your testcases and place them in src/TestInputs then run the following from the qaCompiler folder. Similar scripts are provided in qaCompiler\buildv4.bat
```
java -jar ./lib/jflex-1.6.1.jar ./src/Scanner/qatest.flex

java -jar ./lib/java-cup-11b.jar -locations -xmlactions -interface -destdir ./src/Parser/ < ./src/Parser/qatest.cup

mkdir outputs

javac -d outputs -sourcepath src -cp lib/java-cup-11b.jar;lib/jflex-1.6.1.jar src/*.java

java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/NAMEOFYOURTESTCASE.txt outputs/NAMEOFYOURTESTCASE.html
```
Where NAMEOFYOURTESTCASE is the name of your testcase. Afterwards you want to go to qaCompiler/src/PythonBackend and run the command in the form of 
```
python backend.py [IR.xml] [outputFileName] [preprocessorFileName] 
```
For example
```
python backend.py NAMEOFYOURTESTCASE.html.xml NAMEOFYOURTESTCASE.py
```
preprocessor file name is an optional parameter which allows developers to substitute pre-existing variables for easier reading.

The compiled python code should be located in qaCompiler\outputs\CompiledCode with the filename you provided.
