
import re


def _match_files_by_pattern(files, pattern):
    for file in files:
        if re.findall(pattern, file):
            yield file


class Filter:

    def regxp_filter(self, files, filters):
        pattern = "|".join(filters)
        match = _match_files_by_pattern(files, pattern)
        return match
