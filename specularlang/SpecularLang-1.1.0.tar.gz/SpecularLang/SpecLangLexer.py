# Generated from C:/Users/Emery/PycharmProjects/SpecularLang/ANTLR4\SpecLang.g4 by ANTLR 4.8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


from antlr_denter.DenterHelper import DenterHelper
from SpecularLang.SpecLangParser import SpecLangParser



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2,")
        buf.write("\u010f\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\3\2\3\2\3\3\3\3")
        buf.write("\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3")
        buf.write("\n\3\13\3\13\3\13\3\f\3\f\3\f\3\r\3\r\3\16\3\16\3\17\3")
        buf.write("\17\3\17\3\20\3\20\3\20\3\20\3\20\3\20\3\21\3\21\3\21")
        buf.write("\3\21\3\21\3\21\3\22\3\22\3\22\3\22\3\22\3\22\3\23\3\23")
        buf.write("\3\23\3\23\3\23\3\24\3\24\3\24\3\25\3\25\3\25\3\26\3\26")
        buf.write("\3\26\3\27\3\27\3\27\3\27\3\27\3\30\3\30\3\30\3\30\3\30")
        buf.write("\3\31\3\31\3\31\3\31\3\31\3\31\3\32\3\32\3\32\3\32\3\32")
        buf.write("\3\32\3\32\3\33\3\33\3\33\3\33\3\34\3\34\3\34\3\35\3\35")
        buf.write("\3\35\3\35\3\36\3\36\3\37\3\37\3 \3 \3!\3!\3\"\3\"\3\"")
        buf.write("\3\"\7\"\u00c5\n\"\f\"\16\"\u00c8\13\"\3\"\3\"\3#\3#\3")
        buf.write("#\3#\3#\3$\3$\3$\3$\3$\3$\3%\3%\3%\3%\3%\3&\3&\3&\3&\3")
        buf.write("&\3&\3&\3\'\3\'\3\'\3\'\3\'\3\'\3\'\3\'\3(\3(\7(\u00ed")
        buf.write("\n(\f(\16(\u00f0\13(\3)\6)\u00f3\n)\r)\16)\u00f4\3*\5")
        buf.write("*\u00f8\n*\3*\3*\7*\u00fc\n*\f*\16*\u00ff\13*\3*\7*\u0102")
        buf.write("\n*\f*\16*\u0105\13*\5*\u0107\n*\3+\6+\u010a\n+\r+\16")
        buf.write("+\u010b\3+\3+\4\u00c6\u010b\2,\3\3\5\4\7\5\t\6\13\7\r")
        buf.write("\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!")
        buf.write("\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63\33\65\34\67")
        buf.write("\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,\3\2\6\5\2C\\a")
        buf.write("ac|\6\2\62;C\\aac|\3\2\62;\3\2\"\"\2\u0117\2\3\3\2\2\2")
        buf.write("\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r")
        buf.write("\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3")
        buf.write("\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2")
        buf.write("\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'")
        buf.write("\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2")
        buf.write("\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\29")
        buf.write("\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2")
        buf.write("C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2")
        buf.write("\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2")
        buf.write("\2\3W\3\2\2\2\5Y\3\2\2\2\7[\3\2\2\2\t]\3\2\2\2\13_\3\2")
        buf.write("\2\2\ra\3\2\2\2\17c\3\2\2\2\21e\3\2\2\2\23g\3\2\2\2\25")
        buf.write("i\3\2\2\2\27l\3\2\2\2\31o\3\2\2\2\33q\3\2\2\2\35s\3\2")
        buf.write("\2\2\37v\3\2\2\2!|\3\2\2\2#\u0082\3\2\2\2%\u0088\3\2\2")
        buf.write("\2\'\u008d\3\2\2\2)\u0090\3\2\2\2+\u0093\3\2\2\2-\u0096")
        buf.write("\3\2\2\2/\u009b\3\2\2\2\61\u00a0\3\2\2\2\63\u00a6\3\2")
        buf.write("\2\2\65\u00ad\3\2\2\2\67\u00b1\3\2\2\29\u00b4\3\2\2\2")
        buf.write(";\u00b8\3\2\2\2=\u00ba\3\2\2\2?\u00bc\3\2\2\2A\u00be\3")
        buf.write("\2\2\2C\u00c0\3\2\2\2E\u00cb\3\2\2\2G\u00d0\3\2\2\2I\u00d6")
        buf.write("\3\2\2\2K\u00db\3\2\2\2M\u00e2\3\2\2\2O\u00ea\3\2\2\2")
        buf.write("Q\u00f2\3\2\2\2S\u00f7\3\2\2\2U\u0109\3\2\2\2WX\7]\2\2")
        buf.write("X\4\3\2\2\2YZ\7.\2\2Z\6\3\2\2\2[\\\7_\2\2\\\b\3\2\2\2")
        buf.write("]^\7?\2\2^\n\3\2\2\2_`\7B\2\2`\f\3\2\2\2ab\7<\2\2b\16")
        buf.write("\3\2\2\2cd\7*\2\2d\20\3\2\2\2ef\7+\2\2f\22\3\2\2\2gh\7")
        buf.write("=\2\2h\24\3\2\2\2ij\7?\2\2jk\7?\2\2k\26\3\2\2\2lm\7#\2")
        buf.write("\2mn\7?\2\2n\30\3\2\2\2op\7}\2\2p\32\3\2\2\2qr\7\177\2")
        buf.write("\2r\34\3\2\2\2st\7/\2\2tu\7@\2\2u\36\3\2\2\2vw\7y\2\2")
        buf.write("wx\7j\2\2xy\7k\2\2yz\7n\2\2z{\7g\2\2{ \3\2\2\2|}\7g\2")
        buf.write("\2}~\7p\2\2~\177\7v\2\2\177\u0080\7g\2\2\u0080\u0081\7")
        buf.write("t\2\2\u0081\"\3\2\2\2\u0082\u0083\7g\2\2\u0083\u0084\7")
        buf.write("z\2\2\u0084\u0085\7k\2\2\u0085\u0086\7v\2\2\u0086\u0087")
        buf.write("\7u\2\2\u0087$\3\2\2\2\u0088\u0089\7o\2\2\u0089\u008a")
        buf.write("\7q\2\2\u008a\u008b\7x\2\2\u008b\u008c\7g\2\2\u008c&\3")
        buf.write("\2\2\2\u008d\u008e\7v\2\2\u008e\u008f\7q\2\2\u008f(\3")
        buf.write("\2\2\2\u0090\u0091\7f\2\2\u0091\u0092\7q\2\2\u0092*\3")
        buf.write("\2\2\2\u0093\u0094\7k\2\2\u0094\u0095\7h\2\2\u0095,\3")
        buf.write("\2\2\2\u0096\u0097\7g\2\2\u0097\u0098\7n\2\2\u0098\u0099")
        buf.write("\7k\2\2\u0099\u009a\7h\2\2\u009a.\3\2\2\2\u009b\u009c")
        buf.write("\7g\2\2\u009c\u009d\7n\2\2\u009d\u009e\7u\2\2\u009e\u009f")
        buf.write("\7g\2\2\u009f\60\3\2\2\2\u00a0\u00a1\7u\2\2\u00a1\u00a2")
        buf.write("\7e\2\2\u00a2\u00a3\7g\2\2\u00a3\u00a4\7p\2\2\u00a4\u00a5")
        buf.write("\7g\2\2\u00a5\62\3\2\2\2\u00a6\u00a7\7i\2\2\u00a7\u00a8")
        buf.write("\7n\2\2\u00a8\u00a9\7q\2\2\u00a9\u00aa\7d\2\2\u00aa\u00ab")
        buf.write("\7c\2\2\u00ab\u00ac\7n\2\2\u00ac\64\3\2\2\2\u00ad\u00ae")
        buf.write("\7c\2\2\u00ae\u00af\7p\2\2\u00af\u00b0\7f\2\2\u00b0\66")
        buf.write("\3\2\2\2\u00b1\u00b2\7q\2\2\u00b2\u00b3\7t\2\2\u00b38")
        buf.write("\3\2\2\2\u00b4\u00b5\7p\2\2\u00b5\u00b6\7q\2\2\u00b6\u00b7")
        buf.write("\7v\2\2\u00b7:\3\2\2\2\u00b8\u00b9\7,\2\2\u00b9<\3\2\2")
        buf.write("\2\u00ba\u00bb\7\61\2\2\u00bb>\3\2\2\2\u00bc\u00bd\7-")
        buf.write("\2\2\u00bd@\3\2\2\2\u00be\u00bf\7/\2\2\u00bfB\3\2\2\2")
        buf.write("\u00c0\u00c6\7$\2\2\u00c1\u00c2\7^\2\2\u00c2\u00c5\7$")
        buf.write("\2\2\u00c3\u00c5\13\2\2\2\u00c4\u00c1\3\2\2\2\u00c4\u00c3")
        buf.write("\3\2\2\2\u00c5\u00c8\3\2\2\2\u00c6\u00c7\3\2\2\2\u00c6")
        buf.write("\u00c4\3\2\2\2\u00c7\u00c9\3\2\2\2\u00c8\u00c6\3\2\2\2")
        buf.write("\u00c9\u00ca\7$\2\2\u00caD\3\2\2\2\u00cb\u00cc\7V\2\2")
        buf.write("\u00cc\u00cd\7t\2\2\u00cd\u00ce\7w\2\2\u00ce\u00cf\7g")
        buf.write("\2\2\u00cfF\3\2\2\2\u00d0\u00d1\7H\2\2\u00d1\u00d2\7c")
        buf.write("\2\2\u00d2\u00d3\7n\2\2\u00d3\u00d4\7u\2\2\u00d4\u00d5")
        buf.write("\7g\2\2\u00d5H\3\2\2\2\u00d6\u00d7\7P\2\2\u00d7\u00d8")
        buf.write("\7q\2\2\u00d8\u00d9\7p\2\2\u00d9\u00da\7g\2\2\u00daJ\3")
        buf.write("\2\2\2\u00db\u00dc\7h\2\2\u00dc\u00dd\7c\2\2\u00dd\u00de")
        buf.write("\7f\2\2\u00de\u00df\7g\2\2\u00df\u00e0\7k\2\2\u00e0\u00e1")
        buf.write("\7p\2\2\u00e1L\3\2\2\2\u00e2\u00e3\7h\2\2\u00e3\u00e4")
        buf.write("\7c\2\2\u00e4\u00e5\7f\2\2\u00e5\u00e6\7g\2\2\u00e6\u00e7")
        buf.write("\7q\2\2\u00e7\u00e8\7w\2\2\u00e8\u00e9\7v\2\2\u00e9N\3")
        buf.write("\2\2\2\u00ea\u00ee\t\2\2\2\u00eb\u00ed\t\3\2\2\u00ec\u00eb")
        buf.write("\3\2\2\2\u00ed\u00f0\3\2\2\2\u00ee\u00ec\3\2\2\2\u00ee")
        buf.write("\u00ef\3\2\2\2\u00efP\3\2\2\2\u00f0\u00ee\3\2\2\2\u00f1")
        buf.write("\u00f3\t\4\2\2\u00f2\u00f1\3\2\2\2\u00f3\u00f4\3\2\2\2")
        buf.write("\u00f4\u00f2\3\2\2\2\u00f4\u00f5\3\2\2\2\u00f5R\3\2\2")
        buf.write("\2\u00f6\u00f8\7\17\2\2\u00f7\u00f6\3\2\2\2\u00f7\u00f8")
        buf.write("\3\2\2\2\u00f8\u00f9\3\2\2\2\u00f9\u0106\7\f\2\2\u00fa")
        buf.write("\u00fc\7\13\2\2\u00fb\u00fa\3\2\2\2\u00fc\u00ff\3\2\2")
        buf.write("\2\u00fd\u00fb\3\2\2\2\u00fd\u00fe\3\2\2\2\u00fe\u0107")
        buf.write("\3\2\2\2\u00ff\u00fd\3\2\2\2\u0100\u0102\7\"\2\2\u0101")
        buf.write("\u0100\3\2\2\2\u0102\u0105\3\2\2\2\u0103\u0101\3\2\2\2")
        buf.write("\u0103\u0104\3\2\2\2\u0104\u0107\3\2\2\2\u0105\u0103\3")
        buf.write("\2\2\2\u0106\u00fd\3\2\2\2\u0106\u0103\3\2\2\2\u0107T")
        buf.write("\3\2\2\2\u0108\u010a\t\5\2\2\u0109\u0108\3\2\2\2\u010a")
        buf.write("\u010b\3\2\2\2\u010b\u010c\3\2\2\2\u010b\u0109\3\2\2\2")
        buf.write("\u010c\u010d\3\2\2\2\u010d\u010e\b+\2\2\u010eV\3\2\2\2")
        buf.write("\f\2\u00c4\u00c6\u00ee\u00f4\u00f7\u00fd\u0103\u0106\u010b")
        buf.write("\3\b\2\2")
        return buf.getvalue()


class SpecLangLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    T__12 = 13
    NEXT = 14
    WHILE = 15
    ENTER = 16
    EXITS = 17
    MOVE = 18
    TO = 19
    DO = 20
    IF = 21
    ELIF = 22
    ELSE = 23
    SCENE = 24
    GLOBAL = 25
    AND = 26
    OR = 27
    NOT = 28
    MUL = 29
    DIV = 30
    ADD = 31
    SUB = 32
    STRING = 33
    TRUE = 34
    FALSE = 35
    NONE = 36
    FADEIN = 37
    FADEOUT = 38
    ID = 39
    NUMBER = 40
    NEWLINE = 41
    WS = 42

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'['", "','", "']'", "'='", "'@'", "':'", "'('", "')'", "';'", 
            "'=='", "'!='", "'{'", "'}'", "'->'", "'while'", "'enter'", 
            "'exits'", "'move'", "'to'", "'do'", "'if'", "'elif'", "'else'", 
            "'scene'", "'global'", "'and'", "'or'", "'not'", "'*'", "'/'", 
            "'+'", "'-'", "'True'", "'False'", "'None'", "'fadein'", "'fadeout'" ]

    symbolicNames = [ "<INVALID>",
            "NEXT", "WHILE", "ENTER", "EXITS", "MOVE", "TO", "DO", "IF", 
            "ELIF", "ELSE", "SCENE", "GLOBAL", "AND", "OR", "NOT", "MUL", 
            "DIV", "ADD", "SUB", "STRING", "TRUE", "FALSE", "NONE", "FADEIN", 
            "FADEOUT", "ID", "NUMBER", "NEWLINE", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "T__12", "NEXT", 
                  "WHILE", "ENTER", "EXITS", "MOVE", "TO", "DO", "IF", "ELIF", 
                  "ELSE", "SCENE", "GLOBAL", "AND", "OR", "NOT", "MUL", 
                  "DIV", "ADD", "SUB", "STRING", "TRUE", "FALSE", "NONE", 
                  "FADEIN", "FADEOUT", "ID", "NUMBER", "NEWLINE", "WS" ]

    grammarFileName = "SpecLang.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    class SpecDenter(DenterHelper):
        def __init__(self, lexer, nl_token, indent_token, dedent_token, ignore_eof):
            super().__init__(nl_token, indent_token, dedent_token, ignore_eof)
            self.lexer: SpecLangLexer = lexer

        def pull_token(self):
            return super(SpecLangLexer, self.lexer).nextToken()

    denter = None

    def nextToken(self):
        if not self.denter:
            self.denter = self.SpecDenter(self, self.NEWLINE, SpecLangParser.INDENT, SpecLangParser.DEDENT, False)
        return self.denter.next_token()



