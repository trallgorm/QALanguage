java -jar ./lib/jflex-1.6.1.jar ./src/Scanner/qatest.flex

java -jar ./lib/java-cup-11b.jar -locations -xmlactions -interface -destdir ./src/Parser/ < ./src/Parser/qatest.cup

mkdir outputs

javac -d outputs -sourcepath src -cp lib/java-cup-11b.jar;lib/jflex-1.6.1.jar src/*.java

java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/deadCodeTest01.txt outputs/deadCodeOutputs01.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/deadCodeTest02.txt outputs/deadCodeOutputs02.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/deadCodeTest03.txt outputs/deadCodeOutputs03.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/deadCodeTest04.txt outputs/deadCodeOutputs04.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/deadCodeTest05.txt outputs/deadCodeOutputs05.html

java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/concatCodeTest01.txt outputs/concatCodeTest01.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/concatCodeTest02.txt outputs/concatCodeTest02.html


pause
