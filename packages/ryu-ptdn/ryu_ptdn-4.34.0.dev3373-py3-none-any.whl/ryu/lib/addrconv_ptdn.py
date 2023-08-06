import struct as _struct
from struct import unpack as _unpack, pack as _pack
from netaddr.compat import _bytes_join, _is_str
from netaddr.core import AddrFormatError

AF_PNET = 18 # just give a random number
FOUR_BIT_MAX_INT = 15 #Multicast id 20-8-8 bit validation

# Unlike C language, we have no need to add a holder because we can check if it is in the dictionary
ptdn_type_defined = {'RESERVED':'0','PTDN64':'1', 'PTDN96':'2', 'PTDN128':'3', 'PTDN_TYPE_MUL':'4' }

service_type_defined = {'RESOURCE_GUARANTEED':'0','High_QUALITY':'1', 'NORMAL_QUALITY':'2', 'BEST_EFFORT':'3'}

class PTAddressConverter(object):
    def __init__(self):
        pass

    #str ---> binary
    def text_to_bin(self, text):
        try:
            return ptdn_pton(AF_PNET, text) 
        except Exception as e:
            raise e

    # bin->str      
    def bin_to_text(self, bin):  
        return ptdn_ntop(AF_PNET, bin)
    
# Convert the string including ptdn_address_type, ptdn_service_type, ptdn_core_address to >binary format   
def ptdn_pton(af,ptdn_string):
    if af == AF_PNET:
        res = ptdn_string.split('-')
        #Error Cases
        invalid_type = ValueError('illegal PTDN type string %r' % res[0])
        invalid_service_type = ValueError('illegal PTDN type string %r' % res[1])
        
        #Data set
        values = []
        ptdn_type = res[0]
        service_type = res[1]

        #Validation & Conversion
        if ptdn_type in ptdn_type_defined.values():    # validate ptdn address type 
        
            values.append(_pack('i', int(ptdn_type)))  # c: bytes of length 1. 0i: 32 bit alignment
        else:
            raise invalid_type
        
        if service_type in service_type_defined.values(): # validate service type
            values.append(_pack('i', int(service_type)))   # c: bytes of length 1. 0i: 32 bit alignment
        else:
            raise invalid_service_type

        values.append(_ptdn_pton_af_inet(ptdn_core_addr = res[2], ptdn_type = ptdn_type)) # 16 byte
        return _bytes_join(values)
    else:
        raise ValueError('Unknown address family %d' % af)

# Convert ptdn_core_address to >bytes
def _ptdn_pton_af_inet(ptdn_core_addr, ptdn_type):
    
    invalid_addr = ValueError('illegal PTDN address string %r' % ptdn_core_addr)
    values = []

    #Error Filter
    if not _is_str(ptdn_core_addr):
        raise invalid_addr

    if 'x' in ptdn_core_addr:
        #   Don't accept hextets with the 0x prefix.
        raise invalid_addr

    if ptdn_type == ptdn_type_defined['RESERVED']:
        raise ValueError('can not user reserved ptdn address type')

    if ptdn_type != ptdn_type_defined['PTDN_TYPE_MUL']:
        #Start to parse
        if '::' in ptdn_core_addr:
            if ptdn_core_addr == '::':
                #   Unspecified address.
                return '\x00'.encode() * 16
            #   IPv6 compact mode.
            try:
                prefix, suffix = ptdn_core_addr.split('::')
            except ValueError:
                raise invalid_addr
        
            l_prefix = []
            l_suffix = []

            if prefix != '':
                l_prefix = prefix.split(':')

            if suffix != '':
                l_suffix = suffix.split(':')

            #   PTDN do not compact with IPv4.
            if len(l_suffix) and '.' in l_suffix[-1]:
                raise invalid_addr

            token_count = len(l_prefix) + len(l_suffix)

            if not 0 <= token_count <= 8 - 1:
                raise invalid_addr
            
            gap_size = 8 - ( len(l_prefix) + len(l_suffix) )

            for i in l_prefix:
                values.append(_pack('>H', int(i, 16)) )
            for i in range(gap_size):
                values.append('\x00\x00'.encode() )
            for i in l_suffix:
                values.append(_pack('>H', int(i, 16)) )

            try:
                for token in l_prefix + l_suffix:
                        word = int(token, 16)
                        if not 0 <= word <= 0xffff:
                            raise invalid_addr
            except ValueError:
                raise invalid_addr
        else:
            #   PTDN verbose mode.
            if ':' in ptdn_core_addr:
                tokens = ptdn_core_addr.split(':')

                if '.' in ptdn_core_addr:
                    raise invalid_addr
                else:
                    #  PTDN verbose mode.
                    if len(tokens) != 8:
                        print(len(tokens))
                        raise invalid_addr
            
            else:
                    raise invalid_addr
            
            try:
                tokens = [int(token, 16) for token in tokens]
                for token in tokens:
                    if not 0 <= token <= 0xffff:
                        raise invalid_addr
            except ValueError:
                raise invalid_addr
            
            for i in tokens:
                item = _pack('>H', i)            
                values.append(item)
    else:
        #MULTI PARSING
        if '.' in ptdn_core_addr:
            str_list = ptdn_core_addr.split('.')
            int_list = []
            for strs in str_list:
                try:
                    int_val = int(strs)
                    int_list.append(int_val)
                except ValueError:
                    raise invalid_addr

            # mask: 00001111 11111111 11111111
            if int_list[0] <0 or int_list[0]> FOUR_BIT_MAX_INT: #only 4 bit the max num is 15
                raise invalid_addr

            if int_list[1] <0 or int_list[0]>255 or int_list[2] <0 or int_list[1]>255:
                raise ValueError('illegal PTDN address string %r' % int_list[0])
            
            if len(int_list)!=3:# should have 3 bytes in multi num
                raise invalid_addr

            # PADDING 128-24 bit   

            for items in int_list:
                values.append(_pack('c',bytes([items])))
            
            values.append(_pack('c',bytes([0])))
            values.append(_pack('3I',0,0,0))
           

        else:
            raise invalid_addr

    return _bytes_join(values)
    
# Convert 24 byte binary string to int value
def packed_to_int(packed_int):
    """
    :param packed_int: need to be divided into 4I each (32bit) a packed string containing an unsigned integer.
        It is assumed that string is packed in network byte order.

    :return: An unsigned integer equivalent to value of network address
        represented by packed binary string.
    """
    words = list(_struct.unpack('>6I', packed_int)) # 6* 4byte

    #similar to (3111)(2) = 3*2^4 +1*2^3 + 1*2^2 + 1*2^1
    int_val = 0
    for i, num in enumerate(reversed(words)):
        word = num
        word = word << 32 * i
        int_val = int_val | word
        
    return int_val 

# Deal with raw tokens  with unhandled zeros, add blank space for tagging :: 
# Examle: ['2001','db8','0','0','0','0','0','1'] -> ['2001','db8','','1']
def ipv6_tokens_handler(tokens):
    new_tokens = []

    positions = []
    start_index = None
    num_tokens = 0

    #   Discover all runs of zeros.
    for idx, token in enumerate(tokens):
        if token == '0':
            if start_index is None:
                start_index = idx
            num_tokens += 1
        else:
            if num_tokens > 1:
                positions.append((num_tokens, start_index))
            start_index = None
            num_tokens = 0

        new_tokens.append(token)

    #   Store any position not saved before loop exit.
    if num_tokens > 1:
        positions.append((num_tokens, start_index))

    #   Replace first longest run with an empty string.
    if len(positions) != 0:
        #   Locate longest, left-most run of zeros.
        positions.sort(key=lambda x: x[1])
        best_position = positions[0]
        for position in positions:
            if position[0] > best_position[0]:
                best_position = position
        #   Replace chosen zero run.
        (length, start_idx) = best_position
        new_tokens = new_tokens[0:start_idx] + [''] + new_tokens[start_idx + length:]

        #   Add start and end blanks so join creates '::'.
        if new_tokens[0] == '':
            new_tokens.insert(0, '')

        if new_tokens[-1] == '':
            new_tokens.append('')

    return new_tokens



def ptdn_multi_tokens_handler(token):
    values = []
    binary = _pack('>2H', int(token[0],16), int(token[1],16))

    new_tokens = ['%r' %i for i in _unpack('>4B', binary)][:-1]
    return new_tokens

# From packet binary format to String format
# Example: b'\x00\x00\x00\x02\x00\x00\x00\x02\x11\x11\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb08
#          2-2-1111::b038 (ptdn_address_type, ptdn_service_type, ptdn_core_address)
def ptdn_ntop(af, packed_ptdn):
    """Convert an PTDN address of the given family to string format. """
    final_list = []
    
    if af == AF_PNET:
        #PTDN
        if len(packed_ptdn) != 24 or not _is_str(packed_ptdn):
            raise ValueError('invalid length of packed PTDN address string')

        tokens = ['%x' % i for i in _unpack('>12H', packed_ptdn)]
        byte_tokens = ['%x' % i for i in _unpack('>24B', packed_ptdn)]

        # Handle the ptdn address type info 
        ptdn_type_int = int(byte_tokens[0],16)
        ptdn_type_str = str(ptdn_type_int)
        final_list.append(ptdn_type_str) 

        # Handle the ptdn service type info
        ptdn_service_types_str = str(int(byte_tokens[4],16))
        final_list.append(ptdn_service_types_str)

        # Handle the ptdn core address field, using the IPV6 handling method 
        if ptdn_type_int == int(ptdn_type_defined['RESERVED']):
            raise ValueError('Can not handle reserved ptdn type')

        if ptdn_type_int != int(ptdn_type_defined['PTDN_TYPE_MUL']):       
            ptdn_core_addr_str = ':'.join(ipv6_tokens_handler(tokens[4:]))
        else:
            # intercept the last 2 elements(four bytes) in the list
            ptdn_core_addr_str = '.'.join(ptdn_multi_tokens_handler(tokens[4:6]))
        final_list.append(ptdn_core_addr_str)

        # Cat the final list using '-'
        return '-'.join(final_list)

    else: 
        raise Exception('INVALID Address Family!', af)

ptdn = PTAddressConverter()
