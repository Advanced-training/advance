# coding=utf-8
from time import time
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from find_path import find_biggest_weight_path
from transaction import Transaction
from node import Node
import time
import datetime
import json
from apscheduler.schedulers.blocking import BlockingScheduler

class PCN:
    """PCN 网络类，中心处理
    变量说明：
        PCN.nodes     存储着所有的节点的实例              数据类型：dictionary 成员类型 key:string  value:Node
        PCN.txs       存储着所有的交易的实例              数据类型：list       成员类型 Transaction
        self.node_id    存储所有节点的id                  数据类型：list       成员类型 string
        self.direct_graph    双向图的拓扑结构(通道金额两边平分，一边为50，以后修改)
        self.tx_count 记录已经装载了多少交易
    函数说明：
        __init__

     修改备注：
    （后面需要修改的，在这记录下）：
        增加：visited              所有交易路径涉及的节点           数据类型 list
              finished_txs         完成的交易数量                  数据类型 int
              update()             更新PCN交易网络
              主函数
        修改：tx_load()            增加visited的相关操作,以及path[0]的判断     等
              update_state()函数   增加update的相关操作  


    """
    nodes = {}    # 存储所有 Node 类的实例         数据类型为 dictionary
    txs = []      # 存储所有 Transaction 类的实例  数据类型为 list
    visited = []  #所有交易路径涉及的节点           数据类型 list
    finished_txs = 0

    def __init__(self):
        # 初始化
        data = pd.read_table('all-in-USD-trust-lines-2016-nov-7.txt', header=None,
                             encoding='unicode-escape', delim_whitespace=True,
                             names=['src', 'dst', 'lower_bound', 'balance', 'upper_bound'])
        gra = nx.Graph()  # 先用一个无向图拿到节点列表
        #for i in range(int(len(data['src']) / 20)):  # 用 1/20的数据进行计算
        for i in range(int(len(data['src']) / 5)):  # 用1/5的数据进行计算
            gra.add_edge(data['src'][i], data['dst'][i])
        subset = max(nx.connected_components(gra), key=len)
        graph = gra.subgraph(subset)  # 最大连通子图,无向图的拓扑结构

        """
         # 根据 json 文件拿到通道数据
        with open('ripple_topology.json', 'r', encoding='utf8')as fp:
            json_data = json.load(fp)
        gra = nx.Graph()
        for i in range(len(json_data['links'])):
            gra.add_edge(json_data['links'][i]['source'], json_data['links'][i]['target'])
        graph = gra
        """
        # ########实例化所有节点加入到 nodes 中

        self.node_id = list(graph.nodes())
        for i in range(len(self.node_id)):
            node1 = Node(self.node_id[i])
            PCN.nodes[self.node_id[i]] = node1
        # #######实例化所有交易类加入到 txs 中
        # 同时构建双向拓扑图
        self.dic_graph = nx.DiGraph()
        c = 0
        for i in range(int(len(data['src']))):
            if (data['src'][i] in self.node_id) and (data['dst'][i] in self.node_id):
                c += 1
                trans = Transaction(c, data['src'][i], data['dst'][i], data['balance'][i])  # 实例化交易类
                trans.time_set(2000)
                self.dic_graph.add_weighted_edges_from(
                    [(data['src'][i], data['dst'][i], 50.0), (data['dst'][i], data['src'][i], 50.0)])  # 有向图添加边，金额平分
                PCN.txs.append(trans)  # 添加到交易列表中
                PCN.nodes[data['src'][i]].channels_update(trans.receiver, 50.0)  # 更新节点里的交易通道信息
                
                #通道另一边也要增加
                PCN.nodes[data['dst'][i]].channels_update(trans.sender, 50.0)
                #PCN.nodes[data['src'][i]].display_node()
        # ###

        """
        for i in range(len(list(graph.edges()))):
            c += 1
            trans = Transaction(c, list(graph.edges())[i][0], list(graph.edges())[i][1], 50)
            self.dic_graph.add_weighted_edges_from(
                [(list(graph.edges())[i][0], list(graph.edges())[i][1], 50),
                 (list(graph.edges())[i][1], list(graph.edges())[i][0], 50)])
            PCN.nodes[(list(graph.edges())[i][0])].channels_update(list(graph.edges())[i][1], 50)
        """
        self.tx_count = 0
        print(len(list(self.dic_graph.edges())))
        print(len(list(self.dic_graph.nodes())))
        print(len(PCN.nodes))
        print(len(PCN.txs))

    # update()
    def tx_load(self):  # 装载30笔交易到节点上
        print('load txs')
        # 取出三十笔交易
        if 30 < len(self.txs):
            tx_preload = self.txs[0:30]
            del self.txs[0:30]  # 删除掉取出的交易，节省空间
        else:
            tx_preload = self.txs[0:len(self.txs)]
            del self.txs[0:len(self.txs)]  # 删除掉取出的交易，节省空间
        #self.visited.append(tx_preload[0].sender)

        graph_copy = self.dic_graph  #拷贝一个拓扑结构吗，用以计算路径

        for i in range(len(tx_preload)):
            tmp = tx_preload[i]
            # 给交易装载路径
            path = find_biggest_weight_path(graph_copy, tmp.sender, tmp.receiver)
            #print('len of path: ',len(path))
            #print('len of path[0]',len(path[0]))
            if len(path[0]) > 0:
                tx_preload[i].path_gain(path[0])
            
                #增加 visited            OK
                self.visited.extend(path[0])
                self.visited = list(set(self.visited))

                #print('len of path[0]',len(path[0]))
                #print('len of visited',len(self.visited))

                # 在双向拓扑图中把 path 执行
                for j in range(len(path[0]) - 1):
                    graph_copy[path[0][j]][path[0][j + 1]]['weight'] -= tmp.trade
                    graph_copy[path[0][j + 1]][path[0][j]]['weight'] += tmp.trade
                # 交易处理完毕，然后装载到对应节点上
                self.nodes[tx_preload[i].sender].tx_put(tx_preload[i])
    
    def update(self):
        print('update pcn')
        print('visited len: ',len(self.visited))
        for nid in self.visited: #取可能存在交易的节点
            node = self.nodes[nid]
            if node.txs.empty() == False:  #节点交易队列不空
                tx = node.txs.get()            #取节点交易队列第一笔交易
                
                #检查是否交易到达终点或此交易过期
                while (tx.position == (len(tx.path) - 1)) or (tx.time_check() == False):
                    #交易到达终点则将交易完成数加1    
                    if tx.position == (len(tx.path) -1):
                        self.finished_txs += 1 
                        print('-----------------------------finished: ',self.finished_txs)
                    if node.txs.empty() == False:
                        tx = node.txs.get()              #重新取交易
                    else:                       #队列为空，跳过此节点
                        break
                # print('find txs')
                # print('position: ',tx.position)
                # print('tx.path: ',len(tx.path)) 
                # print('time_limit: ',tx.time_limit)

                # 已解决        问题：节点不满足下列if 条件 ,因为time_limit一直为0 
                #交易未到达终点且未过期              
                ##注意 此处的node，next_node != tx.sender,tx.receiver
                if (tx.position < (len(tx.path) - 1)) and (tx.time_check() == True): 
                    #print('to pass')  
                    tx.time_update()   #  更新交易过期时间（发不发送交易都要更新）
                    next_node_id = tx.path[tx.position + 1]
                    fund1 = node.get_fund(next_node_id)
                    fund2 = self.nodes[next_node_id].get_fund(nid)
                    if  fund1 > tx.trade: #通道资金足够，发送交易
                        tx.update()                          #更新交易信息（位置）
                        self.nodes[next_node_id].tx_put(tx)  #将该交易发送给下一节点（假如下一节点的交易队列）
                        #更改通道资金
                        self.nodes[nid].channels_update(next_node_id,fund1 - tx.trade)  #node资金减少
                        self.nodes[next_node_id].channels_update(nid,fund2 + tx.trade)  #next node资金增加
                        #更改网络拓扑
                        self.dic_graph[nid][next_node_id]['weight'] -= tx.trade
                        self.dic_graph[next_node_id][nid]['weight'] += tx.trade

                    #print('pass')  

    def load_update(self):
        self.tx_load()
        self.update()

    def update_state(self):
        self.finished_txs = 0
        
        i = 0
        while ((len(self.txs) > 0) and (i < 9)):  #每300ms，进行9次更新   括号不能少
            print('-----------------load&update',i,'----------------')
            self.tx_load()  # 装载了三十笔交易,装载到每笔交易的起始节点上
            self.update()
            time.sleep(1/30)
            i += 1
        return self.finished_txs  
        # self.tx_load()
        # self.finished_txs = 0
        # self.update()
        #time.sleep(1/30)


        # time_length = 0.3
        # now = datetime.datetime.now()
        # end = now + datetime.timedelta(seconds=time_length)
        # self.finished_txs = 0

        # scheduler = BlockingScheduler()
        # scheduler.add_job(self.load_update,'interval',seconds = 1/30,end_date=end)      #每1/30秒进行一次交易装载
        # #scheduler.add_job(self.update,'interval',seconds = 1/30,end_date=end)       # 节点并行处理自己交易队列中的交易
        # scheduler.start()
        #return self.finished_txs



#pcn = PCN()
if __name__ == '__main__':
    pcn = PCN()
    
    print('-----------------init success!-------------------')

    total_recv = 0
    time_span = 1000

    print('start work!')
    for i in range(time_span):
        print('----------------------work cycle:',i,'----------------')
        recv_num = pcn.update_state()
        print('Transactions finished in the time_span: ',recv_num)
        total_recv += recv_num
    
    print('Transactions finished in the %d time_span: %d'%(time_span,total_recv))