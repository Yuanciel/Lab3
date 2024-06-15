import sys
import io
import unittest
from lab1 import showDirectedGraph
from lab1 import queryBridgeWords
from lab1 import add_node_if_not_exists
from lab1 import add_edge_with_weight


class MyTestCase(unittest.TestCase):
    def testdemo(self):
        global directed_graph
        directed_graph = showDirectedGraph('input.txt')

        def test_havebridge():
            # 测试存在桥接词的情况
            bridges = queryBridgeWords('at', 'to', flag=False)
            self.assertEqual(bridges,['all'])

        def test_word1final():
            # 测试存在桥接词的情况
            bridges = queryBridgeWords('absence', 'of', flag=False)
            self.assertEqual(bridges,[])

        def test_nobridge():
            # 测试不存在桥接词的情况
            bridges = queryBridgeWords('the', 'times', flag=False)
            self.assertEqual(bridges, [])

        def test_nowords():
            # 测试图中不存在word1和word2的情况
            bridges = queryBridgeWords('elf', 'lef', flag=False)
            self.assertEqual(bridges, [])

        def test_noword1():
            # 测试图中存在word2但不存在word1的情况
            bridges = queryBridgeWords('x', 'sour', flag=False)
            self.assertEqual(bridges, [])

        def test_noword2():
            # 测试图中存在word1但不存在word2的情况
            bridges = queryBridgeWords('sour', 'y', flag=False)
            self.assertEqual(bridges, [])

        def test_text1():
            output = io.StringIO()
            sys.stdout = output
            queryBridgeWords('at', 'to', flag=True)
            sys.stdout = sys.__stdout__
            output_string = output.getvalue()
            # print(output_string)
            self.assertEqual(output_string, "The bridge words from \"at\" to \"to\" are: all\n")
            output.close()

        def test_text2():
            output = io.StringIO()
            sys.stdout = output
            queryBridgeWords('the', 'times', flag=True)
            sys.stdout = sys.__stdout__
            output_string = output.getvalue()
            # print(output_string)
            self.assertEqual(output_string, "No bridge words from \"the\" to \"times\"!\n")
            output.close()

        def test_text3():
            output = io.StringIO()
            sys.stdout = output
            queryBridgeWords('elf', 'lef', flag=True)
            sys.stdout = sys.__stdout__
            output_string = output.getvalue()
            # print(output_string)
            self.assertEqual(output_string, "No \"elf\" and \"lef\" in the graph!\n")
            output.close()

        def test_text4():
            output = io.StringIO()
            sys.stdout = output
            queryBridgeWords('x', 'sour', flag=True)
            sys.stdout = sys.__stdout__
            output_string = output.getvalue()
            # print(output_string)
            self.assertEqual(output_string, "No \"x\" in the graph!\n")
            output.close()

        def test_text5():
            output = io.StringIO()
            sys.stdout = output
            queryBridgeWords('sour', 'y', flag=True)
            sys.stdout = sys.__stdout__
            output_string = output.getvalue()
            # print(output_string)
            self.assertEqual(output_string, "No \"y\" in the graph!\n")
            output.close()

        def test_text6():
            output = io.StringIO()
            sys.stdout = output
            queryBridgeWords('the', 'for', flag=True)
            sys.stdout = sys.__stdout__
            output_string = output.getvalue()
            # print(output_string)
            self.assertEqual(output_string, "The bridge words from \"the\" to \"for\" are: clock\n")



        test_havebridge()
        test_word1final()
        test_nobridge()
        test_nowords()
        test_noword1()
        test_noword2()
        test_text1()
        test_text2()
        test_text3()
        test_text4()
        test_text5()
        test_text6()


if __name__ == '__main__':
    unittest.main()
