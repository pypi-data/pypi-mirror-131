
def decode_dec_to_hex(a=''):


    if int(a) < 0:
        b = 256 + int(a)
    else:
        b = int(a)

    message_hex = hex(b)
    message_hex_wo_head = message_hex.split('x')[1]
    message_hex_padded = message_hex_wo_head.zfill(2)

    print(b)
    print(type(b))
    print(message_hex_padded)
    print(type(message_hex_padded))
    print('hier')
    return message_hex_padded

