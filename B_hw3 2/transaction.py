class Transaction:
    """交易类
    变量说明：
        self.tx_id     交易的 id，从1开始           数据类型：int
        self.sender    交易的发起者                 数据类型：string
        self.receiver  交易的接受者                 数据类型：string
        self.trade     交易的交易额                 数据类型：float
        self.path      交易执行路径                 数据类型：list
        self.position  交易的执行进度               数据类型：int
        self.time_limit交易的时间限制               数据类型：暂定
    函数说明：
        path_gain(path_list)           把计算得到的路径存储到 self.path 中
        update()                       更新当前交易的进度，即 position 自动加1
        time_check()                   检查该交易是否过期 (待实现)


     修改备注：
    （后面需要修改的，在这记录下）
        设定：self.time_limit  交易的时间限制             数据类型：int 以网络的一个单位时间为1
        增加：time_set(self,time)函数                    设定交易过期时间
              time_update()函数
        修改：time_check()函数
    """

    def __init__(self, tx_id, sender, receiver, trade):
        # 初始化定义，tx_id:交易id,sender:交易发起方，receiver:交易接收方，trade:交易额
        self.tx_id = tx_id  # 交易 id
        self.sender = sender  # 交易发起方
        self.receiver = receiver  # 交易接收方
        self.trade = trade  # 交易额
        self.path = []  # 交易路径
        self.position = 0  # 当前交易执行到路径哪一步

        #########
        self.time_limit = 0  # 该交易的过期时间(格式待修改)
        #########

    def path_gain(self, path_list):
        # 计算得到路径后，对该交易的路径进行赋值，path_list:该交易的执行路径 数据类型为 list
        self.path = path_list
        #self.position = 
        # print("交易：%d 已完成路径装载" % self.tx_id)

    def update(self):
        # 更新当前交易的执行状态
        # 路径上的当前位置 自动加一
        self.position += 1
        
    def time_update(self):
        #并更新过期时间
        self.time_limit -= 1

    def time_check(self):
        # 检查当前交易是否过期（待实现）
        #self.time_limit += 1
        #修改                            time_limit == 0则为过期,返回false
        timeout = True if self.time_limit > 0 else False
        return timeout
    
    def time_set(self,time):
        # 设置交易过期时间
        self.time_limit = time
        ######
        ######
        ######
