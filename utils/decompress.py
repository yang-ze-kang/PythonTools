from genericpath import isdir
import os
import pyzipper
import rarfile

class Decompress():

    def __init__(self,filepath,output_path='',password='',type='',signal=None) -> None:
        self.support_type = ['zip']
        self.type = type
        self.filepath = filepath
        self.output_path = self.filepath+'_decompression' if output_path == '' else output_path
        self.password = password
        self.signal = signal
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
    
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

if __name__=="__main__":
    Decompress(r'E:\ict\爱尔眼科\数据\220711重庆一名患者数据\20220711_single_patient_data',
    r'E:\ict\爱尔眼科\数据\220711重庆一名患者数据\20220711_single_patient_data_1',
    'aier_zhongkeyuan_cooperativeProject').process()

