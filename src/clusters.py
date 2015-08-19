from sklearn.cluster import KMeans

# Stats to use for clustering
stat_list = ["pass_cmp_perc","pass_td_perc","pass_int_perc","pass_yds_per_g"]


def cluster_QBs(players):
    global stat_list
    data = []
    names = []
    for p in players:
        pt = [p.get_passing_stat("career",stat) for stat in stat_list]
        data.append(pt)
        names.append(p.name)
    k = KMeans(n_clusters=4)
    k.fit(data)

    cluster_lists = {}
    for i in range(0,k.n_clusters):
        cluster_lists[i] = []

    for i,cluster in enumerate(k.labels_):
        cluster_lists[cluster].append(names[i])
    for c in cluster_lists:
        print "Cluster #"+str(c)+":",','.join(cluster_lists[c])