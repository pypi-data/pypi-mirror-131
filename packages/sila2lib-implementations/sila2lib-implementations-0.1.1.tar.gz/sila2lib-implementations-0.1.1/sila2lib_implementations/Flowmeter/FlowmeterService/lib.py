from struct import *  # used to code binary protocol
from Errorlibrary import decode_process_response
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


def decode_response_read(protocol='binary', message_str: str = '', type_answer=''):
    if protocol == 'binary':
        # The decode workflow for the binary protocol
        try:
            query = unpack_from('bbbbbbbbbbb', message_str)

            print(query)

            dle, stx, message_sequence, node, length, answer_command, process_query, parameter_query, message, dle2, etx = \
                str(query).split(',')

            print(
                f'message_sequence: {message_sequence} \nnode: {node} \nlength: {length}, \ncommand: {answer_command} '
                f'\nprocess_query: {process_query}\nparameter_query: {parameter_query} \nmessage: {message} \n', )


            response_decoded = {
                'message_sequence_nr': int(message_sequence),
                'node': int(node),
                'length': int(length),
                'answer_command': str(answer_command),
                'process_query': str(process_query),
                'parameter_query': str(parameter_query),
                'message': str(message)
            }
        except :
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
            split_at_1 = 1
            split_at_2 = 11
            header, message_hex = message_str[split_at_1:split_at_2], message_str[split_at_2:]
            length, node, answer_command, process_query, parameter_query = [header[i:i + 2] for i in range(0, len(header), 2)]
            message_dec = int(message_hex, 16)
            print(header, message_hex)
            print([header[i:i + 2] for i in range(0, len(header), 2)])
            print(f'length: {length} \nnode: {node} \nanswer_command: {answer_command} \nprocess_query: {process_query}'
                  f'\nparameter_query: {parameter_query} \nmessage_hex: {message_hex} \nmessage_dec: {message_dec}')
            int_length= int(length,16)
            response_decoded = {
                'length': int_length,
                'node': int(node),
                'answer_command': str(answer_command),
                'process_query': str(process_query),
                'parameter_query': str(parameter_query),
                'message_hex': str(message_hex),
                'message': str(message_dec)
            }
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
