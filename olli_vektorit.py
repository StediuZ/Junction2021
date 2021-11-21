def make_vectors(X_max,Y_max,interval):
    import random

    #X_max = 500
    #Y_max = 500
    #interval = 10
    vectors_times = {}
    hours = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
    for hour in hours:
        vectors=[]
        for x in range(0,X_max,interval):
            for y in range(0,Y_max,interval):
                vectors.append([x,y,random.randrange(0,200,1),random.randrange(0,359,1)])
        vectors_times[hour] = vectors

    return vectors_times

def main():
    make_vectors(500,500,100)