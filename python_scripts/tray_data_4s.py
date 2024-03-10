class ReadLine:#serial communication
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

#initialize element for operations and storing few data
source_trays = [[] for _ in range(4)]
buffer_spurce_tray=[[] for _ in range(4)]
dest_trays = [[] for _ in range(5)]


for tray in source_trays:
	for i in range(0,12):
		tray.append([1]*4)

for tray in buffer_spurce_tray:
	for i in range(0,12):
		tray.append([1]*4)
            
for tray in dest_trays:
	for i in range(0,12):
		tray.append([0]*4)
          


# tray_coords = [(290,295),(160,295),(30,295)]

source_tray_coord = [[18,88],#35 91
                     [40,200],
                     [346,90],
                     [345,202]]
# source_tray_coord = [[38,95],#35 91
#                      [40,200],
#                      [346,90],
#                      [345,202]]

dest_tray_coord = [[7,273],
                     [127,273],
                     [252,273],
                     [369,273],
                     [492,281]]
# dest_tray_coord = [[27,280],
#                      [149,280],
#                      [271,280],
#                      [389,280],
#                      [512,280]]


tray1_2_coord = [] 
tray3_4_coord = [] 

#image frame coords for each pallet
tray1_frame_bounds = [[61, 198], [605, 190], [607, 409], [62, 420]]
tray2_frame_bounds = [[61, -15], [608, -22], [610, 195], [67, 207]]
tray3_frame_bounds = [[54, 206], [595, 195], [597, 412], [58, 425]]
tray4_frame_bounds = [[50, -16], [597, -24], [598, 199], [56, 205]]
# tray1_frame_bounds = [[99, 177], [640, 169], [645, 388], [98, 396]]
# tray2_frame_bounds = [[95, -38], [639, -41], [639, 177], [101, 183]]
# tray3_frame_bounds = [[104, 179], [647, 169], [649, 390], [109, 403]]
# tray4_frame_bounds = [[100, -38], [645, -42], [647, 175], [105, 181]]

tray_vis_coord = [[86,782],
	    [86,612],
        [565,782],
	    [565,612]]

current_position = [0,0,0,1]