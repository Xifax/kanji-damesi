# encoding: utf-8

import subprocess


class BakaMeCab:
    """
    Simplistic MeCab wrapper.
    Calls mecab analyzer from system shell,
    then parses result into list or dictionary.
    """

    ###############
    # API methods #
    ###############

    def __init__(self, sentence):
        """Initialize simple MeCab wrapper"""
        self.command = u"echo %s | mecab"
        self.sentence = sentence
        self.words = []
        self.info = {}

    def get_words(self):
        """Parse sentence and return list of words"""
        return self.mecab().words

    def get_info(self):
        """Parse sentence into dictionary of words and corresponding info"""
        return self.mecab().info

    def get_readings(self):
        """Return only list of readings corresponding to list of words"""
        self.mecab()
        return [self.info[w].pop() for w in self.info]

    ###################
    # Utility methods #
    ###################

    def mecab(self):
        """Call mecab process"""
        self.process(
            self.call(
                self.command % self.sentence
            )
        )
        return self

    def process(self, results):
        """Process results, line by line"""
        # Word list
        for line in results:
            if 'EOS' not in line:
                self.words.append(line.split('\t').pop(0))

        # Words info
        for line in results:
            if 'EOS' not in line:
                word, info = line.split('\t')
                self.info[word] = [
                    i.strip() for i in info.split(',') if i != '*'
                ]

    def call(self, command):
        """Execute shell command"""
        try:
            return subprocess.Popen(
                command.encode('utf-8'), shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            ).stdout.readlines()
        except OSError:
            return []

'''
if __name__ == '__main__':
    parser = BakaMeCab(u'任意のディレクトリ内で')

    for word, info in parser.get_info().iteritems():
        print word
        for item in info:
            print item
        print '***'

    for reading in parser.get_readings():
        print reading
'''
