# OOM
thrift程序无故退出，查看日志未发现错误信息，观察思考后得知，内存溢出，程序被OOM机制杀死。
# Python排查
## pympler-大致定位
```
from pympler import tracker,summary,muppy
mt = tracker.SummaryTracker()

code..

mt.print_diff()
```
## tracemalloc-精确定位
```
import tracemalloc
tracemalloc.start(25)
snapshot = tracemalloc.take_snapshot()

code..

snapshot1 = tracemalloc.take_snapshot()
top_stats = snapshot1.compare_to(snapshot, 'lineno')
print("[ Top 10 differences ]")
for stat in top_stats[:10]:
    if stat.size_diff < 0:
        continue
    print(stat)
snapshot = tracemalloc.take_snapshot()
```

# 进度和结果
```
实验
200次
pympler 测试了ocr、fd、gt和mp

结果
ocr、gt、mp未出现内存溢出
fd出现溢出，一次2M

fd精确溯源的位置
#261: /app/fd_gt/fd.py:59: 0.9 KiB
    anchors_tensor = K.reshape(K.constant(anchors), [1, 1, 1, num_anchors, 2])

print(type(anchors_tensor))
print(anchors_tensor)
<class 'tensorflow.python.framework.ops.Tensor'>
Tensor("Reshape:0", shape=(1, 1, 1, 3, 2), dtype=float32)

```
## 尝试解决
```
anchors_tensor = tf.constant(1.2, shape=[1, 1, 1, 3, 2])

效果不明显，说明是按照大小排序，并没有tranceback
```

## 思考
pympler可以输出一个大致梗概

tracemalloc可以输出详细的追溯

大都是以文本的形式

如果人眼是回溯很难做到

画图工具来显示内存的调用？

是否可以使用火焰图来画出函数的调用，并且展示内存用量的信息？


如果找不到相应的工具的话，通过手工，使用pympler来一步一步的定位，速度将会缓慢

并且一步一步的定位，很难看到全局的信息


# 最终解决方案任选其一
## 1.升级安装包
pip3 install --upgrade Keras==2.1.5
## 2.更改代码
```
from keras import backend as K
replace
import tensorflow.compat.v1 as tf
K = tf.keras.backend
```






















