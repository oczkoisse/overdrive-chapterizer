Audiobooks downloaded from Overdrive in MP3 format have ID3 tags that describe chapter information. 
However, those tags are usable only in Overdrive and Libby media players, and aren't supported in
general media players. 

To that end, this script parses Overdrive audiobooks for the chapter information and adds them as
[ID3v2 chapter tags](http://id3.org/id3v2-chapters-1.0).

## Requirements
- `eyed3`
- `recordclass`

## Installation
- Setup a virtual environment and install requirements
```
pip install eyed3 recordclass
```

- `python3 chapterize.py <audiobook_dir>`
