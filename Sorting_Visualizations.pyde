w, h = 1920, 1080

element_count = 32

# Colors for the gradient
colors = [(250, 20, 20), (0, 225, 225), (0, 0, 0)]

circle_size = 5
stroke_weight = 1


# Returns the color between two colors at a specific step in the gradient
def get_gradient_point(color_one, color_two, step, max_steps):
    s = float(step) / max_steps

    r = (color_two[0] - color_one[0]) * s + color_one[0]
    if r < 0:
        r += 255.0

    g = (color_two[1] - color_one[1]) * s + color_one[1]
    if g < 0:
        g += 255.0

    b = (color_two[2] - color_one[2]) * s + color_one[2]
    if b < 0:
        b += 255.0

    return r, g, b


def shuffle(list_to_shuffle):
    v = list(list_to_shuffle)

    print(v)
    shuffled = []
    len_v = len(v)
    for e in range(len_v, 0, -1):
        shuffled.append(list_to_shuffle.pop(int(random(e))))
    return shuffled


def sorted(list_to_check):
    for i in range(1, len(list_to_check)):
        if list_to_check[i - 1] <= list_to_check[i]:
            return False
    return True


def bogo_sort(v):
    stages = [v]
    next_stage = v
    while not sorted(next_stage):
        next_stage = list(stages[-1])

        next_stage = shuffle(next_stage)

        stages.append(next_stage)

    return stages


def bubble_sort(v):
    stages = [v]
    next_stage = v
    while not sorted(next_stage):
        next_stage = list(stages[-1])
        for i in range(len(next_stage) - 1):
            if next_stage[i] > next_stage[i + 1]:
                t = next_stage[i]
                next_stage[i] = next_stage[i + 1]
                next_stage[i + 1] = t

        stages.append(v)

    return stages


def quick_sort_helper(v):
    stages = [list(v)]
        
    def partition(a, lo, hi):
        pivot = a[lo + (hi - lo) / 2]
        i = lo
        j = hi
        while True:
            while a[i] < pivot:
                i += 1
                
            while a[j] > pivot:
                j -= 1
                
            if i >= j:
                return j
            
            a[i], a[j] = a[j], a[i]
            stages.append(list(a))
            
    def quick_sort(a, lo, hi):
        if lo < hi:
            p = partition(a, lo, hi)
            quick_sort(a, lo, p)
            quick_sort(a, p + 1, hi)

    quick_sort(v, 0, len(v) - 1)
    return stages

def visualize(stages):
    colors.extend(((i * 255 / element_count, 20, 60) for i in range(element_count)))

    stages_copy = [stages[0]]
    stages_copy.extend(stages)
    stages_copy.append(stages[-1])
    stages = stages_copy

    column_sep = float(w) / (len(stages) + 1)
    row_sep = float(h) / (element_count + 1)

    for e in range(element_count):
        c = get_gradient_point(colors[0], colors[1], e, element_count)
        stroke(*c)
        beginShape()
        for s, partially_sorted in enumerate(stages):
            x = column_sep + s * column_sep
            y = row_sep + partially_sorted.index(e) * row_sep

            curveVertex(x, y)

            fill(*c)
            circle(x, y, circle_size)

        noFill()
        endShape()


def setup():
    size(w, h)
    pixelDensity(2)
    background(*colors[2])
    strokeWeight(stroke_weight)

    v = list(range(element_count))

    visualize(quick_sort_helper(shuffle(v)))

    save_seed = str(int(random(10000)))
    print(save_seed)
    save('Examples/QuickSort/%s.png' % save_seed)
