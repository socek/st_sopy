from sublime_plugin import TextCommand
from sublime_plugin import TextInputHandler

from .stringcase import pascalcase
from .stringcase import snakecase


def is_python(view):
    return view.match_selector(0, "source.python")


class NameInput(TextInputHandler):
    def name(self):
        return "name"


class SopyCommand(TextCommand):
    def is_enabled(self):
        return is_python(self.view)

    def is_visible(self):
        return is_python(self.view)

    def input(self, *args):
        return NameInput()


class TestClsSnippetCommand(SopyCommand):
    TEMPLATE = """class Test{name_pascal}{inheritance}:
    def test_normal(self):
        {name}"""

    def run(self, edit, name):
        sels = self.view.sel()
        inheritance = ""
        text = self.TEMPLATE.format(
            name=name, name_pascal=pascalcase(name), inheritance=inheritance
        )
        self.view.insert(edit, sels[0].begin(), text)


class MockSnippetCommand(SopyCommand):
    TEMPLATE = """m{name_snake} = mock("{name}")
    """

    def run(self, edit, name):
        sels = self.view.sel()
        inheritance = ""
        text = self.TEMPLATE.format(
            name=name, name_snake=snakecase(name), inheritance=inheritance
        )
        self.view.insert(edit, sels[0].begin(), text)


class ImportTemplate:
    _import_template = "import {0}"
    _from_template = "from {0} import {1}"

    def __init__(self, importurl):
        self.importurl = importurl

    @property
    def left(self):
        return self.importurl.rsplit(".", maxsplit=1)[0]

    @property
    def right(self):
        try:
            return self.importurl.rsplit(".", maxsplit=1)[1:][0]
        except IndexError:
            return ""

    @property
    def fullline(self):
        if self.right:
            return self._from_template.format(self.left, self.right)
        else:
            return self._import_template.format(self.left)


class ImportInput(TextInputHandler):
    def __init__(self):
        super().__init__()
        self.text = ""

    def name(self):
        return "importurl"

    def preview(self, text):
        return ImportTemplate(text).fullline


class ImportSnippetCommand(TextCommand):
    def is_enabled(self):
        return is_python(self.view)

    is_visible = is_enabled

    def run(self, edit, importurl):
        line_num = 0  # line number that signature will go on
        line = self.view.text_point(line_num, 0)
        self.view.insert(edit, line, ImportTemplate(importurl).fullline + "\n")

    def input(self, *args):
        return ImportInput()
