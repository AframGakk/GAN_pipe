import os

class LocalService:

    def __init__(self):
        name = ''

    def rename_files(self,directory, service_pack, s_type):
        i = 0

        for filename in os.listdir(directory):
            dst = "Hostel" + str(i) + ".jpg"
            src = 'xyz' + filename
            dst = 'xyz' + dst

            fName = service_pack + '-' +  s_type + str(i) + '.wav'




            # rename() function will
            # rename all the files
            os.rename(src, dst)
            i += 1
