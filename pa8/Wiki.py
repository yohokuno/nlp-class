#!/usr/bin/env python
import sys, traceback, re

class Wiki:
    
    # reads in the list of wives
    def addWives(self, wivesFile):
        try:
            input = open(wivesFile)
            wives = input.readlines()
            input.close()
        except IOError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
            sys.exit(1)    
        return wives
    
    # read through the wikipedia file and attempts to extract the matching husbands. note that you will need to provide
    # two different implementations based upon the useInfoBox flag. 
    def processFile(self, f, wives, useInfoBox):
        
        husbands = ["No Answer"] * len(wives)
        
        # TODO:
        # Process the wiki file and fill the husbands Array
        # +1 for correct Answer, 0 for no answer, -1 for wrong answers
        # add 'No Answer' string as the answer when you dont want to answer
        
        for i in range(len(wives)):
            wives[i] = wives[i][:-1]

        lines = f.readlines()
        f.close()
        
        # regular expressions
        married_re = re.compile(r'married (to )?([\w ]{0,20}, )?\[\[([\w\.\| ]+)\]\]')
        wife_re = re.compile(r'wife \[\[([\w\.\| ]+)\]\]')
        spouse_re = re.compile(r'\| *[Ss]pouse *=.*\[\[([\w ]+)\]\]')
        title_re = re.compile(r'<title>([\w ]+)</title>')
        title = None

        # sequencial search
        for line in lines:
            # search title
            title_result = title_re.match(line)
            if title_result != None:
                title = title_result.group(1)

            # search married
            married_result = married_re.search(line)
            if married_result != None:
                spouse = married_result.group(3)
                if spouse.find('|'):
                    spouse = spouse.split('|')[0]
                if spouse in wives:
                    index = wives.index(spouse)
                    husbands[index] = "Who is " + title + "?"
                if title in wives:
                    index = wives.index(title)
                    husbands[index] = "Who is " + spouse + "?"
            
            # search wife
            wife_result = wife_re.search(line)
            if wife_result != None:
                spouse = wife_result.group(1)
                if spouse.find('|'):
                    spouse = spouse.split('|')[0]
                if spouse in wives:
                    index = wives.index(spouse)
                    husbands[index] = "Who is " + title + "?"

            # search spouse in the infobox
            if useInfoBox:
                spouse_result = spouse_re.match(line)
                if spouse_result != None and title != None:
                    spouse = spouse_result.group(1) 
                    index = False
                    for i in range(len(wives)):
                        if wives[i] in spouse:
                            index = i
                    if index != False:
                        husbands[index] = "Who is " + title + "?"
        """
        for wife, husband in zip(wives, husbands):
            print wife, ":", husband
        """
        return husbands
    
    # scores the results based upon the aforementioned criteria
    def evaluateAnswers(self, useInfoBox, husbandsLines, goldFile):
        correct = 0
        wrong = 0
        noAnswers = 0
        score = 0 
        try:
            goldData = open(goldFile)
            goldLines = goldData.readlines()
            goldData.close()
            
            goldLength = len(goldLines)
            husbandsLength = len(husbandsLines)
            
            if goldLength != husbandsLength:
                print('Number of lines in husbands file should be same as number of wives!')
                sys.exit(1)
            for i in range(goldLength):
                if husbandsLines[i].strip() in set(goldLines[i].strip().split('|')):
                    correct += 1
                    score += 1
                elif husbandsLines[i].strip() == 'No Answer':
                    noAnswers += 1
                else:
                    wrong += 1
                    score -= 1
        except IOError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
        if useInfoBox:
            print('Using Info Box...')
        else:
            print('No Info Box...')
        print('Correct Answers: ' + str(correct))
        print('No Answers: ' + str(noAnswers))
        print('Wrong Answers: ' + str(wrong))
        print('Total Score: ' + str(score)) 

if __name__ == '__main__':
    wikiFile = '../data/small-wiki.xml'
    wivesFile = '../data/wives.txt'
    goldFile = '../data/gold.txt'
    useInfoBox = True;
    wiki = Wiki()
    wives = wiki.addWives(wivesFile)
    husbands = wiki.processFile(open(wikiFile), wives, useInfoBox)
    wiki.evaluateAnswers(useInfoBox, husbands, goldFile)
