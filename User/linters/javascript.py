from lint import Linter

class JavaScript(Linter):
    language = 'javascript'
    cmd = ('jsl', '-stdin')
    regex = r'^\((?P<line>\d+)\):\s+(?P<error>.+)'

class EmbeddedJS(JavaScript):
    language = 'html'
    selector = 'source.js.embedded.html'
