import Parser.parser;
import Scanner.Scanner;
import java_cup.runtime.XMLElement;
import javax.xml.stream.XMLOutputFactory;
import javax.xml.stream.XMLStreamWriter;
import java_cup.runtime.ComplexSymbolFactory;
import java_cup.runtime.ScannerBuffer;
import java.io.*;
import java.nio.file.Files;

import javax.xml.transform.*;
import javax.xml.transform.stream.*;


/**
 * Created by Bzr on 2/13/2017.
 */
public class Main {
    public static void main(String args[]) throws Exception {
        // initialize the symbol factory
        ComplexSymbolFactory csf = new ComplexSymbolFactory();
        // create a buffering scanner wrapper
        ScannerBuffer lexer = new ScannerBuffer(new Scanner(new BufferedReader(new FileReader(args[0])),csf));
        // start parsing
        parser p = new parser(lexer,csf);
        XMLElement e = (XMLElement)p.parse().value;
        // create XML output file
        XMLOutputFactory outFactory = XMLOutputFactory.newInstance();
        XMLStreamWriter sw = outFactory.createXMLStreamWriter(new FileOutputStream("temp.xml"),"utf-8");
        // dump XML output to the file
        XMLElement.dump(lexer,sw,e);

        // transform the parse tree into an AST and a rendered HTML version
        Transformer transformer = TransformerFactory.newInstance()
                .newTransformer(new StreamSource(new File("tree.xsl")));
        Source text = new StreamSource(new File("temp.xml"));
        transformer.transform(text, new StreamResult(new File(args[1]+".xml")));
        transformer = TransformerFactory.newInstance()
                .newTransformer(new StreamSource(new File("tree-view.xsl")));
        text = new StreamSource(new File(args[1]+".xml"));
        transformer.transform(text, new StreamResult(new File(args[1])));

        //File tree = new File ("ast.html");
        //File xml = new File (args[1]);
        //File xmlParent = xml.getParentFile();
        //Files.copy(tree.toPath(), xmlParent.toPath());
        //This is taken from one of the examples on the CUP website
        //http://www2.cs.tum.edu/projects/cup/
    }
}
