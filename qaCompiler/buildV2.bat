java -jar ./lib/jflex-1.6.1.jar ./src/Scanner/qatest.flex

java -jar ./lib/java-cup-11b.jar -locations -xmlactions -interface -destdir ./src/Parser/ < ./src/Parser/qatest.cup

mkdir outputs

javac -d outputs -sourcepath src -cp lib/java-cup-11b.jar;lib/jflex-1.6.1.jar src/*.java

java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/test0.txt outputs/outputs0.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/test1.txt outputs/outputs1.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/test2.txt outputs/outputs2.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/test3.txt outputs/outputs3.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/test4.txt outputs/outputs4.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/test5.txt outputs/outputs5.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/test6.txt outputs/outputs6.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/test7.txt outputs/outputs7.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/test8.txt outputs/outputs8.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/test9.txt outputs/outputs9.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/test10.txt outputs/outputs10.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/test11.txt outputs/outputs11.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/test12.txt outputs/outputs12.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/test13.txt outputs/outputs13.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/test14.txt outputs/outputs14.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/test15.txt outputs/outputs15.html
java -cp outputs;lib/java-cup-11b.jar;lib/jflex-1.6.1.jar Main src/TestInputs/test16.txt outputs/outputs16.html

pause
