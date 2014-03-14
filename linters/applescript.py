from lint import Linter
import json
import platform
import subprocess


def clean_output(args):
    return '\n'.join([a.decode('utf8') for a in args if a])


def popen(*cmd):
    p = subprocess.Popen(cmd,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return clean_output(p.communicate())


lint_script = '''
import sys
from Foundation import NSAppleScript, NSConcreteValue, NSRange
import objc
import json

class CustomCodec(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, NSConcreteValue):
            if obj.objCType() == NSRange.__typestr__:
                r = obj.rangeValue()
                return (r.location, r.length)
        return json.JSONEncoder.default(self, obj)

def lint(code):
    code = code.decode('utf8')
    linter = NSAppleScript.alloc().initWithSource_(code)
    errors = dict(linter.compileAndReturnError_(None)[1] or {})
    objc.recycleAutoreleasePool()
    return CustomCodec().encode(errors)

if __name__ == '__main__':
    code = sys.stdin.read()
    print lint(code)
'''


find_app_script = '''
import LaunchServices
import sys
code, ref, url = LaunchServices.LSFindApplicationForInfo(
    LaunchServices.kLSUnknownCreator, None, sys.argv[1], None, None)
if url:
    sys.stdout.write(url.path().encode('utf8'))
'''


app_name_cache = {}
def find_app(name):
    if not name.endswith('.app'):
        name += '.app'
    if not name in app_name_cache:
        app = popen('/usr/bin/python', '-c', find_app_script, name)
        app_name_cache[name] = app
    return app_name_cache[name]

APP_NAME_SEL = 'string.quoted.double.application-name.applescript'


class AppleScript(Linter):
    @classmethod
    def can_lint(cls, language):
        if platform.system() != 'Darwin':
            return
        return 'AppleScript' in language

    def lint(self):
        tell_apps = [
            (region, self.view.substr(region).strip('"'))
            for region in self.view.find_by_selector(APP_NAME_SEL)
        ]
        any_invalid = False
        for region, name in tell_apps:
            if not find_app(name):
                any_invalid = True
                start = region.a + 1
                end = region.b - start - 1
                line = self.code[:start].count('\n')
                line_len = len(self.code.split('\n')[line])
                offset = 0
                if line:
                    start -= self.code[:start].rindex('\n') + 1

                end = min(line_len - start, end)
                self.highlight.range(line, start, end)
                self.error(line, 'Could not find app named {}'.format(name))

        if any_invalid:
            return

        out = self.communicate(('/usr/bin/python', '-c', lint_script), self.code)
        out = out.replace('\u2019', '\'')
        error = json.loads(out)
        if error:
            brief = error['NSAppleScriptErrorBriefMessage']
            # message = error['NSAppleScriptErrorMessage']
            start, end = error['NSAppleScriptErrorRange']

            line = self.code[:start].count('\n')
            offset = 0
            if line:
                offset = start - self.code[:start].rindex('\n')

            self.highlight.range(line, offset, end - offset)
            self.error(line, brief)
