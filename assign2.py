# Task 1
def get_side(px, py):
    lx1, ly1 = -3, 4
    lx2, ly2 = 4, -3
    cross = (lx2 - lx1) * (py - ly1) - (ly2 - ly1) * (px -lx1)
    if cross > 0:
        return 1
    elif cross < 0:
        return -1
    else:
        return 0

def func1(name):
    characters = {
        "哆啦Ａ夢": (0, 0),
        "大雄": (2, -1),
        "靜香": (-2, 2),
        "胖虎": (3, 1),
        "小夫": (-1, -2),
        "哆啦美": (-3, 3),
    }
    x1, y1 = characters[name]

    distance_map = {}

    for other_name, (x2, y2) in characters.items():
        if other_name == name:
            continue
        distance = abs(x1 - x2) + abs(y1 - y2)
        if get_side(x1, y1) != get_side(x2, y2):
            distance += 2
        distance_map[other_name] = distance

    max_dist = max(distance_map.values())
    min_dist = min(distance_map.values())

    farthest = []
    for char_name, dist in distance_map.items():
        if dist == max_dist:
            farthest.append(char_name)

    closest = []
    for char_name, dist in distance_map.items():
        if dist == min_dist:
            closest.append(char_name)

    print(name + "-最遠：" + "、".join(farthest) + " (距離："+ str(max_dist) + ")")
    print(name + "-最近：" + "、".join(closest) + " (距離："+ str(min_dist) + ")")

func1("哆啦Ａ夢")
func1("大雄")
func1("靜香")
func1("胖虎")
func1("小夫")
func1("哆啦美")


# Task 2
bookings = {}

def is_available(service_name, start, end):
    if service_name not in bookings:
        return True
    for booking in bookings[service_name]:
        a, b = booking
        if a < end and start < b:
            return False
    return True


def func2(ss, start, end, criteria):
    if ">=" in criteria:
        op = ">="
    elif "<=" in criteria:
        op = "<="
    else:
        op = "="

    parts = criteria.split(op)
    field = parts[0]
    value = parts[1]

    available=[]
    for s in ss:
        if is_available(s["name"], start , end):
            available.append(s)
        
    
    if op == "=":
        result = None
        for s in available:
            if s[field] == value:
                result = s
                break
    else:
        value = float(value)
        result = None
        for s in available:
            if op == ">=" and s[field] >= value:
                if result is None or s[field] < result[field]:
                        result = s
            elif op == "<=" and s[field] <= value:
                if result is None or s[field] > result[field]:
                        result = s
    
    if result:
        print(result["name"])
        if result["name"] not in bookings:
            bookings[result["name"]] = []
        bookings[result["name"]].append((start, end))
    else:
        print("Sorry")

services=[
    {"name":"S1", "r":4.5, "c":1000},
    {"name":"S2", "r":3, "c":1200},
    {"name":"S3", "r":3.8, "c":800}
]

func2(services, 15, 17, "c>=800") # S3
func2(services, 11, 13, "r<=4") # S3
func2(services, 10, 12, "name=S3") # Sorry
func2(services, 15, 18, "r>=4.5") # S1
func2(services, 16, 18, "r>=4") # Sorry
func2(services, 13, 17, "name=S1") # Sorry
func2(services, 8, 9, "c<=1500") # S2


# Task 3
def func3(index):
    start = 25
    gaps = [-2, -3, 1, 2]
    steps = index

    groups = steps // 4
    remainder = steps % 4

    remainder_sum = sum(gaps[:remainder])
    print(start + groups * (-2) + remainder_sum)

func3(1)  # print 23
func3(5)  # print 21
func3(10) # print 16
func3(30) # print 6


# Task 4
def func4(sp, stat, n):
    candidate_cars = []
    for index in range(len(sp)):
        if stat[index] == '0':
            candidate_cars.append(index)

    fitted_cars = []
    for index in candidate_cars:
        if sp[index] >= n:
            fitted_cars.append(index)
    
    if fitted_cars ==[]:
        best = candidate_cars[0]
        for index in candidate_cars:
            if sp[index] > sp[best]:
                best = index
    else:
        best = fitted_cars[0]
        for index in fitted_cars:
            if sp[index] - n < sp[best] - n:
                best = index

    print(best)

func4([3, 1, 5, 4, 3, 2], "101000", 2) # print 5
func4([1, 0, 5, 1, 3], "10100", 4)      # print 4
func4([4, 6, 5, 8], "1000", 4)           # print 2
