#!/usr/bin/env python3
# Json library support hex escape.
from .exceptions import HexsonParserException
import json


class Parser(object):
    """ Json parser. """

    def __init__(self, input_json):
        self.input_json = input_json
        self.input_len = len(input_json)
        self.cursor = 0
        self.last = self.input_json[:]
        self.utf_8_string = False

    def __update_cur(self):
        self.cursor += 1
        self.last = self.input_json[self.cursor:]

    def __cur(self):
        return self.last[0]

    def __scan_number(self):
        ret = ''

        while self.cursor < self.input_len:
            if ord(self.__cur()) >= 48 and ord(self.__cur()) <= 59:
                ret += self.__cur()
                self.__update_cur()
            elif self.__cur() == '.' or self.__cur() == '-' or self.__cur() == '+':
                ret += self.__cur()
                self.__update_cur()
            else:
                break

        try:
            return int(ret)
        except:
            return float(ret)

    def __scan_string(self, is_root=True):
        state = 'READY'
        ret = None

        while self.cursor < self.input_len:
            if state == 'READY':
                if self.__cur() == ' ' or self.__cur() == '\t' or self.__cur() == '\r' or self.__cur() == '\n':
                    # Skip blank.
                    self.__update_cur()
                    continue
                elif self.__cur() == '"':
                    # Hit entry.
                    state = 'PARSING'
                    ret = ''
                    self.__update_cur()
                elif (self.__cur() == ']' or self.__cur() == '}') and not is_root:
                    # Hit outer extry.
                    return None
                else:
                    raise HexsonParserException('Illegal syntax: ' + self.input_json)
            elif state == 'PARSING':
                if self.__cur() == '"':
                    state = 'FINISH'
                else:
                    if self.__cur() == '\\':
                        # First layer of escape.
                        self.__update_cur()
                        if self.__cur() == '"':
                            ret += '"'
                        elif self.__cur() == '\\':
                            ret += '\\'
                        elif self.__cur() == 'u':
                            # Escape for unicode.
                            self.__update_cur()
                            byte_a = self.__cur()
                            self.__update_cur()
                            byte_b = self.__cur()
                            self.__update_cur()
                            byte_c = self.__cur()
                            self.__update_cur()
                            byte_d = self.__cur()
                            ret += json.loads('"\\u' + byte_a + byte_b + byte_c + byte_d + '"')
                        else:
                            raise HexsonParserException('Illegal syntax: ' + self.input_json)
                    else:
                        ret += self.__cur()
                self.__update_cur()
            elif state == 'FINISH':
                break
            else:
                raise HexsonParserException('Illegal syntax: ' + self.input_json)

        return ret

    def __scan_bytes(self, is_root=True):
        state = 'READY'
        ret = None

        while self.cursor < self.input_len:
            if state == 'READY':
                if self.__cur() == ' ' or self.__cur() == '\t' or self.__cur() == '\r' or self.__cur() == '\n':
                    # Skip blank.
                    self.__update_cur()
                    continue
                elif self.__cur() == '"':
                    # Hit entry.
                    state = 'PARSING'
                    ret = b''
                    self.__update_cur()
                elif (self.__cur() == ']' or self.__cur() == '}') and not is_root:
                    # Hit outer extry.
                    return None
                else:
                    raise HexsonParserException('Illegal syntax: ' + self.input_json)
            elif state == 'PARSING':
                if self.__cur() == '"':
                    state = 'FINISH'
                else:
                    if self.__cur() == '\\':
                        # First layer of escape.
                        self.__update_cur()
                        if self.__cur() == '"':
                            ret += b'"'
                        elif self.__cur() == '\\':
                            # Second layer of escape.
                            self.__update_cur()
                            if self.__cur() == 'x':
                                # Escape for hex.
                                self.__update_cur()
                                byte_a = self.__cur()
                                self.__update_cur()
                                byte_b = self.__cur()
                                ret += bytes.fromhex(byte_a + byte_b)
                            elif self.__cur() == 'a':
                                # "\a"
                                ret += b'\a'
                            elif self.__cur() == 'b':
                                # "\b"
                                ret += b'\b'
                            elif self.__cur() == 't':
                                # "\t"
                                ret += b'\t'
                            elif self.__cur() == 'n':
                                # "\n"
                                ret += b'\n'
                            elif self.__cur() == 'v':
                                # "\v"
                                ret += b'\v'
                            elif self.__cur() == 'f':
                                # "\f"
                                ret += b'\f'
                            elif self.__cur() == 'r':
                                # "\r"
                                ret += b'\r'
                            else:
                                raise HexsonParserException('Illegal syntax: ' + self.input_json)
                        else:
                            raise HexsonParserException('Illegal syntax: ' + self.input_json)
                    else:
                        ret += self.__cur().encode('ascii')
                self.__update_cur()
            elif state == 'FINISH':
                break
            else:
                raise HexsonParserException('Illegal syntax: ' + self.input_json)

        return ret

    def __scan_pair(self):
        ret = [None, None]

        #
        # Get key.
        #
        key = self.__scan_string(is_root=False)
        if key is None:
            # Not got a pair.
            return None
        else:
            ret[0] = key

        #
        # Get ":".
        #
        while self.cursor < self.input_len:
            if self.__cur() == ' ' or self.__cur() == '\t' or self.__cur() == '\r' or self.__cur() == '\n':
                # Skip blank.
                self.__update_cur()
                continue
            elif self.__cur() == ':':
                self.__update_cur()
                break
            else:
                raise HexsonParserException('Illegal syntax: ' + self.input_json)

        #
        # Get value.
        #
        ret[1] = self.__scan_value(is_root=False)

        return ret

    def __scan_obj(self):
        ret = {}

        while self.cursor < self.input_len:
            if self.__cur() == ' ' or self.__cur() == '\t' or self.__cur() == '\r' or self.__cur() == '\n':
                # Skip blank.
                self.__update_cur()
                continue
            elif self.__cur() == '{':
                # Hit entry.
                self.__update_cur()
                pair = self.__scan_pair()
                while pair:
                    ret[pair[0]] = pair[1]
                    #
                    # Try to get ",".
                    #
                    while self.cursor < self.input_len:
                        if self.__cur() == ' ' or self.__cur() == '\t' or self.__cur() == '\r' or self.__cur() == '\n':
                            # Skip blank.
                            self.__update_cur()
                            continue
                        elif self.__cur() == ',':
                            self.__update_cur()
                            pair = self.__scan_pair()
                            break
                        else:
                            pair = None
                            break

            elif self.__cur() == '}':
                # Hit exitry.
                self.__update_cur()
                break
            else:
                raise HexsonParserException('Illegal syntax: ' + self.input_json)

        return ret

    def __scan_array(self):
        ret = []

        while self.cursor < self.input_len:
            if self.__cur() == ' ' or self.__cur() == '\t' or self.__cur() == '\r' or self.__cur() == '\n':
                # Skip blank.
                self.__update_cur()
                continue
            elif self.__cur() == '[':
                # Hit entry.
                self.__update_cur()
                item = self.__scan_value(is_root=False)
                while item:
                    ret.append(item)
                    #
                    # Try to get ",".
                    #
                    while self.cursor < self.input_len:
                        if self.__cur() == ' ' or self.__cur() == '\t' or self.__cur() == '\r' or self.__cur() == '\n':
                            # Skip blank.
                            self.__update_cur()
                            continue
                        elif self.__cur() == ',':
                            self.__update_cur()
                            item = self.__scan_value(is_root=False)
                            break
                        else:
                            item = None
                            break
            elif self.__cur() == ']':
                # Hit Extry.
                self.__update_cur()
                break
            else:
                raise HexsonParserException('Illegal syntax: ' + self.input_json)

        return ret

    def __scan_null(self):
        if self.input_json[self.cursor:self.cursor + 4] == 'null':
            self.__update_cur()
            self.__update_cur()
            self.__update_cur()
            self.__update_cur()
            return None
        else:
            raise HexsonParserException('Illegal syntax: ' + self.input_json)

    def __scan_bool(self):
        if self.input_json[self.cursor:self.cursor + 4] == 'true':
            self.__update_cur()
            self.__update_cur()
            self.__update_cur()
            self.__update_cur()
            return True
        elif self.input_json[self.cursor:self.cursor + 5] == 'false':
            self.__update_cur()
            self.__update_cur()
            self.__update_cur()
            self.__update_cur()
            self.__update_cur()
            return False
        else:
            raise HexsonParserException('Illegal syntax: ' + self.input_json)

    def __scan_value(self, is_root=True):
        ret = None
        got_res = False

        while self.cursor < self.input_len:
            if self.__cur() == ' ' or self.__cur() == '\t' or self.__cur() == '\r' or self.__cur() == '\n':
                # Skip blank.
                self.__update_cur()
                continue
            elif self.__cur() == '{':
                # Entry for object.
                ret = self.__scan_obj()
                got_res = True
                break
            elif self.__cur() == '[':
                # Entry for array.
                ret = self.__scan_array()
                got_res = True
                break
            elif self.__cur() == '"':
                # Entry for bytes.
                if not self.utf_8_string:
                    ret = self.__scan_bytes()
                else:
                    ret = self.__scan_string()
                if ret:
                    got_res = True
                break
            elif ord(self.__cur()) >= 48 and ord(self.__cur()) <= 59 or self.__cur() == '-' or self.__cur() == '+':
                # Entry for number.
                ret = self.__scan_number()
                got_res = True
                break
            elif self.__cur() == 'n':
                # Entry for null.
                self.__scan_null()
                got_res = True
                break
            elif self.__cur() == 't' or self.__cur() == 'f':
                # Entry for true or false.
                ret = self.__scan_bool()
                got_res = True
                break
            elif (self.__cur() == ']' or self.__cur() == '}') and not is_root:
                # Hit outer exity.
                return ret
            else:
                raise HexsonParserException('Illegal syntax: ' + self.input_json)

        if not got_res:
            raise HexsonParserException('Illegal syntax: ' + self.input_json)

        return ret

    def parse_from_json(self, utf_8_string=False):
        self.utf_8_string = utf_8_string
        return self.__scan_value()
