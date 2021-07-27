using LightGraphs: tree
using DelimitedFiles, Gurobi, JuMP, MathOptInterface, LightGraphs, Colors, GraphPlot 

path = pwd()*"\\instances\\s_v20_a50_d4.txt"
n = readdlm(path, Int64)[1,1]
m = readdlm(path, Int64)[1,2]
L = Int((n)/2) 
c = zeros(n, n)

l = 1
for k in 2:m
    i = readdlm(path, Int64)[k, l]
    j = readdlm(path, Int64)[k, l+1]
    i = i+1
    j = j+1
    c[i,j] = readdlm(path)[k,l+2]
    c[j,i] = c[i,j]
end


model = Model(Gurobi.Optimizer)
set_optimizer_attribute(model, "Presolve", 0)
set_optimizer_attribute(model, "Cuts", 0)
set_optimizer_attribute(model, "Heuristics", 0)
set_optimizer_attribute(model, "Threads", 1)

B = 600

#Conjuntos
V = 1:n
V0 = 1:n+1

@variable(model, x[i in V0, j in V; i != j], Bin)
@variable(model, 0 <= u[i in V0] <= L+1)
@variable(model, z, Bin)
@variable(model, 0 <= w[i in V, j in V] <= 1, Int)
@variable(model, s >= 0)

@objective(model, Min, 2*(s-1) + z)

@constraint(model, root,
    sum(x[n+1,j] for j in V) == z+1
)

@constraint(model, in_deg[j in V],
    sum(x[i,j] for i in V0 if i != j) == 1
)

@constraint(model, mtz[j in V],
    u[n+1] - u[j] + (L+1)*x[n+1,j] <= L
)

@constraint(model, mtz1[i in V, j in V; i != j],
    u[i] - u[j] + (L+1)*x[i,j] + (L-1)*x[j,i] <= L
)

@constraint(model, mtz2[i in V],
    u[i] - u[n+1] + (L-1)*x[n+1,i] <= L
)

@constraint(model, budget,
    sum(c[i,j]*x[i,j] for i in V for j in V if i != j) + sum(c[i,j]*w[i,j] for i in V for j in V if i != j) <= B
)

@constraint(model, art[i in V, j in V; i != j],
    w[i,j] <= x[n+1, i]
)
@constraint(model, art2[i in V, j in V; i != j],
    w[i,j] <= x[n+1, j]
)

@constraint(model, central,
    sum(w[i,j] for i in V, j in V if i != j) == z
)

@constraint(model, mag[i in V],
    s >= u[i]
)

for i in 1:n
    for j in 1:n
        if c[i,j] < 0.000001 && i != j
            set_upper_bound(x[i,j], 0.0)
            set_lower_bound(x[i,j], 0.0)
            set_upper_bound(w[i,j], 0.0)
            set_lower_bound(w[i,j], 0.0)
        end
    end
end

optimize!(model)
obj = objective_bound(model)
tempo = solve_time(model)

println("Diâmetro mínimo: ", objective_value(model))
println("Budget: ", B)
println("Custo total da árvore: ", sum(c[i,j]*value(x[i,j]) for i in 1:n, j in 1:n if i != j) + sum(c[i,j]*value(w[i,j]) for i in 1:n, j in 1:n if i != j))
println("Árvore: ")

g = SimpleGraph(n+1)

for i in 1:n+1
    for j in 1:n
        if i != j && value(x[i,j]) > 0.00001
            add_edge!(g, i, j)
            if i == n+1
                println("r ---> ", j)
            else
                println(i, " ---> ", j)
            end
        elseif i < n+1 && i != j && value(w[i,j]) > 0.00001
            add_edge!(g, i, j)
            println(i, " ---> ", j)
        end
    end
end

x = Dict()
x = (
    0 => "RS", 
    1 => "SC",
    2 => "PR",
    3 => "MS",
    4 => "SP", 
    5 => "RJ", 
    6 => "ES", 
    7 => "MG", 
    8 => "GO", 
    9 => "MT",
    10 => "RO",
    11 => "AC",
    12 => "AM",
    13 => "RR", 
    14 => "PA", 
    15 => "AP", 
    16 => "TO", 
    17 => "BA", 
    18 => "MA", 
    19 => "PI", 
    20 => "CE", 
    21 => "RN", 
    22 => "PB", 
    23 => "AL", 
    24 => "SE", 
    25 => "PE"
    )


# sum(c[13,14] + c[14,15])


nodelabel = []
for i in x
    push!(nodelabel, i.second)
end 
push!(nodelabel, "r")

nodecolor = [colorant"greenyellow", colorant"teal", colorant"red", colorant"blue"]
map = ones(Int, n+1)
map[n+1] = 2
nodefill = nodecolor[map]
gplot(g, nodefillc=nodefill)


# function MST(G,c,n)
#     mst = LightGraphs.SimpleGraph(n)
#     cost = 0
#     for k in 1:n-1
#         i = src(data[k])
#         j = dst(data[k])
#         add_edge!(mst, i, j)
#         cost = cost + c[i,j]
#     end
#     return cost, mst
# end

# g = SimpleGraph(n)

# for i in 1:n
#     for j in 1:n
#         if c[i,j] > 0.0001
#             add_edge!(g, i, j)
#         end 
#     end
# end


# cost, mst = MST(g, c, n)

# nodelabel = []
# for i in x
#     push!(nodelabel, i.second)
# end 


# nodecolor = [colorant"greenyellow", colorant"teal", colorant"red", colorant"blue"]
# map = ones(Int, n)
# nodefill = nodecolor[map]
# gplot(mst, nodefillc=nodefill, nodelabel=nodelabel)

# diameter(mst)