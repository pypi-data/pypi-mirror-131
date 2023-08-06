from struct import *  # used to code binary protocol
def decode_response_write(protocol='binary', message_str: str = ''):

    if protocol == 'binary':
        # The decode workflow for the binary protocol

        try:
            query = unpack_from('BbbbbbbbbBb', message_str)

            print(query)

            dle, stx, message_sequence, node, length, answer_command, message, parameter_query, message, index, dle2, etx \
                = str(query).split(',')

            print(f'message_sequence_nr: {message_sequence} \nnode: {node} \nlength: {length} '
                  f'\nanswer_command: {answer_command} \nmessage: {message} \nindex_send_message: {index}')

            response_decoded = {
                'message_sequence_nr': int(message_sequence),
                'node': int(node),
                'length': int(length),
                'answer_command': int(answer_command),
                'message': str(message),
                'index_send_message': str(index),
            }
        except:
            query = unpack_from('BbbbbbbbBb', message_str)
            print(query)

            dle, stx, message_sequence, node, length, answer_command, process, parameter, dle2, etx \
                = str(query).split(',')

            print(f'message_sequence_nr: {message_sequence} \nnode: {node} \nlength: {length} '
                  f'\nanswer_command: {answer_command} \nparameter: {process} '
                  f'\nparameter: {parameter}')

            response_decoded = {
                'message_sequence_nr': int(message_sequence),
                'node': int(node),
                'length': int(length),
                'answer_command': int(answer_command),
                'process': str(process),
                'parameter': str(parameter),
            }

        return response_decoded

    elif protocol == 'ascii':
        # The decode protocol for the ascii protocol
            split_at_1 = 1
            split_at_2 = 11
            header, message_hex = message_str[split_at_1:split_at_2], message_str[split_at_2:]
            length, node, answer_command, status, index = [header[i:i + 2] for i in
                                                           range(0, len(header), 2)]
            response_decoded = {
                'length': int(length),
                'node': int(node),
                'answer_command': str(answer_command),
                'message': str(status),
                'index': str(index)
            }



            return response_decoded


def decode_response_read(protocol='binary', message_str: str = ''):
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
        except:
            query = unpack_from('BbbbbbbbBb', message_str)
            print(query)

            dle, stx, message_sequence, node, length, answer_command, process, parameter, dle2, etx \
                = str(query).split(',')

            print(f'message_sequence_nr: {message_sequence} \nnode: {node} \nlength: {length} '
                  f'\nanswer_command: {answer_command} \nprocess: {process} '
                  f'\nparameter: {parameter}')

            response_decoded = {
                'message_sequence_nr': int(message_sequence),
                'node': int(node),
                'length': int(length),
                'answer_command': int(answer_command),
                'process': str(process),
                'parameter': str(parameter),
            }

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

            response_decoded = {
                'length': int(length),
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

            response_decoded = {
                'length': int(length),
                'node': int(node),
                'answer_command': str(answer_command),
                'process': str(process_query),
                'parameter': str(parameter_query),
            }

        return response_decoded
