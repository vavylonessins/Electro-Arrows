# из байт в число
def btoi(bytes: bytes, signed: bool = False) -> int:
    result = int.from_bytes(bytes, 'little', signed=signed)
    return result


# из числа в байты
def itob(value: int, length: int, signed: bool = False) -> bytes:
    result = value.to_bytes(length, 'little', signed=signed)
    return result

def chunks(lst, n):
    ret = []
    for i in range(0, len(lst), n):
        ret.append(lst[i:i + n])
    return ret.copy()
