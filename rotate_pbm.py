import argparse


class FileNotInPBMFormat(Exception):
    pass


class Solution:
    matrix = []
    file_matrix = []

    def open_file(self,filename):
        '''Open PBM format file to read the matrix'''
        try:
            with open(filename.strip(), 'r') as f:
                for i, line in enumerate(f):
                    if i == 0:
                        if not line.strip() == 'P1': #If not start with P1 raise exception
                            raise FileNotInPBMFormat('Not a PBM format.')

                    if i >= 3: # Extracting the matrix
                        self.matrix.append(list(line.strip().split(" ")))
                    if i<2:
                        self.file_matrix.append(line)
        except FileNotInPBMFormat as e:
            raise Exception(e)
        except Exception:
            raise Exception('File or path not present.')

    def write_file(self,filename):
        '''Write the rortated matrix in the file'''
        with open(filename.split('.')[0]+'.pbm','w+') as f:
            f.write("".join(self.file_matrix))

        self.file_matrix = []


    def rotate(self, angle):
        '''Rotate the matrix on an angle'''
        angle = int(angle)
        if angle <=0:
            angle = 360-abs(angle)

        # Apply floor for angle
        angle = self.floor_angle(angle)

        if angle == 90:
            self.matrix = list(zip(*self.matrix[::-1]))
        elif angle == 270:
            self.matrix =  list(zip(*self.matrix))[::-1]
        elif angle == 180:
            self.matrix = list(zip(*list(zip(*self.matrix[::-1]))[::-1]))
        elif angle == 360:
            pass

        self.store_matrix()

    def store_matrix(self):
        self.file_matrix.append(f'{len(self.matrix[0])} {len(self.matrix)}\n')
        for i in self.matrix:
            self.file_matrix.append(str(" ".join(i)) + "\n")

    @staticmethod
    def floor_angle(angle):
        if 0<=angle<=90:
            angle = 90
        elif 90<angle<=180:
            angle = 180
        elif 180<angle<=270:
            angle = 270
        elif 270<angle<=360:
            angle = 360
        else:
            angle =360

        return angle


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='PBM Image rotation.',add_help=False)
    parser.add_argument('filename', type=str,help='an PMB filename or filepath for the rotation')
    parser.add_argument('angle', type=int, help='Rotate the image by given angle (note: Add in multiple of 90)')

    args = parser.parse_args()

    s = Solution()
    ## Opening file
    try:
        s.open_file(filename=args.filename)
    except Exception as e:
        print(e)
        exit(0)

    ## Rotating the matrix on an angle
    s.rotate(angle=args.angle)

    ## Write the rotated matrix in the file in .pbm format with same filename
    s.write_file(args.filename)
