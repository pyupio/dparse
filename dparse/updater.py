# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import re


class RequirementsTXTUpdater(object):

    SUB_REGEX = r"^{}(?=\s*\r?\n?$)"

    @classmethod
    def update(cls, content, dependency, version, spec="==", hashes=()):
        """
        Updates the requirement to the latest version for the given content and adds hashes
        if neccessary.
        :param content: str, content
        :return: str, updated content
        """
        new_line = "{name}{spec}{version}".format(name=dependency.full_name, spec=spec, version=version)
        appendix = ''
        # leave environment markers intact
        if ";" in dependency.line:
            # condense multiline, split out the env marker, strip comments and --hashes
            new_line += ";" + dependency.line.splitlines()[0].split(";", 1)[1] \
                .split("#")[0].split("--hash")[0].rstrip()
        # add the comment
        if "#" in dependency.line:
            # split the line into parts: requirement and comment
            parts = dependency.line.split("#")
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
        if dependency.hashes and not new_line.endswith("\\"):
            new_line += " \\"
        # if this is a hashed requirement, add the hashes
        if hashes:
            for n, new_hash in enumerate(hashes):
                new_line += "\n    --hash={method}:{hash}".format(
                    method=new_hash['method'],
                    hash=new_hash['hash']
                )
                # append a new multiline break if this is not the last line
                if len(hashes) > n + 1:
                    new_line += " \\"
        new_line += appendix

        regex = cls.SUB_REGEX.format(re.escape(dependency.line))

        return re.sub(regex, new_line, content, flags=re.MULTILINE)


class CondaYMLUpdater(RequirementsTXTUpdater):

    SUB_REGEX = r"{}(?=\s*\r?\n?$)"


class ToxINIUpdater(CondaYMLUpdater):
    pass
