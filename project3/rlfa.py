import csp
import sys


#------------------ Text Parsing ------------------
def varfile(string):
    # return a list which contains the variables ID and a dictionary with the variable's ID as key and the domain's ID as item
    f=open("rlfap/"+string, "r")
    text=f.readlines()
    var_domain={}
    variables=[]
    for line in text[1:]:
        str=format(line.strip("\n"))
        x,y=str.split(" ")
        variables.append(int(x))
        var_domain[int(x)]=int(y)

    f.close()

    return variables,var_domain

def domfile(string,variables,var_domain):
    # return a dictionary with variable's ID as key and as item a list which contains all the possibles values that can take from the corresponding domain for this variable
    f=open("rlfap/"+string, "r")
    text=f.readlines()
    domains={}
    total={} # dictionary with domain's ID as key and as item a list which contains the domain's values
    for line in text[1:]:
        line=line.strip("\n")
        str=line.split(" ")
        str=[int(i) for i in str]
        for id in str[:1]:
            total[id]=str[2:]

    for var in variables:
        domains[var]=total[var_domain[var]]


    f.close()
    return domains

def ctrfile(string):
    # return two dioctionaries:
    # constraints: a pair of variables as tuple is the key and the item is a tuple with "k value" and the opperator
    # neighbors: variable's ID is the key and the item is a list which contains all neighbors of the corresponding variable
    f=open("rlfap/"+string, "r")
    text=f.readlines()
    constraints={}
    neighbors={}
    for line in text[1:]:
        str=format(line.strip(" "))
        x,y,op,k=str.split(" ")
        k=int(k)
        x=int(x)
        y=int(y)

        constraints[(x,y)]=(k,op)
        constraints[(y,x)]=(k,op)

        if x not in neighbors:
            neighbors[x] = []
            neighbors[x].append(y)
        else:
            neighbors[x].append(y)

        if y not in neighbors:
            neighbors[y] = []
            neighbors[y].append(x)
        else:
            neighbors[y].append(x)


    f.close()
    return constraints,neighbors

#-------------------------------------------
def check(A,a,B,b):
    # checking if the constraints between 2 variables (A and B) for the corresponding values (a,b) apply
    if (A,B) in constraints:
        k=constraints[(A,B)][0]
        if constraints[(A,B)][1]=='=':
            return (abs(a-b)==k)
        else:
            return (abs(a-b)>k)
    elif (B,A) in constraints:
        k=constraints[(B,A)][0]
        if constraints[(B,A)][1]=='=':
            return (abs(a-b)==k)
        else:
            return (abs(a-b)>k)
            
#-------------------------------------------
# ------------------ Main ------------------
instance = sys.argv[1]
varname = "var" + instance + ".txt"
domname = "dom" + instance + ".txt"
ctrname = "ctr" + instance + ".txt"

variables,var_domain=varfile(varname)
domains=domfile(domname,variables,var_domain)
constraints,neighbors=ctrfile(ctrname)


algorithm=sys.argv[2]
data_obj = csp.CSP(variables,domains,neighbors,check,constraints)

if algorithm=="fc":
    print("Backtrack--dom/wdeg--lcv--fc\n")
    solution=csp.backtracking_search(data_obj,select_unassigned_variable=csp.domdivwdeg,order_domain_values=csp.lcv,inference=csp.forward_checking)
    print(solution[0])
    print("\nVisited nodes: %d " % data_obj.nassigns)
    print("\nChecks: %d" % solution[1])
elif algorithm=="mac":
    print("Backtrack--dom/wdeg--lcv--mac")
    solution=csp.backtracking_search(data_obj,select_unassigned_variable=csp.domdivwdeg,order_domain_values=csp.lcv,inference=csp.mac)
    print(solution[0])
    print("\nVisited nodes: %d " % data_obj.nassigns)
    print("\nChecks: %d" % solution[1])
elif algorithm=="fc-cbj":
    print("CBJ--dom/wdeg--lcv--fc")
    solution=csp.cbj_search(data_obj,select_unassigned_variable=csp.domdivwdeg,order_domain_values=csp.lcv,inference=csp.forward_checking)
    print(solution[0])
    print("\nVisited nodes: %d " % data_obj.nassigns)
    print("\nChecks: %d" % solution[1])
elif algorithm=="min-con":
    print("Min conflicts")
    solution=csp.min_conflicts(data_obj)
    print(solution[0])
    print("\nVisited nodes: %d " % data_obj.nassigns)
    print("\nChecks: %d" % solution[1])
else:
    print("Wrong input!")
