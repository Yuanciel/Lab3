import unittest
from lab1 import showDirectedGraph, generateNewText
# 测试生成新文本的函数generateNewText
class TestCase1(unittest.TestCase):
    def testCase1(self):
        global directed_graph
        directed_graph = showDirectedGraph("input.txt")
        self.assertEqual(generateNewText("we are"), "we are")
        
    def testCase2(self):
        self.assertEqual(generateNewText("slave should we are"), "slave what should we are")

    def testCase3(self):
        f = 0
        count1 = 0
        count2 = 0
        for i in range(100):
            s = generateNewText("you nor to go")
            if s == "you require nor services to go":
                count1 = 1
            elif s == "you top nor services to go":
                count2 = 1
            else:
                f = 1
        if count1 == 1 and count2 == 1 and f == 0:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def testCase4(self):
        self.assertEqual(generateNewText("we"), "we")

    def testCase5(self):
        global directed_graph
        directed_graph = None
        self.assertEqual(generateNewText(""), "") 


if __name__ == '__main__':
    unittest.main()