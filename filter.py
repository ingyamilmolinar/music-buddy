from difflib import SequenceMatcher
import re

class Filter:
    
    def __init__(self):
        self.skip = re.compile(r'live', re.IGNORECASE)

    def FilterResults(self, results, song, artist):
        best_ratio = 0.0
        for result in results:
            if self.ShouldSkip(result['title']):
                continue
            result_title = self.CleanupTitle(result['title'])
            expected_titles = self.CleanupTitles(self.ExpectedTitles(artist, song))
            ratios = self.ComputeRatios(result_title, expected_titles)
            max_ratio = max(ratios)
            if max_ratio > best_ratio:
                best_ratio = max_ratio
                best_result = result
        return best_result, best_ratio

    def ExpectedTitles(self, artist, song):
        return [
            song,
            song + ' lyrics',
            song + ' letra',
            song + ' audio',
            song + ' vid',
            song + ' official audio',
            song + ' official vid',
            song + ' ' + artist,
            song + ' ' + artist + ' lyrics',
            song + ' ' + artist + ' letra',
            song + ' ' + artist + ' audio',
            song + ' ' + artist + ' vid',
            song + ' ' + artist + ' official audio',
            song + ' ' + artist + ' official vid',
            artist + ' ' + song,
            artist + ' ' + song + ' lyrics',
            artist + ' ' + song + ' letra',
            artist + ' ' + song + ' audio',
            artist + ' ' + song + ' vid',
            artist + ' ' + song + ' official audio',
            artist + ' ' + song + ' official vid',
        ]

    def ComputeRatios(self, result_title, expected_titles):
        ratios = []
        for expected_title in expected_titles:
            ratios.append(SequenceMatcher(None, result_title, expected_title).ratio())
        return ratios

    def CleanupTitles(self, titles):
        return map(self.CleanupTitle, titles)

    def CleanupTitle(self, title):
        return title.\
            replace('-',' ').\
            replace('\'', '').\
            replace('\"', '').\
            lower().\
            strip()

    def ShouldSkip(self, title):
        return self.skip.match(title)
