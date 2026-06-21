// Task 1
function get_side(px, py) {
    const lx1 = -3, ly1 = 4
    const lx2 = 4, ly2 = -3
    const cross = (lx2-lx1) * (py - ly1) - (ly2 -ly1) * (px-lx1)
    if (cross > 0) {
        return 1
    }else if (cross < 0) {
        return -1
    }else {
        return 0
    }
}

function func1(name) {
    const characters = {
        "哆啦Ａ夢": [0, 0],
        "大雄": [2, -1],
        "靜香": [-2, 2],
        "胖虎": [3, 1],
        "小夫": [-1 ,-2],
        "哆啦美": [-3, 3],
    }

    const [x1, y1] = characters[name]

    const distance_map = {}

    for (const [other_name, [x2, y2]] of Object.entries(characters)) {
        if (other_name === name) {
            continue
        }
        let distance = Math.abs(x1 - x2) + Math.abs(y1 - y2)
        if (get_side(x1, y1) !== get_side(x2, y2)) {
            distance += 2
        }
        distance_map[other_name] = distance
    }

    const dist_values = Object.values(distance_map)
    const max_dist = Math.max(...dist_values)
    const min_dist = Math.min(...dist_values)

    const farthest = []
    const closest = []

    for (const [char_name, dist] of Object.entries(distance_map)) {
        if (dist === max_dist) {
            farthest.push(char_name)
        }

        if (dist === min_dist) {
            closest.push(char_name)
        }
    }

    console.log(name + "-最遠：" + farthest.join("、") + " (距離：" + max_dist + ")")
    console.log(name + "-最近：" + closest.join("、") + " (距離：" + min_dist + ")")
}

func1("哆啦Ａ夢")
func1("大雄")
func1("靜香")
func1("胖虎")
func1("小夫")
func1("哆啦美")


// Task 2
let bookings = {}

function isAvailable(service_name, start, end) {
    if (!(service_name in bookings)) {
        return true;
    }
    for (let booking of bookings[service_name]) {
        let a = booking[0];
        let b = booking[1];
        if (a < end && start < b) {
            return false;
        }
    }
    return true;
}

function func2(ss, start, end, criteria) {
    let op;
    if (criteria.includes(">=")) {
        op = ">=";
    } else if (criteria.includes("<=")) {
        op = "<=";
    } else {
        op = "=";
    }

    let parts = criteria.split(op);
    let field = parts[0];
    let value = parts[1];

    let available = [];
    for (let s of ss) {
        if (isAvailable(s["name"], start, end)) {
            available.push(s);
        }
    }

   let result = null;
   if (op === "=") {
        for (let s of available) {
            if (s[field] === value) {
                result = s;
                break;
            }
        }
   } else {
        value = parseFloat(value);
        for (let s of available) {
            if (op === ">=" && s[field] >= value) {
                if (result === null || s[field] < result[field]) {
                    result = s;
                }
            } else if (op === "<=" && s[field] <= value) {
                if (result === null || s[field] > result[field]) {
                    result = s;
                }
            }
        }
   }

   if (result) {
    console.log(result["name"]);
    if (!(result["name"] in bookings)) {
        bookings[result["name"]] = [];
    }
    bookings[result["name"]].push([start, end]);
   } else {
    console.log("Sorry")
   }
}

const services=[
    {"name":"S1", "r":4.5, "c":1000},
    {"name":"S2", "r":3, "c":1200},
    {"name":"S3", "r":3.8, "c":800}
];

func2(services, 15, 17, "c>=800"); // S3
func2(services, 11, 13, "r<=4"); // S3
func2(services, 10, 12, "name=S3"); // Sorry
func2(services, 15, 18, "r>=4.5"); // S1
func2(services, 16, 18, "r>=4"); // Sorry
func2(services, 13, 17, "name=S1"); // Sorry
func2(services, 8, 9, "c<=1500"); // S2


// Task 3
function func3(index){
    let steps = index;
    let start = 25;
    let gaps = [-2, -3, 1, 2];
    let groups = Math.floor(steps/4);
    let remainder = steps % 4;

    let remainderSum = gaps.slice(0, remainder).reduce((a, b) => a + b, 0)

    console.log(start + groups * (-2) + remainderSum)
}

func3(1);  // print 23
func3(5);  // print 21
func3(10); // print 16
func3(30); // print 6


// Task 4
function func4(sp, stat, n){
    let candidateCars = [];
        for (let index = 0; index < sp.length; index++) {
            if (stat[index] === '0') {
              candidateCars.push(index)  
            }
        }
    
    let fittedCars = [];
        for (let index = 0; index < candidateCars.length; index++) {
            if (sp[candidateCars[index]] >= n) {
            fittedCars.push(candidateCars[index])
        }
    }    
        if (fittedCars.length === 0) {
            let best = candidateCars[0];
            for (let index = 0; index < candidateCars.length; index++) {
                if (sp[candidateCars[index]] > sp[best]) {
                    best = candidateCars[index];
                }
            }
            console.log(best)
        } else {
            let best = fittedCars[0];
            for (let index = 0; index < fittedCars.length; index++) {
                if (sp[fittedCars[index]] - n < sp[best] - n) {
                    best = fittedCars[index]
                }
            }
            console.log(best)
        }
}

func4([3, 1, 5, 4, 3, 2], "101000", 2); // print 5
func4([1, 0, 5, 1, 3], "10100", 4);      // print 4
func4([4, 6, 5, 8], "1000", 4);           // print 2
