from queue import Queue

from matplotlib.pyplot import flag


class Node:
    """ 节点类
    变量说明：
        self.node_id   节点的 id                                 数据类型：string
        self.channels  key:节点所链接的其他节点的id                 数据类型：dictionary
                       value:本节点在该通道具有的金额(初始为总额一半)  ps：先假设支付通道总额为100，后面根据需要来修改
        self.txs       该节点要执行的交易队列                       数据类型：queue
    函数说明：
        __init__(node_id)                   类初始化
        display_node()                      打印节点的 id 和通道数（没啥用）
        channels_update(dst_id,balance)     更新节点链接的通道信息，可以增加新的通道也可以修改余额

    修改备注：
    （后面需要修改的，在这记录下）
      增加get_fund()函数                    获取通道资金
    """
    node_count = 0

    def __init__(self, node_id):
        # 初始化定义，加入节点 ID
        self.node_id = node_id
        Node.node_count += 1
        self.channels = {}
        self.txs = Queue(maxsize=0)

    def display_node(self):
        print("Node_id : ", self.node_id, "通道数：", len(self.channels))

    def channels_update(self, dst_id, balance): #更新对应支付通道的余额   
        # 支付通道的另一端 id：dst_id,变动的资金：fund
        self.channels[dst_id] = balance 

    def get_fund(self,dst_id):  #获取通道资金余额
        return self.channels[dst_id]

    def tx_put(self, transaction):
        self.txs.put(transaction)
        # print("交易 ID:", transaction.tx_id, "已装载到发起节点" )
