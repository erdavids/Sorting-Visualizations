import javax.swing.JOptionPane as JOptionPane

w, h = 1050, 750

element_count = 8
stages = []

# Colors for the gradient 
colors = [(250, 20, 20), (0, 225, 225), (0, 0, 0)]

circle_size = 5
stroke_weight = 3

# Repeats the unsorted / sorted stages
connect_everything = True

# Returns the color between two colors at a specific step in the gradient
def get_gradient_point(color_one, color_two, step, max_steps):
    s = (float(step)/max_steps)
    
    r = (color_two[0] - color_one[0]) * s + color_one[0]
    if (r < 0):
        r += 255.0
        
    g = (color_two[1] - color_one[1]) * s + color_one[1]
    if (g < 0):
        g += 255.0
        
    b = (color_two[2] - color_one[2]) * s + color_one[2]
    if (b < 0):
        b += 255.0
    
    return (r, g, b)

def shuffle(l):
    v = list(l)

    shuffled = []
    for e in range(element_count):
        shuffled.append(v.pop(int(random(len(v)))))
        
    return shuffled


def partition(v, low, high):
    pivot = v[high]
    
    index = low - 1
    
    for j in range(low, high):
        if (v[j] < pivot):
            index += 1
            
            t = v[index]
            v[index] = v[j]
            v[j] = t
        
    t = v[index + 1]
    v[index + 1] = v[high]
    v[high] = t
    
    return (index + 1)
            


def sorted(l):
    for i in range(len(l) - 1):
        if l[i] > l[i + 1]:
            return False
    return True

def gnome_sort(v):
    stages.append(v[:])
    index = 0
    while index != len(v):
        next_stage = stages[-1][:]
        if (index == 0):
            index += 1
        elif (next_stage[index] < next_stage[index - 1]):
            t = next_stage[index]
            next_stage[index] = next_stage[index - 1]
            next_stage[index - 1] = t
            
            index -= 1
        else:
            index += 1
            
        stages.append(next_stage)
    
#shoutout to https://www.geeksforgeeks.org/python-program-for-radix-sort/
#for providing me (Riedler) with the template for counting and radix sort.
def counting_sort(v,n):
    l=len(v) 
    out=[0]*l
    count=[0]*10
    
    for i in range(0,l):
        count[(v[i]/n)%10]+=1
    
    for i in range(1,10): 
        count[i] += count[i-1]
    
    i = l-1
    while i>=0: 
        index = (v[i]/n) 
        out[ count[ (index)%10 ] - 1] = v[i] 
        count[ (index)%10 ] -= 1
        i -= 1
    
    i = 0
    for i in range(0,l): 
        v[i] = out[i] 
    
def radix_sort(v):
    stages.append(v[:])
    d = max(v)
    n=1
    while d/n>0:
        counting_sort(v,n)
        stages.append(v[:])
        n*=10

def merge_sort(v):
    
    stages.append(v[:])
    
    if len(v) > 1:
        mid = len(v)/2
        L = v[:mid]
        R = v[mid:]
        
        merge_sort(L)
        merge_sort(R)
        
        i = j = k = 0
        
        while (i < len(L) and j < len(R)):
            if L[i] < R[j]:
                v[k] = L[i]
                i += 1
            else:
                v[k] = R[j]
                j += 1
            k += 1
        
        while i < len(L):
            v[k] = L[i]
            i += 1
            k += 1
            
        while j < len(R):
            v[k] = R[j]
            j += 1
            k += 1

    stages.append(v[:])

def quick_sort(v, low, high):
    stages.append(v[:])
    
    if (low < high):
        pivot = partition(v, low, high)
        
        quick_sort(v, low, pivot - 1)
        quick_sort(v, pivot + 1, high)

def bogo_sort(v):
    stages.append(v)
    
    while True:
        next_stage = list(stages[-1])
        
        next_stage = shuffle(next_stage)
        
        stages.append(next_stage)
        
        if (sorted(next_stage)):
            break
        
    return stages

def insertion_sort(v):
    stages.append(v)
    
    index = 1
    while index < len(v):
        next_stage = list(stages[-1])
        mov = index
        while (mov > 0 and next_stage[mov - 1] > next_stage[mov]):
            t = next_stage[mov]
            next_stage[mov] = next_stage[mov - 1]
            next_stage[mov - 1] = t
        
            mov -= 1
        
        stages.append(next_stage)
        index += 1
    
    
    return stages

def bubble_sort(v):
    stages.append(v)
    
    while True:
        change = False
        next_stage = list(stages[-1])
        for i in range(len(next_stage) - 1):
            if (next_stage[i] > next_stage[i + 1]):
                t = next_stage[i]
                next_stage[i] = next_stage[i + 1]
                next_stage[i + 1] = t
                
                
                change = True
            
        stages.append(next_stage)
            
        if (sorted(next_stage)):
            break
    return stages

def visualize():
    for i in range(element_count):
        colors.append((i * 255/element_count, 20, 60))
        
    if (connect_everything):
        stages.insert(0, stages[0][:])
        stages.append(stages[-1][:])
    
        
    column_sep = float(w) / (len(stages) + 1)
    row_sep = float(h) / (element_count + 1)
    
    for e in range(element_count):
        c = get_gradient_point(colors[0], colors[1], e, element_count)
        stroke(c[0], c[1], c[2])
        beginShape()
        for s in range(len(stages)):
            if (e in stages[s]):
                x = column_sep + s * column_sep
                y = row_sep + stages[s].index(e) * row_sep
        
                curveVertex(x, y)
                
    
                fill(c[0], c[1], c[2])
                circle(x, y, circle_size)
        
        noFill()
        endShape()
    
def setup():
    size(w, h)
    pixelDensity(2)
    background(colors[2][0], colors[2][1], colors[2][2])
    strokeWeight(stroke_weight)

    v = []
    for e in range(element_count):
        v.append(e)
        
    opts={"Bogosort":bogo_sort,"Gnome Sort":gnome_sort,"Bubble Sort":bubble_sort,"Merge Sort":merge_sort,"Insertion Sort":insertion_sort,"Radix":radix_sort}
    opt=JOptionPane.showOptionDialog(
        None,
        "Choose a sorting algorithm",
        "Choosening",
        JOptionPane.DEFAULT_OPTION,
        JOptionPane.WARNING_MESSAGE,
        None,
        opts.keys(),
        opts.keys()[0])
    opts.values()[opt](shuffle(v))
    
    visualize()

    
    save_seed = str(int(random(10000)))
    save('Examples/Gnome/%s.png' % save_seed)
