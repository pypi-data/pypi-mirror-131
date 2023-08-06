from struct import Struct
from typing import Union
import random
import aiohttp.http_websocket

PACK_LEN1 = Struct("!BB").pack
PACK_LEN2 = Struct("!BBH").pack
PACK_LEN3 = Struct("!BBQ").pack
OPCODE_TEXT = 1

def encode_progress_frame(org_msg: Union[bytes, str]) -> bytes:
    msg = org_msg.encode("utf-8") if isinstance(org_msg, str) else org_msg
    msg_length = len(msg)
    rsv = 0
    mask_bit = 0x80
    opcode = OPCODE_TEXT
    if msg_length < 126:
        header = PACK_LEN1(0x80 | rsv | opcode, msg_length | mask_bit)
    elif msg_length < (1 << 16):
        header = PACK_LEN2(0x80 | rsv | opcode, 126 | mask_bit, msg_length)
    else:
        header = PACK_LEN3(0x80 | rsv | opcode, 127 | mask_bit, msg_length)

    mask = random.randrange(0, 0xFFFFFFFF)
    mask_bytes = mask.to_bytes(4, "big")
    msg_bytearray = bytearray(msg)
    aiohttp.http_websocket._websocket_mask(mask_bytes, msg_bytearray)
    return header + mask_bytes + msg_bytearray
