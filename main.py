from youtube_search import YoutubeSearch
from youtube_dl import YoutubeDL
from file import File
from parser import SongParser
from filter import Filter

if __name__ == "__main__":
    file = File('songs')
    parser = SongParser()
    filter = Filter()
    lines = file.read_lines()
    for line in lines:
        clean_line = parser.prepare_line(line)
        if line != clean_line:
            continue
        song, artist = parser.parse_line(clean_line)
        print(song, artist)

        success = False
        while not success:
            try:
                results = YoutubeSearch(artist + ' - ' + song, max_results=10).to_dict()
                success = True
            except KeyError:
                print('Retrying...')
        print(results)

        if len(results) == 0:
            print('ERROR: No results')
            file.replace_line(line, clean_line[:-1] + ' // No results\n')
            continue
        best_result, best_ratio = filter.FilterResults(results, song, artist)
        if best_ratio < 0.80:
            print('ERROR: Skipping result: ' + best_result['title'] + ' with ratio: ' + str(best_ratio))
            # TOFIX: Add artist name if missing
            file.replace_line(line, clean_line[:-1] + ' // Best Result: '+best_result['title']+' Ratio: '+str(best_ratio)+'\n')
            continue
        print(best_result)
        ydl_opts = {
            'outtmpl': '/Users/yamilmolinar/Music/Downloads/'+best_result['title'].replace('/','')+'.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        attempts = 0
        retry = True
        while attempts < 3 and retry:
            with YoutubeDL(ydl_opts) as ydl:
                url = 'https://www.youtube.com/'+best_result['url_suffix']
                print(url)
                try:
                    ydl.download([url])
                    retry = False
                except:
                    print("ERROR: Download failed. Retrying...")
                    retry = True
                attempts += 1
        if retry:
            print("ERROR: Download failed "+str(attempts)+" times. Skipping...")
            file.replace_line(line, clean_line[:-1] + ' // Download failed\n')
            continue
        file.remove_line(line)
