from matplotlib import pyplot as plt
import os
import torch
import time
import scipy.signal
import numpy as np
from sklearn.metrics import f1_score
import matplotlib
matplotlib.use('Agg')


class Log():
    def __init__(self, log_dir, model_name, num_classes):
        self.num_classes = num_classes
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.logs_dir = 'logs'
        self.log_dir = log_dir
        self.save_path = os.path.join(
            self.logs_dir, self.log_dir+'_'+str(now_time))
        self.model_name = model_name
        self.f1s_train = []
        self.f1s_test = []
        self.train_accuracy = []
        self.val_accuracy = []
        self.train_lr = []
        os.makedirs(self.save_path)
        os.makedirs(os.path.join(self.save_path, 'model'))

    def append_epoch_num2(self, name, train, test):
        if not hasattr(self, name+'_train'):
            setattr(self, name+'_train', [])
        if not hasattr(self, name+'_test'):
            setattr(self, name+'_test', [])
        list_train = getattr(self, name+'_train')
        list_test = getattr(self, name+'_test')
        list_train.append(train)
        list_test.append(test)
        with open(os.path.join(self.save_path, name+'.txt'), 'a') as f:
            f.write(str(train)+' '+str(test)+'\n')
        self.plot_curves_num2(name)

    def plot_curves_num2(self, name):
        train = getattr(self, name+'_train')
        test = getattr(self, name+'_test')
        iters = range(len(train))
        plt.figure()
        plt.title(self.model_name)
        plt.plot(iters, train, 'red',
                 linewidth=2, label='train '+name)
        plt.plot(iters, test, 'coral',
                 linewidth=2, label='val '+name)
        try:
            if len(self.train_losses) < 25:
                num = 5
            else:
                num = 15
            plt.plot(iters, scipy.signal.savgol_filter(train, num, 3), 'green', linestyle='--', linewidth=2,
                     label='smooth train '+name)
            plt.plot(iters, scipy.signal.savgol_filter(test, num, 3), '#8B4513', linestyle='--', linewidth=2,
                     label='smooth val '+name)
        except:
            pass
        plt.grid(True)
        plt.xlabel('Epoch')
        plt.ylabel(name)
        plt.legend(loc="upper right")
        plt.savefig(os.path.join(self.save_path, name+".png"))
        plt.cla()
        plt.close("all")

    def extend_batch(self, name, vals):
        if not hasattr(self, name):
            setattr(self, name, [])
        l = getattr(self, name)
        l.extend(vals)

    def caluate_f1(self):
        assert len(self.preds_train) == len(self.labels_train)
        train_f1 = f1_score(self.labels_train, self.preds_train,
                            labels=list(range(self.num_classes)),
                            average=None)
        assert len(self.labels_test) == len(self.preds_test)
        test_f1 = f1_score(self.labels_test, self.preds_test,
                           labels=list(range(self.num_classes)),
                           average=None)
        train_f1 = np.mean(train_f1)
        test_f1 = np.mean(test_f1)
        self.f1s_train.append(train_f1)
        self.f1s_test.append(test_f1)
        with open(os.path.join(self.save_path, "f1s.txt"), 'a') as f:
            f.write(str(train_f1)+' '+str(test_f1)+'\n')
        self.plot_curves_num2('f1s')
        self.preds_train = []
        self.labels_train = []
        self.preds_test = []
        self.labels_test = []

    def save_model(self, model, name=None):
        if name is None:
            save_path = os.path.join(self.save_path, 'model', 'best.pth')
        else:
            save_path = os.path.join(self.save_path, 'model', name+'.pth')
        if isinstance(model, torch.nn.DataParallel):
            model = model.module
        torch.save(model.state_dict(), save_path)

    def save_check_point(self, epoch, model, optimizer, lr_scheduler):
        if isinstance(model, torch.nn.DataParallel):
            model = model.module
        check_point = {
            'index': epoch,
            'model': model,
            'optimizer': optimizer,
            'lr_scheduler': lr_scheduler
        }
        torch.save(check_point, os.path.join(
            self.save_path, 'model', 'last.pth'))
