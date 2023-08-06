
def decode_process_response( process_query='', type_answer=''):
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
            message= answers[process_query]
            return message
        else:
            message= int(99999999999999999999)

            return message

