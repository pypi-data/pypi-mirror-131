import hashlib
import re
import json

# a class for encapsulating JSON data frames of arbitrary type for transmission over serial communication
class DataEncapsulator:
    def __init__(self, logger=None):
        self.logger = logger

        self.data_payload_type_size = 24
        self.data_checksum_size = 32
        self.data_payload_length_size = 8
        self.data_header_size = self.data_payload_type_size + self.data_checksum_size + self.data_payload_length_size
        self.data_marker = "P1MSGDATA"

        self.buffer = ''

    @staticmethod
    def ensure_var_is_string(var):
        if isinstance(var, str):
            return var
        elif isinstance(var, bytes):
            return var.decode("utf-8")
        else:
            return str(var)

    def add_to_buffer(self, new_data):
        new_data = self.ensure_var_is_string(new_data)

        self.buffer += new_data

    def get_data_code_for_type(self, type_str):
        type_str = self.ensure_var_is_string(type_str)
        adjusted_type_str = f'{type_str: <{self.data_payload_type_size}}'  # expand to size if short
        adjusted_type_str = adjusted_type_str[:self.data_payload_type_size]  # limit to size if too long
        return adjusted_type_str

    def create_data_frame(self, payload_type, payload_str):
        # a simple encapsulation scheme that prefixes the payload with a frame registration marker
        # and a fixed size header (containing payload length 6 digits and payload MD5 checksum)

        payload_str = self.ensure_var_is_string(payload_str)
        payload_type = self.ensure_var_is_string(payload_type)

        checksum = hashlib.md5(payload_str.encode("utf-8")).hexdigest()
        payload_len = len(payload_str)
        marker = self.data_marker
        payload_type = self.get_data_code_for_type(payload_type)
        return f"{marker}{payload_type}{payload_len:0{self.data_payload_length_size}}{checksum}{payload_str}"

    def get_next_frame_data(self):
        # print(f'buffer : {self.buffer}')
        s = re.search(self.data_marker, self.buffer)
        if not s: return  # frame registration marker not found yet
        start = s.end()
        buf_len = len(self.buffer)
        if buf_len - start <= self.data_header_size: return  # not enough data for header

        try:
            payload_type = self.buffer[start: start + self.data_payload_type_size].strip()
            start += self.data_payload_type_size
            payload_len = int(self.buffer[start: start + self.data_payload_length_size])
            start += self.data_payload_length_size
            checksum = self.buffer[start: start + self.data_checksum_size]
            start += self.data_checksum_size

            if start + payload_len > buf_len: return  # not enough data for payload

            payload_str = self.buffer[start: start + payload_len]
            test_checksum = hashlib.md5(payload_str.encode("utf-8")).hexdigest()

            if start + payload_len >= buf_len:
                self.buffer = ''
            else:
                self.buffer = self.buffer[start + payload_len:]

            if test_checksum == checksum:
                return {"type": payload_type, "data": json.loads(payload_str)}

        except Exception as e:
            print(f'encountered error in get_next_frame parsing: {e}')
            # chop buf at current start to avoid cycling on bad data
            self.buffer = self.buffer[start:]

        return None
