# import json
# import hashlib
# import string

# import re
# import utils.objectUtils as objUtils

BOOL_TRUE_SYNONYMS = ["TRUE", "true", "True", "yes", "y", "1"]
BOOL_FALSE_SYNONYMS = ["FALSE", "false", "False", "no", "n", "0"]


def determine_boolean(value, def_val=None):
    '''
        Attempts to determine a boolean value from a string using synonyms

        ----------

        Arguments
        -------------------------
        `value` {string}
            The string to parse for a boolean value.
        [`def_val`=None] {mixed}
            The value to return if a boolean cannot be determined

        Return {bool|None|Mixed}
        ----------------------
        True if the value contains a True synonym.
        False if the value contains a False synonym.
        def_val [None] if no boolean value can be determined.


        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:10:55
        `memberOf`: parse_utils
        `version`: 1.0
        `method_name`: determine_boolean
    '''
    result = def_val
    if value in BOOL_TRUE_SYNONYMS:
        result = True
    if value in BOOL_FALSE_SYNONYMS:
        result = False
    return result
