# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import re
import yaml

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

from .dependencies import DependencyFile, Dependency
from pkg_resources import parse_requirements
from . import filetypes


class RequirementsTXTLineParser(object):
    """

    """

    @classmethod
    def parse(cls, line):
        """

        :param line:
        :return:
        """
        # setuptools requires a space before the comment. If this isn't the case, add it.
        if "\t#" in line:
            parsed, = parse_requirements(line.replace("\t#", "\t #"))
        else:
            parsed, = parse_requirements(line)
        dep = Dependency(
            name=parsed.project_name,
            specs=parsed.specs,
            line=line,
            extras=parsed.extras,
            dependency_type=filetypes.requirements_txt
        )
        return dep


class Parser(object):
    """

    """

    def __init__(self, obj):
        """

        :param obj:
        """
        self.obj = obj
        self._lines = None

    def iter_lines(self, lineno=0):
        """

        :param lineno:
        :return:
        """
        for line in self.lines[lineno:]:
            yield line

    @property
    def lines(self):
        """

        :return:
        """
        if self._lines is None:
            self._lines = self.obj.content.splitlines()
        return self._lines

    @property
    def is_marked_file(self):
        """

        :return:
        """
        for n, line in enumerate(self.iter_lines()):
            for marker in self.obj.file_marker:
                if marker in line:
                    return True
            if n >= 2:
                break
        return False

    def is_marked_line(self, line):
        """

        :param line:
        :return:
        """
        for marker in self.obj.line_marker:
            if marker in line:
                return True
        return False

    @classmethod
    def parse_hashes(cls, line):
        """

        :param line:
        :return:
        """
        hashes = []
        for match in re.finditer(HASH_REGEX, line):
            hashes.append(line[match.start():match.end()])
        return re.sub(HASH_REGEX, "", line).strip(), hashes

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
    def resolve_file(cls, file_path, line):
        """

        :param file_path:
        :param line:
        :return:
        """
        line = line.replace("-r ", "").replace("--requirement ", "")
        parts = file_path.split("/")
        if " #" in line:
            line = line.split("#")[0].strip()
        if len(parts) == 1:
            return line
        return "/".join(parts[:-1]) + "/" + line


class RequirementsTXTParser(Parser):
    """

    """

    def parse(self):
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
            elif self.obj.path and (line.startswith('-r') or line.startswith('--requirement')):
                self.obj.resolved_files.append(self.resolve_file(self.obj.path, line))
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
                        parseable_line, hashes = Parser.parse_hashes(parseable_line)

                    req = RequirementsTXTLineParser.parse(parseable_line)
                    req.hashes = hashes
                    req.index_server = index_server
                    # replace the requirements line with the 'real' line
                    req.line = line
                    self.obj.dependencies.append(req)
                except ValueError:
                    continue


class ToxINIParser(Parser):
    """

    """

    def parse(self):
        """

        :return:
        """
        parser = SafeConfigParser()
        parser.readfp(StringIO(self.obj.content))
        for section in parser.sections():
            try:
                content = parser.get(section=section, option="deps")
                for n, line in enumerate(content.splitlines()):
                    if self.is_marked_line(line):
                        continue
                    if line:
                        req = RequirementsTXTLineParser.parse(line)
                        req.dependency_type = self.obj.file_type
                        self.obj.dependencies.append(req)
            except NoOptionError:
                pass


class CondaYMLParser(Parser):
    """

    """

    def parse(self):
        """

        :return:
        """
        try:
            data = yaml.safe_load(self.obj.content)
            if data and 'dependencies' in data and isinstance(data['dependencies'], list):
                for dep in data['dependencies']:
                    if isinstance(dep, dict) and 'pip' in dep:
                        for n, line in enumerate(dep['pip']):
                            if self.is_marked_line(line):
                                continue
                            req = RequirementsTXTLineParser.parse(line)
                            req.dependency_type = self.obj.file_type
                            self.obj.dependencies.append(req)
        except yaml.YAMLError:
            pass


def parse(content, file_type=None, path=None, sha=None, marker=((), ()), parser=None):
    """

    :param content:
    :param file_type:
    :param path:
    :param sha:
    :param marker:
    :param parser:
    :return:
    """
    dep_file = DependencyFile(
        content=content,
        path=path,
        sha=sha,
        marker=marker,
        file_type=file_type,
        parser=parser
    )

    return dep_file.parse()
