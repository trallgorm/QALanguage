package Scanner;
import java_cup.runtime.*;
import Parser.sym;
import java_cup.runtime.ComplexSymbolFactory;
import java_cup.runtime.ComplexSymbolFactory.Location;

%%

%public
%class Scanner
%implements Parser.sym

%unicode

%line
%column

%cup
%cupdebug

%{
  StringBuilder string = new StringBuilder();

  public Scanner(java.io.Reader in, ComplexSymbolFactory sf){
  	this(in);
  	symbolFactory = sf;
  }
  ComplexSymbolFactory symbolFactory;

  private Symbol symbol(String name, int sym) {
      return symbolFactory.newSymbol(name, sym, new Location(yyline+1,yycolumn+1,yychar), new Location(yyline+1,yycolumn+yylength(),yychar+yylength()));
  }

  private Symbol symbol(String name, int sym, Object val) {
      Location left = new Location(yyline+1,yycolumn+1,yychar);
      Location right= new Location(yyline+1,yycolumn+yylength(), yychar+yylength());
      return symbolFactory.newSymbol(name, sym, left, right,val);
  }
  private Symbol symbol(String name, int sym, Object val,int buflength) {
      Location left = new Location(yyline+1,yycolumn+yylength()-buflength,yychar+yylength()-buflength);
      Location right= new Location(yyline+1,yycolumn+yylength(), yychar+yylength());
      return symbolFactory.newSymbol(name, sym, left, right,val);
  }
%}


/* main character classes */
/*
Letter= [A-Za-z_]
Digit= [0-9]
*/
IntegerLiteral = 0 | [1-9][0-9]*

WhiteSpace = [ \t\f]+

ID	= [A-Za-z_] ([A-Za-z_] | [0-9])*

LineTerminator = \r|\n|\r\n
InputCharacter = [^\r\n]

/* string and character literals */
StringCharacter = [^\r\n\"\\]

URL = (ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?

%state STRING, CHARLITERAL

%%
<YYINITIAL> {
	/* keywords */
	"main"  						{ return symbol("", MAIN); }
	"step" 							{ return symbol("",STEPLITERAL); }
	"button"						{ return symbol("",BUTTON); }
	"webpage"						{ return symbol("",WEBPAGE); }
	"textfield"						{ return symbol("",TEXTFIELD); }
	"that"							{ return symbol("",THAT); }
	"those"							{ return symbol("",THAT); }
	"has"							{ return symbol("",HAVE); }
	"have"							{ return symbol("",HAVE); }
	"current"						{ return symbol("",LOCALITYINDIC); }
	"at"							{ return symbol("",POSITIONINDIC); }
	"contain"						{ return symbol("",CONTAIN); }
	"contains"						{ return symbol("",CONTAIN); }
	"time"							{ return symbol("",TIME); }
	"times"							{ return symbol("",TIME); }
	"there"							{ return symbol("",THERE); }
	"is"							{ return symbol("",IS); }
	"exists"						{ return symbol("",EXISTS); }
	"be"							{ return symbol("",BE); }
	"label"							{ return symbol("",ATTRIBUTE); }
	"title"							{ return symbol("",ATTRIBUTE); }
	"with"							{ return symbol("",WITH); }
	"should"						{ return symbol("",SHOULD); }
	"value"							{ return symbol("",VALUE); }
	"do"							{ return symbol("",DO); }
	"if"							{ return symbol("",IF); }
	"go"							{ return symbol("",GO); }
	"to"							{ return symbol("",TO); }
	"into"							{ return symbol("",INTO); }
	"enter"							{ return symbol("",ENTER); }
	"otherwise"						{ return symbol("",OTHERWISE); }
    "exit"                          { return symbol("",EXIT); }
    "click"                         { return symbol("",CLICK); }
    "refresh"                       { return symbol("",REFRESH); }
    "number"                        { return symbol("",NUMBER); }
    "text"                          { return symbol("",TEXT); }
    "plus"                          { return symbol("",PLUS); }
    "minus"                         { return symbol("",MINUS); }
    "from"                          { return symbol("",FROM); }
    "URL"                           { return symbol("", URL_LITERAL);}
    "predefined"                    { return symbol("", PREDEFINED);}
	/* separators */
	":" 							{ return symbol("",COLON); }
	"|" 							{ return symbol("",PIPE); }

	{LineTerminator}				{ return symbol("",NEWLINE); }

	{URL}							{ return symbol("",URL, yytext()); }
	/* identifiers */ 
    {ID}                  	        { return symbol("",ID, yytext()); }
	
	/* numeric literals */
	{IntegerLiteral}           		{ return symbol("",INTEGER, new Integer(yytext())); }
	
	/* string literal */
	\"                             { yybegin(STRING); string.setLength(0); }
	
	/* whitespace */
	{WhiteSpace}                   {/*ignore*/}/*{ return symbol(WS); }*/

}

<STRING> {
  \"                             { yybegin(YYINITIAL); return symbol("",STRING_LITERAL, string.toString()); }
  
  {StringCharacter}+             { string.append( yytext() ); }
  
  /* escape sequences */
  "\\b"                          { string.append( '\b' ); }
  "\\t"                          { string.append( '\t' ); }
  "\\n"                          { string.append( '\n' ); }
  "\\f"                          { string.append( '\f' ); }
  "\\r"                          { string.append( '\r' ); }
  "\\\""                         { string.append( '\"' ); }
  "\\'"                          { string.append( '\'' ); }
  "\\\\"                         { string.append( '\\' ); }
  
  /* error cases */
  \\.                            { throw new RuntimeException("Illegal escape sequence \""+yytext()+"\""); }
  {LineTerminator}               { throw new RuntimeException("Unterminated string at end of line"); }
}

%%

/* error fallback */
[^]                              { throw new RuntimeException("Illegal character \""+yytext()+
                                                              "\" at line "+yyline+", column "+yycolumn); }
<<EOF>>                          { return symbol("", EOF); }