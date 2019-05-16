'''Name: Amit Rokade

   Problem 1: Solving Maze using A* Algorithm
   (Note: THe following program runs with turtle graphics and runs slowly for mazes as turtle draws every cell
   , to turn them on comment lines 118-124 , 307-317)
'''


import turtle,sys,math,random,time


grid=[]
with open("big_maze") as file:
    for line in file:
        grid.append(line.split())


cellHeight=20
cellWidth=20
rows=len(grid)
# print("Rows",rows)
cols=len(grid[0])
# print("Columns",cols)
goal=(rows-1,cols-1)
start=(0,0)

print("NOTE: TURTLE GRAPHICS ARE OFF BY DEFAULT, REFER COMMENTS TO TURN THEM ON...")
print()
print()

heuristic= [[0 for x in range(cols)] for y in range(rows)]

f= [[0 for x in range(cols)] for y in range(rows)]

g= [[0 for x in range(cols)] for y in range(rows)]

visited_list=[]
to_be_explored_list=[]
neighbors={}
path_dict={}
path=[]
startg=0
t=turtle.Turtle()
# t.goto(-600,600)
t.hideturtle()
t.speed(0)
t._tracer(False)
n=[1,2,3,4]
states_traversed={}
depth=0


def main(rows,cols,heuristic,f,g,visited_list,to_be_explored_list,neighbors,path_dict,t,n,start,states_traversed,depth):
    '''A* algorithm is run on different heuristics'''
    for number in n:
        list = ["Euclidean Heuristic", "Manhattan Heuristic", "Random Heuristic", "Zero Heuristic"]
        print("HEURISTIC :",list[number-1])

        t.screen.title(list[number-1])
        start_time=time.time()
        color_grid(rows,cols,heuristic,neighbors,number)
        # print("HEURISTICS")
        for x in range(rows):
            for y in range(cols):
                pass
                # print(heuristic[x][y])
                # print(f[x][y])
        # print("Printing neighbors")
        # print(neighbors)

        to_be_explored_list.append(start)
        draw_filled_rect(start[0],start[1],"blue")
        states_traversed[start]=1
        path_found=False
        path_found=search_min_path(heuristic,f,g,visited_list,to_be_explored_list,neighbors,path_dict,number,start,states_traversed,depth)

        end_time=time.time()
        print("Time taken is: ",end_time-start_time)
        print("Maze Path ",path_found)

        rows = len(grid)
        print("Rows", rows)
        cols = len(grid[0])
        print("Columns", cols)
        goal = (rows - 1, cols - 1)
        start = (0, 0)

        heuristic = [[0 for x in range(cols)] for y in range(rows)]

        f = [[0 for x in range(cols)] for y in range(rows)]

        g = [[0 for x in range(cols)] for y in range(rows)]

        visited_list = []
        to_be_explored_list = []
        neighbors = {}
        path_dict = {}
        t = turtle.Turtle()
        # t.goto(-600,600)
        t.hideturtle()
        t.speed(0)
        states_traversed={}
        depth=0
        t._tracer(False)
        print("-----------------------------------")



    turtle.mainloop()

def color_grid(rows,cols,heuristic,neighbors,number):
    '''Used to draw the matrix in turtle and add neighbors for every cell, adjacent cells with walls are not added'''
    for x in range(rows):
        for y in range(cols):
            # print(x,y)
            add_neighbors(x,y,rows,cols,neighbors)
            heuristic[x][y]=compute_heuristic(x,y,number)
            # if(grid[x][y]=='0'):
            #     draw_filled_rect(x,y,"white")
            # elif(grid[x][y]=='1'):
            #     draw_filled_rect(x,y,"black")
            # else:
            #     draw_filled_rect(x,y,"green")

def search_min_path(heuristic,f,g,visited_list,to_be_explored_list,neighbors,path_dict,number,start,states_traversed,depth):
    '''Used to backtrack and calculate minimum path'''
    while (len(to_be_explored_list) > 0):
        parent = to_be_explored_list[0]
        min_f_cell = to_be_explored_list[0]
        min_f_val = f[to_be_explored_list[0][0]][to_be_explored_list[0][1]]

        # finding cell with minimum f(n) in open list
        for i in range(len(to_be_explored_list)):

            x = to_be_explored_list[i][0]
            y = to_be_explored_list[i][1]
            temp_val = f[x][y]
            if temp_val <= min_f_val:
                min_f_val = temp_val
                min_f_cell = to_be_explored_list[i]
            if min_f_cell == goal:
                # print("End reached")
                temp = goal
                draw_filled_rect(goal[0],goal[1],"green")
                depth+=1
                while (temp != start):
                    val = path_dict[temp]
                    path.append(val)
                    temp = path_dict[temp]
                    draw_filled_rect(val[0],val[1],"green")
                    depth+=1
                # print(path)
                print("Depth:",depth)
                print("States Traversed:", len(states_traversed))
                print("Branching Factor:",math.e**(math.log(len(states_traversed))/depth))
                return True
        to_be_explored_list.remove(min_f_cell)
        visited_list.append(min_f_cell)

        # find minimum from all the neighbors


        for neighbor in neighbors[min_f_cell]:
            '''' if neighbor is not in closed list, only then check for it'''
            if neighbor not in visited_list:

                ''' first calculating temporary g value'''
                neighbor_curr_g = g[x][y] + 10;


                if neighbor in to_be_explored_list:
                    ''' If neighbor already in open list and then look for the better g value'''
                    if (neighbor_curr_g < g[neighbor[0]][neighbor[1]]):
                        # print("Updating current neighbor from ",g[neighbor[0]][neighbor[1]]," to ",neighbor_curr_g)
                        g[neighbor[0]][neighbor[1]] = neighbor_curr_g


                        ''' Adding child -> parent to dictionary'''
                        path_dict[neighbor] = (min_f_cell[0], min_f_cell[1])
                else:
                    ''' New un-explored neighbor found ; now setting its g value and adding it to open list
                     print("Setting the g value of neighbor to be ","",neighbor_curr_g)'''
                    g[neighbor[0]][neighbor[1]] = neighbor_curr_g
                    to_be_explored_list.append(neighbor)
                    draw_filled_rect(neighbor[0], neighbor[1], "blue")
                    toAdd=(neighbor[0],neighbor[1])
                    states_traversed[toAdd]=1

                    ''' Adding child -> parent to dictionary'''
                    path_dict[neighbor] = (min_f_cell[0], min_f_cell[1])

                '''Updating heuristic value'''
                heuristic[neighbor[0]][neighbor[1]]=compute_heuristic(neighbor[0],neighbor[1],number)
                '''Updating f value'''
                f[neighbor[0]][neighbor[1]] = g[neighbor[0]][neighbor[1]] + heuristic[neighbor[0]][neighbor[1]]
                '''print("F value for ",neighbor[0],neighbor[1]," is ",f[neighbor[0]][neighbor[1]])'''


            else:
                # Cell skipped
                pass

def calc_gn(x,y):
    return g[x][y]+10

def compute_heuristic(x,y,number):
    '''EUCLEDIAN,MANHATTAN,RANDOM OR ZERO HEURISTICS'''

    if number ==1:
        '''EUCLEDIAN'''
        return math.sqrt((goal[0]-x)**2)+((goal[1]-y)**2)

    elif number ==2:
        '''Manhattan'''
        return (abs(goal[0]-x))*10+(abs(goal[1]-y))*10

    elif number ==3:
        '''Random'''
        return random.randint(1,200)

    else:
        '''Zero'''
        return 0


def add_neighbors(x,y,rows,cols,neighbors):
    '''Adding neighbors for the given cell'''
    curr_key=(x,y)
    list_of_neighbors=[]

    if (y<cols-1):
        if grid[x][y+1]!='1':
            list_of_neighbors.append((x,y+1))
    if (x<rows-1):
        if grid[x+1][y]!='1':
            list_of_neighbors.append((x+1, y))
    if(y>0):
        if grid[x][y-1]!='1':
            list_of_neighbors.append((x,y-1))
    if (x>0) :
        if grid[x-1][y]!='1':
            list_of_neighbors.append((x-1,y))

    copy=[]
    for neighbor in list_of_neighbors:

        if curr_key in neighbors:
            neighbors.setdefault(curr_key,[]).append(neighbor)

        else:
            neighbors[curr_key]=[neighbor]
            copy.extend(neighbors[curr_key])




def draw_filled_rect(x,y,color):
    '''Drawing cell using turtle'''
    pass
    # t.up()
    #
    # t.goto(y*cellWidth-400,-x*cellHeight+400)
    # t.down()
    # t.begin_fill()
    # t.fillcolor(color)
    # for i in range(4):
    #     t.forward(cellWidth)
    #     t.left(90)
    # t.end_fill()
    # t.up()



if __name__=="__main__":

    main(rows,cols,heuristic,f,g,visited_list,to_be_explored_list,neighbors,path_dict,t,n,start,states_traversed,depth)


