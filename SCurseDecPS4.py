import struct
import zlib


def scurse_hash(raw_data: bytes, /) -> int:
    """
    thx to https://github.com/algmyr/ alot for helping making this function
    if you can recongise the hash aloghorthim and have a better python implemention let me know!, 
    its likley to be part of jenkins hash functions https://en.wikipedia.org/wiki/Jenkins_hash_function
    """
    byte_length = (len(raw_data)) & 0xFFFFFFFF

    golden_ratio1 = (0x9E3779B9) & 0xFFFFFFFF
    uVar4 = (0x9E3779B9) & 0xFFFFFFFF
    uVar6 = (0) & 0xFFFFFFFF
    uVar7 = (byte_length) & 0xFFFFFFFF

    if byte_length >= 12:
        while uVar7 > 11:
            uVar7 -= 12  # 12 byte chunks

            i0 = (struct.unpack("<I", raw_data[:4])[0]) & 0xFFFFFFFF
            i1 = (struct.unpack("<I", raw_data[4:8])[0]) & 0xFFFFFFFF
            i2 = (struct.unpack("<I", raw_data[8:12])[0]) & 0xFFFFFFFF

            raw_data = raw_data[12:]

            uVar6 = (i2 + uVar6) & 0xFFFFFFFF

            uVar4 = (uVar6 >> 13 ^ ((i0 + uVar4) - (i1 + golden_ratio1)) - uVar6) & 0xFFFFFFFF
            golden_ratio1 = (uVar4 << 8 ^ ((i1 + golden_ratio1) - uVar6) - uVar4) & 0xFFFFFFFF
            uVar5 = (golden_ratio1 >> 13 ^ (uVar6 - uVar4) - golden_ratio1) & 0xFFFFFFFF
            uVar4 = (uVar5 >> 12 ^ (uVar4 - golden_ratio1) - uVar5) & 0xFFFFFFFF
            uVar6 = (uVar4 << 16 ^ (golden_ratio1 - uVar5) - uVar4) & 0xFFFFFFFF
            uVar5 = (uVar6 >> 5 ^ (uVar5 - uVar4) - uVar6) & 0xFFFFFFFF
            uVar4 = (uVar5 >> 3 ^ (uVar4 - uVar6) - uVar5) & 0xFFFFFFFF
            golden_ratio1 = (uVar4 << 10 ^ (uVar6 - uVar5) - uVar4) & 0xFFFFFFFF
            uVar6 = (golden_ratio1 >> 15 ^ (uVar5 - uVar4) - golden_ratio1) & 0xFFFFFFFF

        uVar7 = ((byte_length - 12) % 12) & 0xFFFFFFFF

    uVar6 = (byte_length + uVar6) & 0xFFFFFFFF

    if uVar7 == 11:
        uVar6 = (raw_data[10] * 0x1000000 + uVar6) & 0xFFFFFFFF
    if uVar7 >= 10:
        uVar6 = (raw_data[9] * 0x10000 + uVar6) & 0xFFFFFFFF
    if uVar7 >= 9:
        uVar6 = (raw_data[8] * 0x100 + uVar6) & 0xFFFFFFFF
    if uVar7 >= 8:
        golden_ratio1 = (golden_ratio1 + raw_data[7] * 0x1000000) & 0xFFFFFFFF
    if uVar7 >= 7:
        golden_ratio1 = (golden_ratio1 + raw_data[6] * 0x10000) & 0xFFFFFFFF
    if uVar7 >= 6:
        golden_ratio1 = (golden_ratio1 + raw_data[5] * 0x100) & 0xFFFFFFFF
    if uVar7 >= 5:
        golden_ratio1 = (golden_ratio1 + raw_data[4]) & 0xFFFFFFFF
    if uVar7 >= 4:
        uVar4 = (uVar4 + raw_data[3] * 0x1000000) & 0xFFFFFFFF
    if uVar7 >= 3:
        uVar4 = (uVar4 + raw_data[2] * 0x10000) & 0xFFFFFFFF
    if uVar7 >= 2:
        uVar4 = (uVar4 + raw_data[1] * 0x100) & 0xFFFFFFFF
    if uVar7 >= 1:
        uVar4 = (uVar4 + raw_data[0]) & 0xFFFFFFFF

    uVar4 = (uVar6 >> 13 ^ (uVar4 - golden_ratio1) - uVar6) & 0xFFFFFFFF
    golden_ratio1 = (uVar4 << 8 ^ (golden_ratio1 - uVar6) - uVar4) & 0xFFFFFFFF
    uVar6 = ((golden_ratio1) >> 13 ^ ((uVar6) - (uVar4)) - (golden_ratio1)) & 0xFFFFFFFF
    uVar5 = (uVar6 >> 12 ^ (uVar4 - golden_ratio1) - uVar6) & 0xFFFFFFFF
    golden_ratio1 = (uVar5 << 16 ^ (golden_ratio1 - uVar6) - uVar5) & 0xFFFFFFFF
    uVar4 = (golden_ratio1 >> 5 ^ (uVar6 - uVar5) - golden_ratio1) & 0xFFFFFFFF
    uVar6 = (uVar4 >> 3 ^ (uVar5 - golden_ratio1) - uVar4) & 0xFFFFFFFF
    golden_ratio1 = (uVar6 << 10 ^ (golden_ratio1 - uVar4) - uVar6) & 0xFFFFFFFF

    return (golden_ratio1 >> 15 ^ (uVar4 - uVar6) - golden_ratio1) & 0xFFFFFFFF


def check_save(save_bytes: bytes, /):
    SOMEMAGICVALUE = 1224793212
    og_hash = struct.unpack("<I", save_bytes[:4])[0]

    return ((scurse_hash(save_bytes[4:]) + SOMEMAGICVALUE) & 0xFFFFFFFF) == og_hash


def decode_save(save_bytes: bytes, /, check_the_save: bool = True) -> bytes:
    WBITS = -15
    if (not check_save(save_bytes)) and check_the_save:
        raise ValueError('Hash mismatch')
        
    return zlib.decompress(save_bytes[4:],wbits=WBITS)


def encode_save(decompressed_save_bytes: bytes, /):
    WBITS = -15
    SOMEMAGICVALUE = 1224793212
    
    
    
    if len(decompressed_save_bytes) < 500:
        raise ValueError(f'Does not seem to be a decompressed save {len(decompressed_save_bytes)} bytes is too small')
    
    new_save = zlib.compress(decompressed_save_bytes,wbits=WBITS)
    
    new_hash = struct.pack("<I",(scurse_hash(new_save) + SOMEMAGICVALUE) & 0xFFFFFFFF)
    return new_hash + new_save
    
    

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
                    prog='SCurseDecPS4',
                    description='Decompress and compress saves for Shantae and the Pirate\'s Curse, along side generating the correct hash',
                    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d','-decompress',help='Decompress a compressed save, the hash is checked',action='store_true')
    group.add_argument('-c','-compress',help='Compress a decompressed save, the correct hash is also generated',action='store_true')
    


    parser.add_argument('-i', '--input', help='Input save file',required=True)
    parser.add_argument('-o', '--output', help='output save file',required=True)
        
    args = parser.parse_args()
    
    with open(args.input,'rb') as f:
        input_data = f.read()
    
    output_data = decode_save(input_data) if args.d else encode_save(input_data)
    
    with open(args.output,'wb') as f:
        f.write(output_data)
    
    if args.d:
        print(f'Decompressed {args.input} succesfully! Decompressed save is in {args.output}')
    elif args.c:
        print(f'Compressed {args.input} succesfully! Compressed save is in {args.output}')
    
    """
    from io import BytesIO
    gems_offset = 0x138C
    
    with open('savegame','rb') as f:
        save = BytesIO(decode_save(f.read()))
    
    save.seek(gems_offset)
    
    mygems = struct.unpack("<I",save.read(4))[0]
    save.seek(0)
    
    print(mygems)
    
    save.seek(gems_offset)
    
    save.write(struct.pack("<I",786))
    save.seek(0)
    
    with open('savegame.bin','wb') as f:
        f.write(encode_save(save.getvalue()))
    """
