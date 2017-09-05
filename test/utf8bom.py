# import os, sys, codecs

# BUFSIZE = 4096
# BOMLEN = len(codecs.BOM_UTF8)

# with open("ip.txt", "r+b") as fp:
#     chunk = fp.read(BUFSIZE)
#     if chunk.startswith(codecs.BOM_UTF8):
#         i = 0
#         chunk = chunk[BOMLEN:]
#         while chunk:
#             fp.seek(i)
#             fp.write(chunk)
#             i += len(chunk)
#             fp.seek(BOMLEN, os.SEEK_CUR)
#             chunk = fp.read(BUFSIZE)
#         fp.seek(-BOMLEN, os.SEEK_CUR)
#         fp.truncate()

# def trim_bom(file_path):
#     BOM = b'\xef\xbb\xbf'
#     with open(file_path, 'rb') as f:
#         if f.read(3) == BOM:
#             data = f.read()
#             with open(file_path, 'wb') as f:
#                 f.write(data)
# trim_bom("ip.txt")

BOM = b'\xef\xbb\xbf'
with open("ip.txt", 'rb') as f:
    if f.read(3) == BOM:
        data = f.read()
        with open("ip.txt", 'wb') as f:
            f.write(data)