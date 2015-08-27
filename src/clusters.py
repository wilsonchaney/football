from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from math import atan,pi

from datastorage import get_player_list,get_player,player

# Set these before running
STATS_LIST = ["pass_int_perc","pass_yds_per_att","pass_cmp_perc"] # Which stats are used for clustering
NUM_CLUSTERS_RANGE = [4,7] # inclusive

class PlayerClusters(KMeans):
    cluster_colors = ["#ff0000","#00ff00","#0000ff","#ff6a00","#9900FF"]

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

        scaled_data = self.get_scaled_data(data)

        super(PlayerClusters,self).fit(scaled_data)

        self.variance = self.get_variance(scaled_data)

        cluster_lists = {}
        for i in range(0,self.n_clusters):
            cluster_lists[i] = []

        for i,cluster in enumerate(self.labels_):
            cluster_lists[cluster].append(names[i])
        for c in cluster_lists:
            pass
            # print "Cluster #"+str(c)+":",','.join(cluster_lists[c])

        if showChart and len(self.stat_list) is 2:
            x_vals = [pt[0] for pt in data]
            y_vals = [pt[1] for pt in data]
            colors = [self.cluster_colors[i % 5] for i in self.labels_]
            rad = [30]*len(data)
            plt.scatter(x=x_vals,y=y_vals,c=colors,s=rad)
            plt.xlabel(self.stat_list[0])
            plt.ylabel(self.stat_list[1])
            plt.show()


    def get_variance(self,scaled_data):
        total = 0
        for i in range(0,len(scaled_data)):
            cluster_index = self.labels_[i]
            centroid = self.cluster_centers_[cluster_index]
            total += self.sq_dist(scaled_data[i],centroid)
        variance = total / len(scaled_data)
        return variance

    def sq_dist(self,pt1,pt2):
        if len(pt1) != len(pt2):
            raise Exception("Points have different dimensions!")
        total = 0
        for i in range(0,len(pt1)):
            total += (pt1[i]-pt2[i])**2
        return total
            

    def get_scaled_data(self,data):
        dim_extrema = []
        for i in range(0,len(self.stat_list)):
            dim_data = [x[i] for x in data]
            dim_extrema.append((min(dim_data),max(dim_data)))
            #print self.stat_list[i],(min(dim_data),max(dim_data))

        scaled_data = []
        for pt in data:
            scaled_pt = []
            for i in range(0,len(self.stat_list)):
                extrema = dim_extrema[i]
                new_val = float(pt[i]-extrema[0])/(extrema[1]-extrema[0])
                #print self.stat_list[i],pt[i],"=>",new_val
                #raw_input()
                scaled_pt.append(new_val)
            scaled_data.append(scaled_pt)
        return scaled_data

# Returns angle between *head-to-tail* segments with the given slopes
def get_angle(slope1,slope2):
    return 180-atan((slope1-slope2)/(1+slope1*slope2))*(180/pi)


# Checks for "elbow"
def determine_correct_k(data):
    slopes = [data[i][1]-data[i-1][1] for i in range(1,len(data))]
    angles = [get_angle(slopes[i],slopes[i-1]) for i in range(1,len(slopes))]

    val, idx = min((val, idx+1) for (idx, val) in enumerate(angles))

    print "Calculated k value:",data[idx][0]

players = get_player_list("datastorage/data/player_list.json")
with open("players.dat","r") as names_file:
    names = [name.strip() for name in names_file.readlines()]
players = [player.PassingPlayer(get_player(players,x,"QB")) for x in names]
for p in players:
    # print "Reading",p.name
    p.read_page()

x_vals = []
y_vals = []
data = []
for k in range(NUM_CLUSTERS_RANGE[0]-1,NUM_CLUSTERS_RANGE[1]+2):
    clusters = PlayerClusters(k,STATS_LIST)
    clusters.cluster_QBs(players,False)
    x_vals.append(k)
    y_vals.append(clusters.variance)
    data.append([k,clusters.variance])
plt.scatter(x_vals,y_vals)
determine_correct_k(data)
plt.show()