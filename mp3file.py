from typing import List
from pathlib import Path

import eyed3

from chapter import Chapter
from overdrive import MediaMarker
from timestamp import Timestamp


class Mp3File(object):
    def __init__(self, filepath):
        self._filepath = Path(filepath)
        self._mp3 = eyed3.load(self._filepath)
        if self._mp3 is not None:
            self._media_markers = self._read_media_markers()
            self._chapters = self._read_id3v2_chapters()
            if len(self._chapters) == 0:
                self._chapters = self.media_markers_as_chapters

    def _read_id3v2_chapters(self):
        chapters = []
        # Find top-level toc
        for toc in self._mp3.tag.table_of_contents:
            if toc.toplevel:
                for ch_eid in toc.child_ids:
                    ch = self._mp3.tag.chapters.get(ch_eid)
                    title = ch.title
                    start, end = map(Timestamp.from_milliseconds, ch.times)
                    chapters.append(Chapter(title, start=start, end=end))
        return chapters

    def _read_media_markers(self):
        user_frames = self._mp3.tag.user_text_frames
        if 'OverDrive MediaMarkers' in user_frames:
            markers_frame = user_frames.get('OverDrive MediaMarkers')
            return MediaMarker.from_xml(markers_frame.text)
        return []

    def clean(self):
        """
        Removes existing chapter tags from the mp3 file if present.
        """
        # Remove chapters
        for chap in self._mp3.tag.chapters:
            self._mp3.tag.chapters.remove(chap.element_id)

        # Remove TOCs
        for toc in self._mp3.tag.table_of_contents:
            self._mp3.tag.table_of_contents.remove(toc.element_id)

        self._mp3.tag.save()

    def save(self) -> None:
        """
        Saves the chapters
        :return:
        """
        self.clean()

        if len(self.chapters) == 0:
            return

        toc = self._mp3.tag.table_of_contents.set(b'toc', toplevel=True, description=u'Table of Contents')

        for index, chapter in zip(range(1, len(self.chapters) + 1), self.chapters):
            start = chapter.start.total_milliseconds
            end = chapter.end.total_milliseconds
            ch_eid = 'ch{}'.format(index).encode('ascii')

            ch = self._mp3.tag.chapters.set(ch_eid, (start, end))
            ch.title = chapter.title
            toc.child_ids.append(ch.element_id)

        self._mp3.tag.save()

    @property
    def path(self):
        return self._filepath

    @property
    def duration(self) -> int:
        """
        Duration of audio file in milliseconds
        :return: number of milliseconds in mp3 file
        """
        return int(self._mp3.info.time_secs * 1000)


    @property
    def chapters(self) -> List[Chapter]:
        return self._chapters

    @property
    def media_markers_as_chapters(self) -> List[Chapter]:
        markers = self.media_markers
        chapters = []

        if len(markers) > 0:
            for prev, cur in zip(markers[:-1], markers[1:]):
                chapters.append(Chapter(title=prev.name, start=prev.time, end=cur.time))
            last_marker = markers[-1]
            chapters.append(Chapter(title=last_marker.name,
                                    start=last_marker.time,
                                    end=Timestamp.from_milliseconds(self.duration)))
        return chapters

    @property
    def media_markers(self):
        return self._media_markers

    def __str__(self):
        return "{}:\n{}".format(self.path.name,
                                '\n'.join([str(ch) for ch in self._chapters]))
