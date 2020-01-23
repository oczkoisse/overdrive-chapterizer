from pathlib import Path
from typing import List
from argparse import ArgumentParser
import xml.etree.ElementTree as ET

from recordclass import recordclass
import eyed3
from eyed3.mp3 import Mp3AudioFile

Chap = recordclass('Chap', 'title start end time')


def _time_to_milliseconds(t: str) -> int:
    """
    Converts hh:mm:ss.zzz into integer milliseconds
    :param t: a string formatted as [[hh:]mm:]ss[.zzz]
    :return: number of milliseconds
    """
    time_comp = t.strip().split(':')
    secs = 0.0
    if len(time_comp) > 0:
        secs = float(time_comp[-1])
        mins = 0
        if len(time_comp) > 1:
            mins = int(time_comp[-2])
            hours = 0
            if len(time_comp) > 2:
               hours = int(time_comp[-3])
    seconds = (hours * 3600) + (mins * 60) + secs
    return int(seconds * 1000)


def _parse_markers(markers) -> List[Chap]:
    """
    Parses markers into Chap items
    :param markers: a user frame called 'Overdrive MediaMarkers' containing XML formatted markers
    :return: a list of Chap items
    """
    if markers is None:
        return []

    titles = []
    times = []
    starts = []

    root = ET.fromstring(markers.text)
    for marker in root.iter('Marker'):
        name = marker.find('Name')
        time = marker.find('Time')
        if name is not None and time is not None:
            titles.append(name.text)
            times.append(time.text)
            starts.append(_time_to_milliseconds(time.text))

    if len(starts) > 0:
        ends = starts[1:] + [None]
    else:
        ends = [None]

    chapters = []

    for title, time, start, end in zip(titles, times, starts, ends):
        chapters.append(Chap(title=title, time=time, start=start, end=end))

    return chapters


def _load_markers(mp3: Mp3AudioFile):
    """
    Returns 'Overdrive MediaMarkers' user frame (containing markers) from the loaded mp3 file
    :param mp3: the loaded mp3 file
    :return: 'Overdrive MediaMarkers' user frame if found, else None
    """
    user_frames = mp3.tag.user_text_frames
    if 'OverDrive MediaMarkers' in user_frames:
        markers = user_frames.get('OverDrive MediaMarkers')
        return markers
    return None


def _find_mp3_files(dir: str) -> List[Path]:
    """
    Provides a list of paths to mp3 files in a given directory
    :param dir: A directory
    :return: List of mp3 file paths
    """
    p = Path(dir)
    return list(p.glob('*.mp3'))


def _remove_existing_chapter_metadata(mp3: Mp3AudioFile) -> None:
    """
    Removes existing chapter tags from the loaded mp3 file if present.
    Note that this does not save the modified tags.
    :param mp3: the loaded mp3 file
    """
    toc_eids = [toc.element_id for toc in mp3.tag.table_of_contents]
    chap_eids = [chap.element_id for chap in mp3.tag.chapters]

    if len(toc_eids) + len(chap_eids) > 0:
        print("Removing existing chapters from {}".format(mp3_file.name))

    for toc_eid in toc_eids:
        mp3.tag.table_of_contents.remove(toc_eid)

    for chap_eid in chap_eids:
        mp3.tag.chapters.remove(chap_eid)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.description = "Adds ID3v2 chapter tags to mp3 audiobook files downloaded from Overdrive"
    parser.add_argument('path', help='Path to audiobook directory')
    args = parser.parse_args()

    mp3_files = _find_mp3_files(args.path)
    for mp3_file in mp3_files:
        mp3 = eyed3.load(mp3_file)

        mp3_duration = int(mp3.info.time_secs * 1000) # Duration of audio file in milliseconds

        markers = _load_markers(mp3)
        chapters = _parse_markers(markers)

        toc = None
        if len(chapters) > 0:
            chapters[-1].end = mp3_duration

            _remove_existing_chapter_metadata(mp3)

            toc = mp3.tag.table_of_contents.set(b'toc', toplevel=True, description=u'Table of Contents')

        if toc is not None:
            for index, chapter in zip(range(1, len(chapters) + 1), chapters):
                ch = mp3.tag.chapters.set('ch{}'.format(index).encode('ascii'), (chapter.start, chapter.end))
                ch.title = chapter.title

                toc.child_ids.append(ch.element_id)
            print("Writing {} chapters to {}".format(len(chapters), mp3_file.name))
            mp3.tag.save()
            print()
