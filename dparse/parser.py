# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import yaml
from pkg_resources import parse_requirements
import json

# Python 2 & 3 compatible StringIO
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

# Python 2 & 3 compatible Configparser
try:
    from ConfigParser import SafeConfigParser, NoOptionError
except ImportError:
    from configparser import SafeConfigParser, NoOptionError

from .regex import URL_REGEX, HASH_REGEX
from .errors import UnknownDependencyFileError
from . import filetypes


class Dependency(object):

    def __init__(self, name, specs, line, extras=None, line_numbers=None, index_server=None, hashes=(), dependency_type=None):
        self.name = name
        self.key = name.lower().replace("_", "-")
        self.specs = specs
        self.line = line
        self.line_numbers = line_numbers
        self.index_server = index_server
        self.hashes = hashes
        self.dependency_type = dependency_type
        self.extras = extras

    def __str__(self):
        return "Requirement({name}, {specs}, {line})".format(
            name=self.name,
            specs=self.specs,
            line=self.line
        )

    def serialize(self):
        return {
            "name": self.name,
            "specs": self.specs,
            "line": self.line,
            "line_numbers": self.line_numbers,
            "index_server": self.index_server,
            "hashes": self.hashes,
            "dependency_type": self.dependency_type,
            "extras": self.extras
        }


class RequirementsDependency(Dependency):

    @property
    def full_name(self):
        if self.extras:
            return "{}[{}]".format(self.name, ",".join(self.extras))
        return self.name

    @classmethod
    def parse(cls, line):
        # setuptools requires a space before the comment. If this isn't the case, add it.
        if "\t#" in line:
            parsed, = parse_requirements(line.replace("\t#", "\t #"))
        else:
            parsed, = parse_requirements(line)
        dep = cls(
            name=parsed.project_name,
            specs=parsed.specs,
            line=line,
            extras=parsed.extras
        )
        dep.dependency_type = filetypes.requirements_txt
        return dep

    def update(self, content, version, spec="==", hashes=()):
        """
        Updates the requirement to the latest version for the given content and adds hashes
        if neccessary.
        :param content: str, content
        :return: str, updated content
        """
        new_line = "{name}{spec}{version}".format(name=self.full_name, spec=spec, version=version)
        appendix = ''
        # leave environment markers intact
        if ";" in self.line:
            # condense multiline, split out the env marker, strip comments and --hashes
            new_line += ";" + self.line.splitlines()[0].split(";", 1)[1] \
                .split("#")[0].split("--hash")[0].rstrip()
        # add the comment
        if "#" in self.line:
            # split the line into parts: requirement and comment
            parts = self.line.split("#")
            requirement, comment = parts[0], "#".join(parts[1:])
            # find all whitespaces between the requirement and the comment
            whitespaces = (hex(ord('\t')), hex(ord(' ')))
            trailing_whitespace = ''
            for c in requirement[::-1]:
                if hex(ord(c)) in whitespaces:
                    trailing_whitespace += c
                else:
                    break
            appendix += trailing_whitespace + "#" + comment
        # if this is a hashed requirement, add a multiline break before the comment
        if self.hashes and not new_line.endswith("\\"):
            new_line += " \\"
        # if this is a hashed requirement, add the hashes
        if hashes:
            for n, new_hash in enumerate(hashes):
                new_line += "\n    --hash=sha256:{}".format(new_hash)
                # append a new multiline break if this is not the last line
                if len(hashes) > n + 1:
                    new_line += " \\"
        new_line += appendix

        if self.dependency_type in [filetypes.tox_ini, filetypes.conda_yml]:
            regex = r"{}(?=\s*\r?\n?$)".format(re.escape(self.line))
        else:
            regex = r"^{}(?=\s*\r?\n?$)".format(re.escape(self.line))

        return re.sub(regex, new_line, content, flags=re.MULTILINE)


class Marker(object):

    IGNORE_LINE = 1
    IGNORE_FILE = 2

    def __init__(self, marker, marker_type):
        self.marker = marker
        self.marker_type = marker_type

    @property
    def is_line_marker(self):
        return self.marker_type == Marker.IGNORE_LINE

    @property
    def is_file_marker(self):
        return self.marker_type == Marker.IGNORE_FILE


class DependencyFile(object):
    """

    """

    def __init__(self, content, path=None, sha=None, marker=frozenset()):
        """

        :param content:
        :param path:
        :param sha:
        :param marker:
        """
        self.content = content
        self.path = path
        self.sha = sha
        self.marker = marker

        self.dependencies = []
        self.resolved_files = []
        self.is_valid = False

        self._line_marker = frozenset([m.marker for m in marker if m.is_line_marker])
        self._file_marker = frozenset([m.marker for m in marker if m.is_file_marker])

        self._lines = None

    def serialize(self):
        return {
            "file_type": self.file_type,
            "content": self.content,
            "path": self.path,
            "sha": self.sha,
            "dependencies": [dep.serialize() for dep in self.dependencies]
        }

    def json(self):
        return json.dumps(self.serialize(), indent=2)

    @property
    def is_marked_file(self):
        n = 0
        for line in enumerate(self.iter_lines()):
            for marker in self._file_marker:
                if marker in line:
                    return True
            if n >= 2:
                break
        return False

    def is_marked_line(self, line):
        for marker in self._line_marker:
            if marker in line:
                return True
        return False

    @property
    def lines(self):
        if self._lines is None:
            self._lines = self.content.splitlines()
        return self._lines

    @classmethod
    def parse_index_server(cls, line):
        """

        :param line:
        :return:
        """
        matches = URL_REGEX.findall(line)
        if matches:
            url = matches[0]
            return url if url.endswith("/") else url + "/"
        return None

    @classmethod
    def parse_hashes(cls, line):
        """
        Parses hashes on the given line
        :param line: str, line
        :return: tuple, (str line, list hashes)
        """
        hashes = []
        for match in re.finditer(HASH_REGEX, line):
            hashes.append(line[match.start():match.end()])
        return re.sub(HASH_REGEX, "", line).strip(), hashes

    def parse(self):
        if self.is_marked_file:
            self.is_valid = False
            return self

        self._parse()

        self.is_valid = len(self.dependencies) > 0 or len(self.resolved_files) > 0
        return self

    def _parse(self):
        raise NotImplementedError

    @property
    def file_type(self):
        raise NotImplementedError

    def iter_lines(self, lineno=0):
        for line in self.lines[lineno:]:
            yield line

    @classmethod
    def resolve_file(cls, file_path, line):
        line = line.replace("-r ", "").replace("--requirement ", "")
        parts = file_path.split("/")
        if " #" in line:
            line = line.split("#")[0].strip()
        if len(parts) == 1:
            return line
        return "/".join(parts[:-1]) + "/" + line


class RequirementsTXT(DependencyFile):

    @property
    def file_type(self):
        return filetypes.requirements_txt

    def _parse(self):
        """
        Parses a requirements.txt-like file
        """
        index_server = None
        for num, line in enumerate(self.iter_lines()):
            line = line.rstrip()
            if not line:
                continue
            if line.startswith('#'):
                # comments are lines that start with # only
                continue
            if line.startswith('-i') or \
                line.startswith('--index-url') or \
                line.startswith('--extra-index-url'):
                # this file is using a private index server, try to parse it
                index_server = self.parse_index_server(line)
                continue
            elif self.path and (line.startswith('-r') or line.startswith('--requirement')):
                self.resolved_files.append(self.resolve_file(self.path, line))
            elif line.startswith('-f') or line.startswith('--find-links') or \
                line.startswith('--no-index') or line.startswith('--allow-external') or \
                line.startswith('--allow-unverified') or line.startswith('-Z') or \
                line.startswith('--always-unzip'):
                continue
            elif self.is_marked_line(line):
                continue
            else:
                try:

                    parseable_line = line

                    # multiline requirements are not parseable
                    if "\\" in line:
                        parseable_line = line.replace("\\", "")
                        for next_line in self.iter_lines(num + 1):
                            parseable_line += next_line.strip().replace("\\", "")
                            line += "\n" + next_line
                            if "\\" in next_line:
                                continue
                            break

                    hashes = []
                    if "--hash" in parseable_line:
                        parseable_line, hashes = DependencyFile.parse_hashes(parseable_line)

                    req = RequirementsDependency.parse(parseable_line)
                    req.hashes = hashes
                    req.index_server = index_server
                    # replace the requirements line with the 'real' line
                    req.line = line
                    self.dependencies.append(req)
                except ValueError:
                    continue


class ToxINI(DependencyFile):

    @property
    def file_type(self):
        return filetypes.tox_ini

    def _parse(self):
        parser = SafeConfigParser()
        parser.readfp(StringIO(self.content))
        for section in parser.sections():
            try:
                content = parser.get(section=section, option="deps")
                for n, line in enumerate(content.splitlines()):
                    if self.is_marked_line(line):
                        continue
                    if line:
                        req = RequirementsDependency.parse(line)
                        req.dependency_type = self.file_type
                        self.dependencies.append(req)
            except NoOptionError:
                pass


class CondaYML(DependencyFile):

    @property
    def file_type(self):
        return filetypes.conda_yml

    def _parse(self):
        try:
            data = yaml.safe_load(self.content)
            if 'dependencies' in data and isinstance(data['dependencies'], list):
                for dep in data['dependencies']:
                    if isinstance(dep, dict) and 'pip' in dep:
                        for n, line in enumerate(dep['pip']):
                            if self.is_marked_line(line):
                                continue
                            req = RequirementsDependency.parse(line)
                            req.dependency_type = self.file_type
                            self.dependencies.append(req)
        except yaml.YAMLError:
            pass


def parse(content, filetype=None, path=None , sha=None, marker=frozenset(), strict=False):

    if filetype is not None:
        if filetype == filetypes.requirements_txt:
            klass = RequirementsTXT
        elif filetype == filetypes.tox_ini:
            klass = ToxINI
        elif filetype == filetypes.conda_yml:
            klass = CondaYML
    elif path is not None:
        if path.endswith(".txt"):
            klass = RequirementsTXT
        elif path.endswith(".yml"):
            klass = CondaYML
        elif path.endswith(".ini"):
            klass = ToxINI
    elif not strict:
        # todo: add requirement files detection?
        # assuming requirements.txt
        klass = RequirementsTXT
    else:
        raise UnknownDependencyFileError

    instance = klass(
        content=content,
        path=path,
        sha=sha,
        marker=marker
    )

    return instance.parse()
