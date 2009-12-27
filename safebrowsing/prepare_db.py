import re
import urllib2
import string
from backend import DbObj

URL="http://sb.google.com/safebrowsing/update?client=api&apikey=${key}&version=goog-${badware_type}-hash:${version}"

class Google_Blacklist(object):
    """
    Google Blacklist class that is used to fetch and prepare hashes to be
    stored in the database.
    """
    def __init__(self,badware_type="malware"):
        """
        The constructor initializes the module.
        """
        self.backend = DbObj().backend
        self.url = self._get_URL()
        badware_dict = {"malware": "M","black": "B"}
        self.badware_type = badware_type
        if not badware_type in badware_dict:
            raise KeyError("Invalid Badware Type")
        self.badware_code = badware_dict[badware_type]
        self.remove_row_regexp = re.compile("^-\w+")

    def _get_URL(self):
        return URL

    def fetch_data(self):
        version = self.backend.get_version(self.badware_type)
        st = string.Template(self.url)
        if not version:
            # Start the version number from the beginning
            self.version_number = "1:-1"
        else:
            self.version_number = version
        self.final_url = st.safe_substitute(key = self.backend.api_key,
                                            badware_type = self.badware_type,
                                            version = self.version_number)
        self.fetch_url_pointer = urllib2.urlopen(self.final_url)
        self.url_hashes_data = self.fetch_url_pointer.readlines()
        if self.url_hashes_data == []:
            # No data, so no point checking version 
            # number. This case might be because of
            # throttling or no updates available.
            return 0
        for url_hash in self.url_hashes_data[1:-1]:
            if self.remove_row_regexp.match(url_hash):
                self.backend.delete_row(self.badware_code, url_hash[1:].strip())
                del self.url_hashes_data[self.url_hashes_data.index(url_hash)]

        version_number_rx = re.compile("\d\.\d+").search(self.url_hashes_data[0])
        new_version_number = ":".join(version_number_rx.group().split("."))
        if self.version_number == "1:-1":
            self.version_number = new_version_number
            self.backend.insert_version_row(self.badware_type, self.version_number)
        else:
            self.backend.update_version_row(self.badware_type, new_version_number, self.version_number)
        for url_hash in self.url_hashes_data[1:]:
            if not url_hash == '\n':
                self.backend.insert_row(self.badware_code, url_hash[1:].strip())
        return 0
