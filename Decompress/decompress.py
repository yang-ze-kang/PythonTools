import os
import pyzipper
import rarfile
from PyQt5.QtCore import QThread,pyqtSignal

class Decompress():

    def __init__(self,filepath,output_path='',password='',type='',signal=None) -> None:
        self.support_type = ['zip']
        self.type = type
        self.filepath = filepath
        self.output_path = self.filepath+'_decompression' if output_path == '' else output_path
        self.password = password
        self.signal = signal
    
    def process(self):
        self.decompress_files(self.filepath,self.output_path)
        self.delete_compressed_files(self.output_path)
    
    def decompress_files(self,path,out_dir):
        filepaths = os.listdir(path)
        for filepath in filepaths:
            sp = filepath.split('.')
            if len(sp)==2 and sp[1] in self.support_type:
                if sp[1] == 'zip':
                    self.unzip_file(os.path.join(path,filepath),os.path.join(out_dir,sp[0]))
                    self.decompress_files(os.path.join(out_dir,sp[0]),os.path.join(out_dir,sp[0]))
            elif len(sp)==1:
                if not os.path.exists(os.path.join(out_dir,sp[0])):
                    os.mkdir(os.path.join(out_dir,sp[0]))
                self.decompress_files(os.path.join(path,sp[0]),os.path.join(out_dir,sp[0]))
   
    # zip解压缩
    def unzip_file(self,filepath,output_path,password=''):
        if self.signal is not None:
            self.signal.emit(filepath)
        if password=='':
            password=self.password
        with pyzipper.AESZipFile(filepath, 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zp:
            zp.extractall(path=output_path,pwd=str.encode(password))
    
    def delete_compressed_files(self,path):
        filepaths = os.listdir(path)
        for filepath in filepaths:
            sp = filepath.split('.')
            if len(sp)==2 and sp[1] in self.support_type:
                os.remove(os.path.join(path,filepath))
            elif len(sp)==1:
                self.delete_compressed_files(os.path.join(path,filepath))

class DecompressThread(QThread):
    logSignal = pyqtSignal(str)

    def __init__(self,sourceDir,destDir,password='') -> None:
        super().__init__()
        self.decompress = Decompress(sourceDir,destDir,password,signal=self.logSignal)

    def run(self):
        self.decompress.process()
        self.logSignal.emit('解压完成！')



if __name__=="__main__":
    Decompress(r'C:\Users\Dell\Desktop\220812data-几例患者数据\A',
    r'C:\Users\Dell\Desktop\220812data-几例患者数据\A2',
    'aier_zhongkeyuan_cooperativeProject').process()

