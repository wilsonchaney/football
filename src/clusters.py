from sklearn.cluster import KMeans

class PlayerClusters(KMeans):

    def __init__(self,n_clusters,stat_list):
        super(PlayerClusters, self).__init__(n_clusters)
        self.stat_list = stat_list

    def cluster_QBs(self,players,showChart=False):
        global stat_list
        data = []
        names = []
        for p in players:
            pt = [p.get_passing_stat("career",stat) for stat in self.stat_list]
            data.append(pt)
            names.append(p.name)

        super(PlayerClusters,self).fit(data)

        cluster_lists = {}
        for i in range(0,self.n_clusters):
            cluster_lists[i] = []

        for i,cluster in enumerate(self.labels_):
            cluster_lists[cluster].append(names[i])
        for c in cluster_lists:
            print "Cluster #"+str(c)+":",','.join(cluster_lists[c])

    def attempt_cluster_ranks(self):
        pass
