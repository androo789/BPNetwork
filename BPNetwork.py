
# -*- coding: utf-8 -*-

import math
import numpy as np
import scipy.io as sio


# 读入数据
################################################################################################
print "输入样本文件名（需放在程序目录下）"
filename = 'mnist_train.mat' # raw_input()
sample = sio.loadmat(filename)
sample = sample["mnist_train"]
sample /= 256.0       # 特征向量归一化

print "输入标签文件名（需放在程序目录下）"
filename = 'mnist_train_labels.mat' # raw_input()
label = sio.loadmat(filename)
label = label["mnist_train_labels"]

##################################################################################################


# 神经网络配置
##################################################################################################
samp_num = len(sample)      # 样本总数
inp_num = len(sample[0])    # 输入层节点数
out_num = 10                # 输出节点数
hid_num = int(math.sqrt(0.43*inp_num*out_num + 0.12*out_num**2 + 2.54*inp_num + 0.77*out_num + 0.35)+0.51)       # 隐层节点数(经验公式)
w1 = 0.2*np.random.random((inp_num, hid_num))-0.1   # 初始化输入层权矩阵
w2 = 0.2*np.random.random((hid_num, out_num))-0.1   # 初始化隐层权矩阵
delta2 = np.zeros(out_num)                 # 隐层到输出层的delta
delta1 = np.zeros(hid_num)                 # 输入层到隐层的delta
inp_lrate = 0.5             # 输入层学习率
hid_lrate = 0.5             # 隐层学习率
err_th = 0.01                # 学习误差门限


###################################################################################################

# 必要函数定义
###################################################################################################
def get_act(x):
    act_vec = []
    for i in x:
        act_vec.append(1/(1+math.exp(-i)))
    act_vec = np.array(act_vec)
    return act_vec

def sigmoid(x):
    return 1/(1 + math.exp(-x))

def get_err(y, l):
    return 0.5*np.dot((y-l), (y-l))


###################################################################################################

# 训练
###################################################################################################
test=0
for count in range(0, 10000):
    print 'Processing....'
    print count
    hid_value = np.dot(sample[count], w1)       # 隐层值
    hid_act = get_act(hid_value)                # 隐层激活值
    out_value = np.dot(hid_act, w2)             # 输出层值
    out_act = get_act(out_value)                # 输出层激活值
    t_label = np.zeros(out_num)
    t_label[label[count]] = 1
    err = get_err(out_act, t_label)        # 计算误差
    print err
    if err <= err_th:
        print "Training finished, OK"
    else:
        for i in range(0, len(delta2)):
            delta2[i] = (t_label[i] - out_act[i])# * sigmoid(out_value[i]) * (1 - sigmoid(out_value[i]))        # 输出层delta
            w2[:, i] = w2[:, i] + hid_lrate * delta2[i] * hid_act  # 更新隐层到输出层权向量

        for j in range(0, len(delta1)):
            delta1[j] = sigmoid(hid_value[j]) * (1 - sigmoid(hid_value[j])) * np.dot(delta2, w2[j])  # 隐层delta
            w1[:, j] = w1[:, j] + inp_lrate * delta1[j] * sample[j]  # 更新隐层到输出层权向量
###################################################################################################

# 输出网络
###################################################################################################
Network = open("MyNetWork", 'w')
Network.write(str(inp_num))
Network.write('\n')
Network.write(str(hid_num))
Network.write('\n')
Network.write(str(out_num))
Network.write('\n')
for i in w1:
    for j in i:
        Network.write(str(j))
        Network.write(' ')
    Network.write('\n')
Network.write('\n')

for i in w2:
    for j in i:
        Network.write(str(j))
        Network.write(' ')
Network.write('\n')

Network.close()








