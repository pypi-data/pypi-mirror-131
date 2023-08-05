'''
    A module of utility methods used for formatting strings.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 12-09-2021 09:00:27
    `memberOf`: string_conversion
    `version`: 1.0
    `method_name`: string_conversion
'''


# import json
# import hashlib
import re
import os
import utils.objectUtils as obj


def to_snake_case(subject):
    '''
        Convert a subject to snake case.

        ----------
        Arguments
        -----------------
        `subject` {str}
            The subject to convert

        Return
        ----------
        `return` {str}
            The subject converted to snake case

        Example
        ----------            
        BeepBoop Bleep blorp => beep_boop_bleep_blorp
    '''
    subject = str(subject)
    subject = re.sub(r'([a-z])([A-Z])', r'\1_\2', subject)
    subject = subject.replace(' ', '_')
    return subject.lower()


def to_screaming_snake(subject):
    '''
        Convert a subject to screaming snake case.

        ----------
        Arguments
        -----------------
        `subject` {str}
            The subject to convert

        Return
        ----------
        `return` {str}
            The subject converted to screaming snake case

        Example
        ----------            
        BeepBoop Bleep blorp => BEEP_BOOP_BLEEP_BLORP
    '''
    return to_snake_case(subject).upper()


def leftPad(subject, max_len=2, pad_char='0'):
    '''
        Convert a subject to snake case.

        ----------
        Arguments
        -----------------
        `subject` {subject}
            The subject to convert
        `max_len` {int}
            The maximum length of the subject, if >= max_len the subject will not be padded.
        `pad_char` {subject}
            The character to pad the subject with
        Return
        ----------
        `return` {subject}
            The subject formatted with left padding

        Example
        ----------            
        leftPad("1",5,'0') // "00001"
    '''
    subject = str(subject)
    slen = len(subject)
    if slen <= max_len:
        subject = f"{pad_char * (max_len - slen)}{subject}"
    return subject


def encode_quotes(value):
    '''
        Encodes single and double quotes within the value to &apos; or &quot; respectively.

        ----------

        Arguments
        -------------------------
        `value` {string}
            The string to encode

        Return {string}
        ----------------------
        The encoded string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:15:52
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: encode_quotes
    '''
    value = value.replace("'", "&apos;")
    value = value.replace('"', "&quot;")
    return value


def decode_quotes(value):
    '''
        Decodes single and double quotes within the value from &apos; or &quot; respectively.

        ----------

        Arguments
        -------------------------
        `value` {string}
            The string to decode

        Return {string}
        ----------------------
        The decoded string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:15:52
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: encode_quotes
    '''
    value = value.replace("&apos;", "'")
    value = value.replace("&quot;", '"')
    return value


def strip_excessive_spaces(value):
    '''
        Removes excessive (2 or more consecutive) spaces from the string.

        ----------

        Arguments
        -------------------------
        `value` {string}
            The string to format.

        Return {string}
        ----------------------
        The formatted string

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:19:28
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: strip_excessive_spaces
    '''
    return re.sub(r'[\s\s]{2,}', ' ', value)


def escape_regex(value):
    '''
        Escapes regex special characters.

        ----------

        Arguments
        -------------------------
        `value` {string}
            The string to escape.

        Return {string}
        ----------------------
        The formatted string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:46:32
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: escape_regex
    '''
    regex_chars = ["\\", "^", "$", "{", "}", "[", "]", "(", ")", ".", "*", "+", "?", "<", ">", "-", "&"]
    for char in regex_chars:
        value = value.replace(char, f"\\{char}")
    return value


def file_path(value, **kwargs):
    '''
        Formats the path for use in windows.

        ----------

        Arguments
        -------------------------
        `value` {string}
            The file path to format.

        Keyword Arguments
        -------------------------
        `escape_spaces` {bool}
            if True, any segments of the path that contains a space is wrapped in quotes.

        Return {string}
        ----------------------
        The formatted file path.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:45:08
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: file_path
    '''
    escape_spaces = obj.get_kwarg(["escape spaces"], False, (bool), **kwargs)
    path_sep = escape_regex(os.path.sep)
    # print(f"path_sep: {path_sep}")
    value = re.sub(r'(\\|\/)', path_sep, value)
    regex = re.compile(rf'{path_sep}+')
    value = re.sub(regex, path_sep, value)
    if len(value) > 250:
        value = clean_path(value)
    if escape_spaces:
        path_array = value.split(os.path.sep)
        new_path_array = []
        for seg in path_array:
            seg_string = seg
            if " " in seg_string:
                seg_string = f'"{seg_string}"'
            new_path_array.append(seg_string)
        value = path_sep.join(new_path_array)
    return value


def clean_path(path):
    path = path.replace('/', os.sep).replace('\\', os.sep)
    if os.sep == '\\' and '\\\\?\\' not in path:
        # fix for Windows 260 char limit
        relative_levels = len([directory for directory in path.split(os.sep) if directory == '..'])
        cwd = [directory for directory in os.getcwd().split(os.sep)] if ':' not in path else []
        path = '\\\\?\\' + os.sep.join(cwd[:len(cwd)-relative_levels] + [directory for directory in path.split(os.sep) if directory != ''][relative_levels:])
    return path


# ----------========== ALIASES ==========----------
left_pad = leftPad
