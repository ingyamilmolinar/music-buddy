import re

class SongParser:

    def __init__(self):
        self.comment_regex = re.compile(r' +//.*$')

    def parse_line(self, line):
        lines = line.split('-')
        song = lines[0]
        if len(lines) > 1:
            artist = lines[1]
            self.artist = artist
        else:
            artist = self.artist
        return song.strip(), artist.strip()

    def prepare_line(self, line):
        return self.comment_regex.sub('', line)
    
    def fix_lines(self, lines):
        self.artist = ''
        return map(self.fix_line, lines)
    
    def fix_line(self, line):
        song, artist = self.parse_line(line)
        return song + ' - ' + artist
