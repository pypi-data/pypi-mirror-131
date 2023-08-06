from struct import *  # used to code binary protocol
def decode_response_write(protocol='binary', message_str: str = '', type_answer=''):

    if protocol == 'binary':
        # The decode workflow for the binary protocol

            query = unpack_from('BbbbbbbbBb', message_str)
            print(query)

            dle, stx, message_sequence, node, length, answer_command, process, parameter, dle2, etx \
                = str(query).split(',')

            print(f'message_sequence_nr: {message_sequence} \nnode: {node} \nlength: {length} '
                  f'\nanswer_command: {answer_command} \nparameter: {process} '
                  f'\nparameter: {parameter}')

            hex_process = hex(int(process))
            hex_process_wo_head = hex_process.split('x')[1]
            hex_process_padded = hex_process_wo_head.zfill(2)
            message = decode_process_response(process_query=hex_process_padded, type_answer=type_answer)
            response_decoded = {
                'message_sequence_nr': int(message_sequence),
                'node': int(node),
                'length': int(length),
                'answer_command': int(answer_command),
                'message': str(message),
                'index': str(parameter),
            }

            return response_decoded

    elif protocol == 'ascii':
        # The decode protocol for the ascii protocol
            split_at_1 = 1
            split_at_2 = 11
            header, message_hex = message_str[split_at_1:split_at_2], message_str[split_at_2:]
            length, node, answer_command, status, index = [header[i:i + 2] for i in
                                                           range(0, len(header), 2)]

            message = decode_process_response(process_query=status)

            response_decoded = {
                'length': int(length),
                'node': int(node),
                'answer_command': str(answer_command),
                'message': str(message),
                'index': str(index)
            }



            return response_decoded

def decode_response_read(protocol='binary', message_str: str = '', type_answer='', message_length='', message_type=''):
    if protocol == 'binary':
        # The decode workflow for the binary protocol
        try:
            if message_type == 'value':
                """
                message_sequence= None
                node= None
                length=None
                answer_command=None
                process_query =None
                parameter_query=None
                message_hex=None
                message_dec=None
                message_text=None
                """


                if message_length == 11:
                    query = unpack_from('bbbbbbbbbbb', message_str)

                    print(query)

                    dle, stx, message_sequence, node, length, answer_command, process_query, parameter_query, message1,\
                    dle2, etx = str(query).split(',')
                    message1_hex = decode_dec_to_hex(a=message1)


                    message_hex = int(f'{(message1_hex)}')
                    message_dec = int(str(message_hex), 16)
                    message_text = str(message1)

                    """
                    response = {
                        'message_sequence':(message_sequence),
                        'node':(node),
                        'length': (length),
                        'answer_command':(answer_command),
                        'process_query':(process_query),
                        'parameter_query':(parameter_query),
                        'message_hex': (message_hex),
                        'message_dec':(message_dec),
                        'message_text': (message_text)
                    }
                    return response
                    """
                    print(
                        f'message_sequence: {message_sequence} \nnode: {node} \nlength: {length}, \ncommand: {answer_command} '
                        f'\nprocess_query: {process_query}\nparameter_query: {parameter_query} '
                        f'\nmessage_hex: {message_hex}\nmessage_dec: {message_dec}\nmessage_text: {message_text}\n', )

                    response_decoded = {
                        'message_sequence_nr': int(message_sequence),
                        'node': int(node),
                        'length3': int(length),
                        'answer_command': str(answer_command),
                        'process_query': str(process_query),
                        'parameter_query': str(parameter_query),
                        'message_hex': str(message_hex),
                        'message_dec': str(message_dec),
                        'message_text': str(message_text)
                    }
                    return response_decoded

                elif message_length == 12:
                    query = unpack_from('bbbbbbbbbbbb', message_str)

                    print(query)

                    dle, stx, message_sequence, node, length, answer_command, process_query, parameter_query, message1,\
                    message2, dle2, etx = str(query).split(',')

                    message1_hex = decode_dec_to_hex(a=message1)
                    message2_hex = decode_dec_to_hex(a=message2)
                    message_hex = (f'{(message1_hex)}{(message2_hex)}')
                    message_dec = int(str(message_hex), 16)
                    message_text_a = pack('bb', int(message1), int(message2))
                    message_text = str({message_text_a})

                    """
                    response = {
                        'message_sequence':(message_sequence),
                        'node':(node),
                        'length': (length),
                        'answer_command':(answer_command),
                        'process_query':(process_query),
                        'parameter_query':(parameter_query),
                        'message_hex': (message_hex),
                        'message_dec':(message_dec),
                        'message_text': (message_text)
                    }
                    return response
                    """
                    print(
                        f'message_sequence: {message_sequence} \nnode: {node} \nlength: {length}, \ncommand: {answer_command} '
                        f'\nprocess_query: {process_query}\nparameter_query: {parameter_query} '
                        f'\nmessage_hex: {message_hex}\nmessage_dec: {message_dec}\nmessage_text: {message_text}\n', )

                    response_decoded = {
                        'message_sequence_nr': int(message_sequence),
                        'node': int(node),
                        'length3': int(length),
                        'answer_command': str(answer_command),
                        'process_query': str(process_query),
                        'parameter_query': str(parameter_query),
                        'message_hex': str(message_hex),
                        'message_dec': str(message_dec),
                        'message_text': str(message_text)
                    }
                    return response_decoded

                elif message_length == 14:


                    query = unpack_from('bbbbbbbbbbbbbb', message_str)

                    print(query)

                    dle, stx, message_sequence, node, length, answer_command, process_query, parameter_query, \
                    message1, message2, message3, message4, dle2, etx = \
                        str(query).split(',')

                    message1_hex = decode_dec_to_hex(a=message1)
                    message2_hex = decode_dec_to_hex(a=message2)
                    message3_hex = decode_dec_to_hex(a=message3)
                    message4_hex = decode_dec_to_hex(a=message4)

                    print(f'{message1_hex}{message2_hex}{message3_hex}{message4_hex}')
                    message_hex = f'{message1_hex}{message2_hex}{message3_hex}{message4_hex}'
                    message_dec = int(message_hex, 16)
                    message_text_a = pack('bbbb', int(message1), int(message2), int(message3), int(message4))
                    print('heeere2')
                    message_text = str({message_text_a})

                    """
                    response = {
                        'message_sequence':(message_sequence),
                        'node':(node),
                        'length': (length),
                        'answer_command':(answer_command),
                        'process_query':(process_query),
                        'parameter_query':(parameter_query),
                        'message_hex': (message_hex),
                        'message_dec':(message_dec),
                        'message_text': (message_text)
                    }
                    return response
                    """
                    print(
                        f'message_sequence: {message_sequence} \nnode: {node} \nlength: {length}, \ncommand: {answer_command} '
                        f'\nprocess_query: {process_query}\nparameter_query: {parameter_query} '
                        f'\nmessage_hex: {message_hex}\nmessage_dec: {message_dec}\nmessage_text: {message_text}\n', )

                    response_decoded = {
                        'message_sequence_nr': int(message_sequence),
                        'node': int(node),
                        'length3': int(length),
                        'answer_command': str(answer_command),
                        'process_query': str(process_query),
                        'parameter_query': str(parameter_query),
                        'message_hex': str(message_hex),
                        'message_dec': str(message_dec),
                        'message_text': str(message_text)
                    }
                    return response_decoded

                elif message_length == 17:
                    query = unpack_from('bbbbbbbbbbbbbbbbb', message_str)

                    print(query)

                    dle, stx, message_sequence, node, length, answer_command, process_query, parameter_query, \
                    message1, message2, message3, message4, message5, message6, message7, dle2, etx = \
                        str(query).split(',')

                    message1_hex = decode_dec_to_hex(a=message1)
                    message2_hex = decode_dec_to_hex(a=message2)
                    message3_hex = decode_dec_to_hex(a=message3)
                    message4_hex = decode_dec_to_hex(a=message4)
                    message5_hex = decode_dec_to_hex(a=message5)
                    message6_hex = decode_dec_to_hex(a=message6)
                    message7_hex = decode_dec_to_hex(a=message7)


                    message_hex = int(f'{(message1_hex)}{(message2_hex)}{(message3_hex)}{(message4_hex)}{(message5_hex)}'
                                      f'{(message6_hex)}{(message7_hex)}')
                    message_dec = int(str(message_hex), 16)
                    message_text_a = pack('bbbbbbb', int(message1), int(message2), int(message3), int(message4),
                                          int(message5), int(message6), int(message7))
                    message_text = str({message_text_a})

                    """
                    response = {
                        'message_sequence':(message_sequence),
                        'node':(node),
                        'length': (length),
                        'answer_command':(answer_command),
                        'process_query':(process_query),
                        'parameter_query':(parameter_query),
                        'message_hex': (message_hex),
                        'message_dec':(message_dec),
                        'message_text': (message_text)
                    }
                    return response
                    """
                    print(
                        f'message_sequence: {message_sequence} \nnode: {node} \nlength: {length}, \ncommand: {answer_command} '
                        f'\nprocess_query: {process_query}\nparameter_query: {parameter_query} '
                        f'\nmessage_hex: {message_hex}\nmessage_dec: {message_dec}\nmessage_text: {message_text}\n', )

                    response_decoded = {
                        'message_sequence_nr': int(message_sequence),
                        'node': int(node),
                        'length3': int(length),
                        'answer_command': str(answer_command),
                        'process_query': str(process_query),
                        'parameter_query': str(parameter_query),
                        'message_hex': str(message_hex),
                        'message_dec': str(message_dec),
                        'message_text': str(message_text)
                    }
                    return response_decoded

                elif message_length == 18:
                    query = unpack_from('bbbbbbbbbbbbbbbbbb', message_str)

                    print(query)

                    dle, stx, message_sequence, node, length, answer_command, process_query, parameter_query, message1, \
                    message2, message3, message4, message5, message6, message7, message8, dle2, etx = \
                        str(query).split(',')

                    message1_hex = decode_dec_to_hex(a=message1)
                    message2_hex = decode_dec_to_hex(a=message2)
                    message3_hex = decode_dec_to_hex(a=message3)
                    message4_hex = decode_dec_to_hex(a=message4)
                    message5_hex = decode_dec_to_hex(a=message5)
                    message6_hex = decode_dec_to_hex(a=message6)
                    message7_hex = decode_dec_to_hex(a=message7)
                    message8_hex = decode_dec_to_hex(a=message8)


                    message_hex = int(
                        f'{(message1_hex)}{(message2_hex)}{(message3_hex)}{(message4_hex)}{(message5_hex)}'
                        f'{(message6_hex)}{(message7_hex)}{(message8_hex)}')
                    message_dec = int(str(message_hex), 16)
                    message_text_a = pack('bbbbbbbb', int(message1), int(message2), int(message3), int(message4),
                                          int(message5), int(message6), int(message7), int(message8))
                    message_text = str({message_text_a})

                    """
                    response = {
                        'message_sequence':(message_sequence),
                        'node':(node),
                        'length': (length),
                        'answer_command':(answer_command),
                        'process_query':(process_query),
                        'parameter_query':(parameter_query),
                        'message_hex': (message_hex),
                        'message_dec':(message_dec),
                        'message_text': (message_text)
                    }
                    return response
                    """
                    print(
                        f'message_sequence: {message_sequence} \nnode: {node} \nlength: {length}, \ncommand: {answer_command} '
                        f'\nprocess_query: {process_query}\nparameter_query: {parameter_query} '
                        f'\nmessage_hex: {message_hex}\nmessage_dec: {message_dec}\nmessage_text: {message_text}\n', )

                    response_decoded = {
                        'message_sequence_nr': int(message_sequence),
                        'node': int(node),
                        'length3': int(length),
                        'answer_command': str(answer_command),
                        'process_query': str(process_query),
                        'parameter_query': str(parameter_query),
                        'message_hex': str(message_hex),
                        'message_dec': str(message_dec),
                        'message_text': str(message_text)
                    }
                    return response_decoded

                elif message_length == 19:
                    query = unpack_from('bbbbbbbbbbbbbbbbbbb', message_str)

                    print(query)

                    dle, stx, message_sequence, node, length, answer_command, process_query, parameter_query, message1, \
                    message2, message3, message4, message5, message6, message7, message8, message9, dle2, etx = \
                        str(query).split(',')

                    message1_hex = decode_dec_to_hex(a=message1)
                    message2_hex = decode_dec_to_hex(a=message2)
                    message3_hex = decode_dec_to_hex(a=message3)
                    message4_hex = decode_dec_to_hex(a=message4)
                    message5_hex = decode_dec_to_hex(a=message5)
                    message6_hex = decode_dec_to_hex(a=message6)
                    message7_hex = decode_dec_to_hex(a=message7)
                    message8_hex = decode_dec_to_hex(a=message8)
                    message9_hex = decode_dec_to_hex(a=message9)

                    message_hex = int(
                        f'{(message1_hex)}{(message2_hex)}{(message3_hex)}{(message4_hex)}{(message5_hex)}'
                        f'{(message6_hex)}{(message7_hex)}{(message8_hex)}{(message9_hex)}')
                    message_dec = int(str(message_hex), 16)

                    message_text_a = pack('bbbbbbbb', int(message2), int(message3), int(message4),
                                          int(message5), int(message6), int(message7), int(message8), int(message9))

                    message_text = str({message_text_a})

                    """
                    response = {
                        'message_sequence':(message_sequence),
                        'node':(node),
                        'length': (length),
                        'answer_command':(answer_command),
                        'process_query':(process_query),
                        'parameter_query':(parameter_query),
                        'message_hex': (message_hex),
                        'message_dec':(message_dec),
                        'message_text': (message_text)
                    }
                    return response
                    """
                    print(
                        f'message_sequence: {message_sequence} \nnode: {node} \nlength: {length}, \ncommand: {answer_command} '
                        f'\nprocess_query: {process_query}\nparameter_query: {parameter_query} '
                        f'\nmessage_hex: {message_hex}\nmessage_dec: {message_dec}\nmessage_text: {message_text}\n', )

                    response_decoded = {
                        'message_sequence_nr': int(message_sequence),
                        'node': int(node),
                        'length3': int(length),
                        'answer_command': str(answer_command),
                        'process_query': str(process_query),
                        'parameter_query': str(parameter_query),
                        'message_hex': str(message_hex),
                        'message_dec': str(message_dec),
                        'message_text': str(message_text)
                    }
                    return response_decoded

                elif message_length == 21:
                    query = unpack_from('bbbbbbbbbbbbbbbbbbbbb', message_str)

                    print(query)

                    dle, stx, message_sequence, node, length, answer_command, process_query, parameter_query, message1, \
                    message2, message3, message4, message5, message6, message7, message8, message9, message10, message11, \
                    dle2, etx = \
                        str(query).split(',')

                    message1_hex = decode_dec_to_hex(a=message1)
                    message2_hex = decode_dec_to_hex(a=message2)
                    message3_hex = decode_dec_to_hex(a=message3)
                    message4_hex = decode_dec_to_hex(a=message4)
                    message5_hex = decode_dec_to_hex(a=message5)
                    message6_hex = decode_dec_to_hex(a=message6)
                    message7_hex = decode_dec_to_hex(a=message7)
                    message8_hex = decode_dec_to_hex(a=message8)
                    message9_hex = decode_dec_to_hex(a=message9)
                    message10_hex = decode_dec_to_hex(a=message10)
                    message11_hex = decode_dec_to_hex(a=message11)


                    message_hex = int(
                        f'{(message1_hex)}{(message2_hex)}{(message3_hex)}{(message4_hex)}{(message5_hex)}'
                        f'{(message6_hex)}{(message7_hex)}{(message8_hex)}{(message9_hex)}{(message10_hex)}{(message11_hex)}')
                    message_dec = int(str(message_hex), 16)

                    message_text_a = pack('bbbbbbbbbbb', int(message1),int(message2), int(message3), int(message4),
                                          int(message5), int(message6), int(message7), int(message8), int(message9),
                                          int(message9), int(message10), int(message11))
                    message_text = str({message_text_a})

                    """
                    response = {
                        'message_sequence':(message_sequence),
                        'node':(node),
                        'length': (length),
                        'answer_command':(answer_command),
                        'process_query':(process_query),
                        'parameter_query':(parameter_query),
                        'message_hex': (message_hex),
                        'message_dec':(message_dec),
                        'message_text': (message_text)
                    }
                    return response
                    """
                    print(
                        f'message_sequence: {message_sequence} \nnode: {node} \nlength: {length}, \ncommand: {answer_command} '
                        f'\nprocess_query: {process_query}\nparameter_query: {parameter_query} '
                        f'\nmessage_hex: {message_hex}\nmessage_dec: {message_dec}\nmessage_text: {message_text}\n', )

                    response_decoded = {
                        'message_sequence_nr': int(message_sequence),
                        'node': int(node),
                        'length3': int(length),
                        'answer_command': str(answer_command),
                        'process_query': str(process_query),
                        'parameter_query': str(parameter_query),
                        'message_hex': str(message_hex),
                        'message_dec': str(message_dec),
                        'message_text': str(message_text)
                    }
                    return response_decoded

                elif message_length == 22:
                    query = unpack_from('bbbbbbbbbbbbbbbbbbbbbb', message_str)

                    print(query)

                    dle, stx, message_sequence, node, length, answer_command, process_query, parameter_query, message1, \
                    message2, message3, message4, message5, message6, message7, message8, message9, message10, message11, \
                    message12, dle2, etx = \
                        str(query).split(',')

                    message1_hex = decode_dec_to_hex(a=message1)
                    message2_hex = decode_dec_to_hex(a=message2)
                    message3_hex = decode_dec_to_hex(a=message3)
                    message4_hex = decode_dec_to_hex(a=message4)
                    message5_hex = decode_dec_to_hex(a=message5)
                    message6_hex = decode_dec_to_hex(a=message6)
                    message7_hex = decode_dec_to_hex(a=message7)
                    message8_hex = decode_dec_to_hex(a=message8)
                    message9_hex = decode_dec_to_hex(a=message9)
                    message10_hex = decode_dec_to_hex(a=message10)
                    message11_hex = decode_dec_to_hex(a=message11)
                    message12_hex = decode_dec_to_hex(a=message12)


                    message_hex = int(
                        f'{(message1_hex)}{(message2_hex)}{(message3_hex)}{(message4_hex)}{(message5_hex)}'
                        f'{(message6_hex)}{(message7_hex)}{(message8_hex)}{(message9_hex)}{(message10_hex)}'
                        f'{(message11_hex)}{(message12_hex)}')
                    message_dec = int(str(message_hex), 16)
                    message_text_a = pack('bbbbbbbbbbb', int(message2), int(message3), int(message4),
                                          int(message5), int(message6), int(message7), int(message8), int(message9),
                                          int(message10), int(message11), int(message12))
                    message_text = str({message_text_a})

                    """
                    response = {
                        'message_sequence':(message_sequence),
                        'node':(node),
                        'length': (length),
                        'answer_command':(answer_command),
                        'process_query':(process_query),
                        'parameter_query':(parameter_query),
                        'message_hex': (message_hex),
                        'message_dec':(message_dec),
                        'message_text': (message_text)
                    }
                    return response
                    """
                    print(
                        f'message_sequence: {message_sequence} \nnode: {node} \nlength: {length}, \ncommand: {answer_command} '
                        f'\nprocess_query: {process_query}\nparameter_query: {parameter_query} '
                        f'\nmessage_hex: {message_hex}\nmessage_dec: {message_dec}\nmessage_text: {message_text}\n', )

                    response_decoded = {
                        'message_sequence_nr': int(message_sequence),
                        'node': int(node),
                        'length3': int(length),
                        'answer_command': str(answer_command),
                        'process_query': str(process_query),
                        'parameter_query': str(parameter_query),
                        'message_hex': str(message_hex),
                        'message_dec': str(message_dec),
                        'message_text': str(message_text)
                    }
                    return response_decoded

                elif message_length ==0:
                    error = 1010101010101010101010101010101
                    response = {
                        'message_sequence_nr': int(error),
                        'node': int(error),
                        'length3': int(error),
                        'answer_command': str(error),
                        'process_query': str(error),
                        'parameter_query': str(error),
                        'message_hex': str(error),
                        'message_dec': str(error),
                        'message_text': str('error')
                    }
                    return response

            elif message_type == 'text':

                if message_length == 14:
                    query = unpack_from('bbbbbbbbbbbbbb', message_str)

                    print(query)

                    dle, stx, message_sequence, node, length, answer_command, process_query, parameter_query, \
                    response_length, message2, message3, message4, dle2, etx = \
                        str(query).split(',')

                    message_text_a = pack('bbb', int(message2), int(message3), int(message4))
                    message_text = str({message_text_a})

                    print(
                        f'message_sequence: {message_sequence} \nnode: {node} \nlength: {length}, \ncommand: {answer_command} '
                        f'\nprocess_query: {process_query}\nparameter_query: {parameter_query}\nmessage_text: {message_text}\n')

                    response_decoded = {
                        'message_sequence_nr': int(message_sequence),
                        'node': int(node),
                        'length': int(length),
                        'answer_command': str(answer_command),
                        'process_query': str(process_query),
                        'parameter_query': str(parameter_query),
                        'message_text': str(message_text)
                    }
                    return response_decoded

                elif message_length == 17:
                    query = unpack_from('bbbbbbbbbbbbbbbbb', message_str)

                    print(query)

                    dle, stx, message_sequence, node, length, answer_command, process_query, parameter_query, response_length, \
                    message2, message3, message4, message5, message6, message7, dle2, etx = \
                        str(query).split(',')

                    message_text_a = pack('bbbbbb', int(message2), int(message3), int(message4),
                                          int(message5), int(message6), int(message7))
                    message_text = str({message_text_a})

                    print(
                        f'message_sequence: {message_sequence} \nnode: {node} \nlength: {length}, \ncommand: {answer_command} '
                        f'\nprocess_query: {process_query}\nparameter_query: {parameter_query}\nmessage_text: {message_text}\n')

                    response_decoded = {
                        'message_sequence_nr': int(message_sequence),
                        'node': int(node),
                        'length': int(length),
                        'answer_command': str(answer_command),
                        'process_query': str(process_query),
                        'parameter_query': str(parameter_query),
                        'message_text': str(message_text)
                    }
                    return response_decoded

                elif message_length == 18:
                    query = unpack_from('bbbbbbbbbbbbbbbbbb', message_str)

                    print(query)

                    dle, stx, message_sequence, node, length, answer_command, process_query, parameter_query, response_length, \
                    message2, message3, message4, message5, message6, message7, message8, dle2, etx = \
                        str(query).split(',')

                    message_text_a = pack('bbbbbbb', int(message2), int(message3), int(message4),
                                          int(message5), int(message6), int(message7), int(message8))

                    message_text = str(message_text_a)

                    print(
                        f'message_sequence: {message_sequence} \nnode: {node} \nlength: {length}, \ncommand: {answer_command} '
                        f'\nprocess_query: {process_query}\nparameter_query: {parameter_query}\nmessage_text: {message_text}\n')

                    response_decoded = {
                        'message_sequence_nr': int(message_sequence),
                        'node': int(node),
                        'length': int(length),
                        'answer_command': str(answer_command),
                        'process_query': str(process_query),
                        'parameter_query': str(parameter_query),
                        'message_text': str(message_text)
                    }
                    return response_decoded

                elif message_length == 19:
                    query = unpack_from('bbbbbbbbbbbbbbbbbbb', message_str)

                    print(query)

                    dle, stx, message_sequence, node, length, answer_command, process_query, parameter_query, response_length, \
                    message2, message3, message4, message5, message6, message7, message8, message9, dle2, etx = \
                        str(query).split(',')

                    message_text_a = pack('bbbbbbbb', int(message2), int(message3), int(message4),
                                          int(message5), int(message6), int(message7), int(message8), int(message9))

                    message_text = str({message_text_a})
                    print(
                        f'message_sequence: {message_sequence} \nnode: {node} \nlength: {length}, \ncommand: {answer_command} '
                        f'\nprocess_query: {process_query}\nparameter_query: {parameter_query}\nmessage_text: {message_text}\n')

                    response_decoded = {
                        'message_sequence_nr': int(message_sequence),
                        'node': int(node),
                        'length': int(length),
                        'answer_command': str(answer_command),
                        'process_query': str(process_query),
                        'parameter_query': str(parameter_query),
                        'message_text': str(message_text)
                    }
                    return response_decoded



                elif message_length == 21:
                    query = unpack_from('bbbbbbbbbbbbbbbbbbbbb', message_str)

                    print(query)

                    dle, stx, message_sequence, node, length, answer_command, process_query, parameter_query, lenght_message1, \
                    message2, message3, message4, message5, message6, message7, message8, message9, message10, message11, \
                    dle2, etx = \
                    str(query).split(',')

                    message_text_a = pack('bbbbbbbbbb', int(message2), int(message3), int(message4),
                                          int(message5), int(message6), int(message7),int(message8), int(message9),
                                          int(message10), int(message11))
                    message_text = str({message_text_a})
                    print(
                        f'message_sequence: {message_sequence} \nnode: {node} \nlength: {length}, \ncommand: {answer_command} '
                        f'\nprocess_query: {process_query}\nparameter_query: {parameter_query}\nmessage_text: {message_text}\n')

                    response_decoded = {
                        'message_sequence_nr': int(message_sequence),
                        'node': int(node),
                        'length': int(length),
                        'answer_command': str(answer_command),
                        'process_query': str(process_query),
                        'parameter_query': str(parameter_query),
                        'message_text': str(message_text)
                    }
                    return response_decoded

                elif message_length == 22:
                    query = unpack_from('bbbbbbbbbbbbbbbbbbbbbb', message_str)

                    print(query)

                    dle, stx, message_sequence, node, length, answer_command, process_query, parameter_query, response_length, \
                    message2, message3, message4, message5, message6, message7, message8, message9, message10, message11, \
                    message12, dle2, etx = \
                        str(query).split(',')

                    message_text_a = pack('bbbbbbbbbbb', int(message2), int(message3), int(message4),
                                          int(message5), int(message6), int(message7), int(message8), int(message9),
                                          int(message10), int(message11), int(message12))
                    message_text = str({message_text_a})

                    print(
                        f'message_sequence: {message_sequence} \nnode: {node} \nlength: {length}, \ncommand: {answer_command} '
                        f'\nprocess_query: {process_query}\nparameter_query: {parameter_query}\nmessage_text: {message_text}\n')

                    response_decoded = {
                        'message_sequence_nr': int(message_sequence),
                        'node': int(node),
                        'length': int(length),
                        'answer_command': str(answer_command),
                        'process_query': str(process_query),
                        'parameter_query': str(parameter_query),
                        'message_text': str(message_text)
                    }
                    return response_decoded

                elif message_length ==0:
                    error = 1010101010101010101010101010101
                    response = {
                        'message_sequence_nr': int(error),
                        'node': int(error),
                        'length3': int(error),
                        'answer_command': str(error),
                        'process_query': str(error),
                        'parameter_query': str(error),
                        'message_text': str('error')
                    }
                    return response

        except  :
        #struct.error:
            query = unpack_from('BbbbbbbbBb', message_str)
            print(query)

            dle, stx, message_sequence, node, length, answer_command, process, index, dle2, etx \
                = str(query).split(',')

            print(f'message_sequence_nr: {message_sequence} \nnode: {node} \nlength: {length} '
                  f'\nanswer_command: {answer_command} \nprocess: {process} '
                  f'\nindex: {index}')
            hex_process = hex(int(process))
            hex_process_wo_head = hex_process.split('x')[1]
            hex_process_padded = hex_process_wo_head.zfill(2)
            message = decode_process_response(process_query=hex_process_padded, type_answer=type_answer)
            #message = 99999999999999999999999
            response_decoded = {
                'message_sequence_nr': int(message_sequence),
                'node': int(node),
                'length': int(length),
                'answer_command': int(answer_command),
                'message': str(message),
                'index': str(index),

            }
        #except ValueError :0104

            return response_decoded

    elif protocol == 'ascii':
        # The decode protocol for the ascii protocol
        try:
            if message_type =='text':
                split_at_1 = 1
                split_at_2 = 13
                header, message_hex = message_str[split_at_1:split_at_2], message_str[split_at_2:]
                length, node, answer_command, process_query, parameter_query, response_length = [header[i:i + 2] for i in
                                                                                range(0, len(header), 2)]
                byte_array = bytearray.fromhex(message_hex)
                print(byte_array)
                message_text = byte_array.decode()
                message_dec = int(message_hex, 16)

                print(header, message_hex)
                print([header[i:i + 2] for i in range(0, len(header), 2)])
                print(
                    f'length: {length} \nnode: {node} \nanswer_command: {answer_command} \nprocess_query: {process_query}'
                    f'\nparameter_query: {parameter_query} \nresponse_length: {response_length}  '
                    f'\nmessage_hex: {message_hex} \nmessage_text: {message_text}')

                int_length = int(length, 16)
                response_decoded = {
                    'length': int_length,
                    'node': int(node),
                    'answer_command': str(answer_command),
                    'process_query': str(process_query),
                    'parameter_query': str(parameter_query),
                    'message_hex': str(message_hex),
                    'message_dec': str(message_dec),
                    'message_text': str(message_text)
                }
                return response_decoded

            elif message_type =='value':
                split_at_1 = 1
                split_at_2 = 11
                header, message_hex = message_str[split_at_1:split_at_2], message_str[split_at_2:]
                length, node, answer_command, process_query, parameter_query = [header[i:i + 2] for i in
                                                                                range(0, len(header), 2)]
                message_dec = int(message_hex, 16)
                print(header, message_hex)
                print([header[i:i + 2] for i in range(0, len(header), 2)])
                print(
                    f'length: {length} \nnode: {node} \nanswer_command: {answer_command} \nprocess_query: {process_query}'
                    f'\nparameter_query: {parameter_query} \nmessage_hex: {message_hex} \nmessage_dec: {message_dec}')
                int_length = int(length, 16)
                response_decoded = {
                    'length': int_length,
                    'node': int(node),
                    'answer_command': str(answer_command),
                    'process_query': str(process_query),
                    'parameter_query': str(parameter_query),
                    'message_hex': str(message_hex),
                    'message_dec': str(message_dec)
                }
                return response_decoded


        except:
            split_at_1 = 1
            split_at_2 = 11
            header= message_str[split_at_1:split_at_2]
            length, node, answer_command, process_query, parameter_query = [header[i:i + 2] for i in
                                                                            range(0, len(header), 2)]


            print(header)
            print([header[i:i + 2] for i in range(0, len(header), 2)])
            print(f'length: {length} \nnode: {node} \nanswer_command: {answer_command} \nprocess: {process_query}'
                  f'\nparameter: {parameter_query}')

            message = decode_process_response(process_query=process_query, type_answer=type_answer)
            #message = 999999999999999999999999
            response_decoded = {
                'length': int(length),
                'node': int(node),
                'answer_command': str(answer_command),
                'process': str(process_query),
                'parameter': str(parameter_query),
                'message':str(message)
            }
            return response_decoded

#Secondary libraries

def decode_dec_to_hex(a=''):


    if int(a) < 0:
        b = 256 + int(a)
    else:
        b = int(a)

    message_hex = hex(b)
    message_hex_wo_head = message_hex.split('x')[1]
    message_hex_padded = message_hex_wo_head.zfill(2)

    return message_hex_padded

def decode_dec_to_binary(a=''):

    if a<127:
        b=a
    else:
        b=a-256
    return b



def decode_process_response(process_query='', type_answer=''):
    if isinstance(type_answer, str):
        answers = {
            str('00'): '00 No_error',
            str('01'): '01 Process claimed',
            str('02'): '02 Command error',
            str('03'): '03 Process error',
            str('04'): '04 Parameter error',
            str('05'): '05 Parameter type error',
            str('06'): '06 Parameter value error',
            str('07'): '07 Network not active',
            str('08'): '08 Time-out start character',
            str('09'): '09 Time-out serial line',
            str('0A'): '0A Hardware memory error',
            str('0B'): '0B Node number error',
            str('0C'): '0C General communication error 0D Read only parameter',
            str('0D'): '0D Read only parameter',
            str('0E'): '0E Error PC-communication',
            str('0F'): '0F No RS232 connection',
            str('10'): '10 PC out of memory',
            str('11'): '11 Write only parameter',
            str('12'): '12 System configuration unknown',
            str('13'): '13 No free node address',
            str('14'): '14 Wrong interface type',
            str('15'): '15 Error serial port connection',
            str('16'): '16 Error opening communication',
            str('17'): '17 Communication error',
            str('18'): '18 Error interface bus master',
            str('19'): '19 Timeout answer',
            str('1A'): '1A No start character',
            str('1B'): '1B Error first digit',
            str('1C'): '1C Buffer overflow in host',
            str('1D'): '1D Buffer overflow',
            str('1E'): '1E No answer found',
            str('1F'): '1F Error closing communication',
            str('20'): '20 Synchronisation error',
            str('21'): '21 Send error',
            str('22'): '22 Protocol error',
            str('23'): '23 Buffer overflow in module',
        }
        message = answers[process_query]
        return message
    else:
        response = {
            'message': int(9999999999999),
            'message_dec': float(9999999999999),
            'message_hex': int(999999999)
        }

        return response

