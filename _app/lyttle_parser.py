'''

use case: '[[asdfasd]]' >
use case: '[[asdf-asd]]'
use case: 'qbc[[asdf-asd]]'
use case: 'abc[[asdf-asd]]def'
use case: '[[asdf-asd]]def'
pull [[asdfasd]]
'''
class LyttleParser():
    def __init__(self, line):
        self.line=line

    def parse(self):
        results = []
        bracket = 0
        endbracket = 0

        for ch in self.line:

            if '[' == ch:
                bracket += 1
                endbracket = 0

                if bracket == 1:
                    results.append('[')
                else:
                    results[len(results) - 1] += '['

            elif ']' == ch:
                endbracket += 1
                bracket = 0
                results[len(results) - 1] += ']'

            else:
                if len(results) == 0: # when empty
                    results.append(ch)
                else:
                    if endbracket == 2:
                        results.append(ch)
                        endbracket = 0
                    else:
                        results[len(results) - 1] += ch


        results = [r for r in results if '[[' in r]

        return results

def main():
    lst = ['[[asdfasd]]'
        ,'qbc[[asdf-asd]]'
        , 'abc[[asdf-asd]]def'
        , '[[asdf-asd]]def'
        , '[[asdf-asd]] def'
        , 'axc [[A]] def [[B]] '
           ]
    for it in lst:
        print(LyttleParser(it).parse())
        #for item in LyttleParser(it).parse():
        #    if '[[' in item:
        #        print('item', item)


    # lp = LyttleParser('')

if __name__ == "__main__":
    main()