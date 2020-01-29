import xml.etree.ElementTree as ET

from timestamp import Timestamp


class MediaMarker(object):
    def __init__(self, name: str, time: Timestamp):
        self._name = name
        self._time = time

    @classmethod
    def from_xml(cls, xml_txt: str):
        markers = []
        root = ET.fromstring(xml_txt)
        for marker in root.iter('Marker'):
            name = marker.find('Name')
            time = marker.find('Time')
            if name is not None and time is not None:
                markers.append(cls(name.text, Timestamp.from_string(time.text)))
        return markers

    @property
    def name(self):
        return self._name

    @property
    def time(self):
        return self._time
