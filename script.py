from functools import total_ordering
from re import sub


@total_ordering
class Version:

    def __init__(self, version):
        self.TO_REPLACE = {"alpha": 0, "beta": 1, "a": 0, "b": 1, "rc": 2}
        self.version = self._convert(version)
        self.split_ver = self.version.split(".")

    def _convert(self, version):

        version = version.replace("-", ".")

        for value in self.TO_REPLACE.items():
            version = version.replace(value[0], f".{value[1]}.")

        result = sub(r"\.+", ".", version)
        return sub(r"\.$", "", result)

    def __lt__(self, other):
        for i in range(len(self.split_ver)):
            if len(other.split_ver) - 1 < i:
                tmp = int(self.split_ver[len(other.split_ver)])
                if tmp in set(self.TO_REPLACE.values()):
                    return True
                else:
                    return False
            elif int(self.split_ver[i]) > int(other.split_ver[i]):
                return False
            elif int(self.split_ver[i]) < int(other.split_ver[i]):
                return True
        if len(self.split_ver) < len(other.split_ver):
            tmp = int(other.split_ver[len(self.split_ver)])
            if tmp not in set(self.TO_REPLACE.values()):
                return True
            else:
                return False
        return False

    def __eq__(self, other):
        return self.version == other.version


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"


if __name__ == "__main__":
    main()
