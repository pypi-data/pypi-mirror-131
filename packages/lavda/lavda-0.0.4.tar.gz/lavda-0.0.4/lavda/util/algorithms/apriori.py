# -*- coding:utf-8 -*-
"""
apriori 算法
"""


class Apriori(object):
    def __init__(self, print_detail=False):
        self.print_detail = print_detail

    def createC1(self, dataSet):
        C1 = []
        for transaction in dataSet:
            for item in transaction:
                if not [item] in C1:
                    C1.append([item]) #store all the item unrepeatly

        C1.sort()
        #return map(frozenset, C1)#frozen set, user can't change it.
        return list(map(frozenset, C1))

    def scanD(self, D,Ck,minSupport):
        """
        
        :param D: 数据集
        :param Ck: 候选项集列表Ck
        :param minSupport: 感兴趣项集的最小支持度 minSupport
        :return: 
        """
        ssCnt={}
        for tid in D:#遍历数据集
            for can in Ck:#遍历候选项
                if can.issubset(tid):#判断候选项中是否含数据集的各项
                    #if not ssCnt.has_key(can): # python3 can not support
                    if not can in ssCnt:
                        ssCnt[can]=1 #不含设为1
                    else: ssCnt[can]+=1#有则计数加1
        numItems=float(len(D))#数据集大小
        retList = []#L1初始化
        supportData = {}#记录候选项中各个数据的支持度
        for key in ssCnt:
            support = ssCnt[key]/numItems#计算支持度
            if support >= minSupport:
                retList.insert(0, key)#满足条件加入L1中
                supportData[key] = support
        return retList, supportData

    def aprioriGen(self, Lk, k):
        """
        #组合，向上合并
        :param Lk: 频繁项集列表 Lk
        :param k: 项集元素个数 k
        :return: 
        """
        retList = []
        lenLk = len(Lk)
        for i in range(lenLk):
            for j in range(i+1, lenLk): #两两组合遍历
                L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
                L1.sort(); L2.sort()
                if L1==L2: #若两个集合的前k-2个项相同时,则将两个集合合并
                    retList.append(Lk[i] | Lk[j]) #set union
        return retList

    def process(self, dataSet, minSupport = 0.5):
        """
        
        :param dataSet: list(list()), 输入数据
        :param minSupport: float，最小支持度
        :return: 
        """
        C1 = self.createC1(dataSet)
        D = list(map(set, dataSet)) #python3
        L1, supportData = self.scanD(D, C1, minSupport)#单项最小支持度判断 0.5，生成L1
        L = [L1]
        k = 2
        while (len(L[k-2]) > 0):#创建包含更大项集的更大列表,直到下一个大的项集为空
            Ck = self.aprioriGen(L[k-2], k)#Ck
            Lk, supK = self.scanD(D, Ck, minSupport)#get Lk
            supportData.update(supK)
            L.append(Lk)
            k += 1
        return L, supportData

    def generateRules(self, L, supportData, minConf=0.7):
        #频繁项集列表、包含那些频繁项集支持数据的字典、最小可信度阈值
        bigRuleList = [] #存储所有的关联规则
        for i in range(1, len(L)):  #只获取有两个或者更多集合的项目，从1,即第二个元素开始，L[0]是单个元素的
            # 两个及以上的才可能有关联一说，单个元素的项集不存在关联问题
            for freqSet in L[i]:
                H1 = [frozenset([item]) for item in freqSet]
                #该函数遍历L中的每一个频繁项集并对每个频繁项集创建只包含单个元素集合的列表H1
                if (i > 1):
                #如果频繁项集元素数目超过2,那么会考虑对它做进一步的合并
                    self.rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
                else:#第一层时，后件数为1
                    self.calcConf(freqSet, H1, supportData, bigRuleList, minConf)# 调用函数2
        return bigRuleList

    def calcConf(self, freqSet, H, supportData, brl, minConf=0.7):
        # 针对项集中只有两个元素时，计算可信度
        # 返回一个满足最小可信度要求的规则列表
        prunedH = []
        for conseq in H:
            # 后件，遍历 H中的所有项集并计算它们的可信度值
            # 可信度计算，结合支持度数据
            if freqSet not in supportData or freqSet-conseq not in supportData:
                # TODO 一些数据可能不在支持度里面，这些数据一律不要了
                continue
            conf = supportData[freqSet]/supportData[freqSet-conseq]
            if conf >= minConf:
                if self.print_detail:
                    print(freqSet-conseq, '-->', conseq, 'conf:', conf)
                # 如果某条规则满足最小可信度值,那么将这些规则输出到屏幕显示
                # 添加到规则里，brl 是前面通过检查的 bigRuleList
                brl.append((freqSet-conseq, conseq, conf))
                # 同样需要放入列表到后面检查
                prunedH.append(conseq)
        return prunedH

    def rulesFromConseq(self, freqSet, H, supportData, brl, minConf=0.7):
        #参数:一个是频繁项集,另一个是可以出现在规则右部的元素列表 H
        m = len(H[0])
        if (len(freqSet) > (m + 1)): #频繁项集元素数目大于单个集合的元素数
            Hmp1 = self.aprioriGen(H, m+1)#存在不同顺序、元素相同的集合，合并具有相同部分的集合
            Hmp1 = self.calcConf(freqSet, Hmp1, supportData, brl, minConf)#计算可信度
            if (len(Hmp1) > 1):
            #满足最小可信度要求的规则列表多于1,则递归来判断是否可以进一步组合这些规则
                self.rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)


if __name__ == '__main__':

    dataSet = [['豆奶', '苹果'],
               ['豆奶', '莴苣'],
               ['莴苣', '尿布', '葡萄酒', '甜菜'],
               ['豆奶', '尿布', '葡萄酒', '橙汁'],
               ['莴苣', '豆奶', '尿布', '葡萄酒'],
               ['莴苣', '豆奶', '尿布', '橙汁']]

    processor = Apriori()
    L, suppData = processor.process(dataSet, 0.5)

    rules = processor.generateRules(L, suppData, 0.6)
    print(L)
    print("----")
    print(suppData)
    print("-----")
    print(rules)
