import pathlib

class File:
    def __init__(self, filename):
        self.path = pathlib.Path.cwd()
        self.path = self.path / filename
        self.handle = self.path.open('r')

    def __del__(self): 
        self.handle.close()

    def read_lines(self):
        self.handle.close()
        self.handle = self.path.open('r')
        return self.handle.readlines()

    def write_lines(self, lines):
        self.handle.close()
        self.handle = self.path.open('w+')
        self.handle.write('\n'.join(lines) + '\n')
        return lines

    def replace_line(self, line, new_line):
        self.handle.close()
        self.handle = self.path.open('r+')
        lines = self.handle.readlines()
        self.handle.seek(0)
        for l in lines:
            if l == line:
                self.handle.write(new_line)
            else:
                self.handle.write(l)
        self.handle.truncate()

    def remove_line(self, line):
        self.handle.close()
        self.handle = self.path.open('r+')
        lines = self.handle.readlines()
        self.handle.seek(0)
        for l in lines:
            if l != line:
                self.handle.write(l)
        self.handle.truncate()
