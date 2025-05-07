import datetime

print(datetime.datetime(2005,2,4))
t1 = datetime.datetime.now()
print(t1)
t1 = t1.strftime("%Y/%m/%d %H:%M:%S")
print(t1)

n1 = 0.2

if isinstance(n1, float):
    print("YEs")
