from common import  *
import numpy as np
from lstm import *
import matplotlib.pyplot as plt

TIME_STEPS = 9
BATCH_SIZE = 50
INPUT_SIZE = 5
OUTPUT_SIZE = 2
CELL_SIZE = 20

x_data,y_data = getAllData(0,(BATCH_SIZE*TIME_STEPS+1)*10)


x_data = (x_data-np.min(x_data,axis=0))/(np.max(x_data,axis=0)-np.min(x_data,axis=0))

RNN = LSTMRNN(TIME_STEPS, INPUT_SIZE, OUTPUT_SIZE, CELL_SIZE, BATCH_SIZE)
sess = tf.Session()
sess.run(tf.global_variables_initializer())     # initialize var in graph
plt.figure(1, figsize=(12, 5)); plt.ion()       # continuously plot

saver = tf.train.Saver(tf.global_variables())
module_file = tf.train.latest_checkpoint('dnnckpt')

for step in range(0,100000):
    x = np.array(x_data).reshape((BATCH_SIZE,TIME_STEPS,INPUT_SIZE))

    y = np.array(y_data).reshape(((BATCH_SIZE,TIME_STEPS,OUTPUT_SIZE)))

    if 'final_s_' not in globals():                 #
        feed_dict = {RNN.xs: x, RNN.ys: y}
    else:                                           # has hidden state, so pass it to rnn
        feed_dict = {RNN.xs: x, RNN.ys: y, RNN.cell_init_state: final_s_}
    _, pred_, final_s_,_loss = sess.run([RNN.train_op,RNN.pred,RNN.cell_final_state,RNN.cost], feed_dict)     # train
    if step%50==0:
        print(sess.run(RNN.accuracy, feed_dict={
            RNN.xs: x,
            RNN.ys: y,
        }))
