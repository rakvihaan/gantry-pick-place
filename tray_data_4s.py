class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s
    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i + 1]
            self.buf = self.buf[i + 1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i + 1]
                self.buf[0:] = data[i + 1:]
                return r
            else:
                self.buf.extend(data)


source_trays = [[] for _ in range(4)]
dest_trays = [[] for _ in range(5)]

for tray in source_trays:
	for i in range(0,12):
		tray.append([1]*4)

for tray in dest_trays:
	for i in range(0,12):
		tray.append([0]*4)


# for tray in dest_trays:
# 	print(tray)
# 	print("\n")
      

# tray_dest.append(tray_comp)
# tray_dest.append(tray_inComp)

# tray_coords = [(290,295),(160,295),(30,295)]

source_tray_coord = [[20,81.5],
                     [20,255.5],
                     [320,81.5],
                     [320,255.5]]

dest_tray_coord = [[20,250],
                     [140,250],
                     [260,250],
                     [380,250],
                     [500,250]]

# # print(tray_dest[0])
# dtt = source_trays[0]
#             # print(dtt)
# for col, val in enumerate(dtt):
#     for roww, value in enumerate(val):
#         if value == 1:
#             print(col,roww)