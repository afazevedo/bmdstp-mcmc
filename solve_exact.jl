using LightGraphs: tree
using DelimitedFiles, Gurobi, JuMP, MathOptInterface, LightGraphs, Colors, GraphPlot 

model = Model(Gurobi.Optimizer)
B = 12733.0

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
    1 => "RS", 
    2 => "SC",
    3 => "PR",
    4 => "SP",
    5 => "MS", 
    6 => "RJ", 
    7 => "ES", 
    8 => "MG", 
    9 => "GO", 
    10 => "MT",
    11 => "BA",
    12 => "SE",
    13 => "AL",
    14 => "PE", 
    15 => "PB", 
    16 => "RN", 
    17 => "CE", 
    18 => "PI", 
    19 => "MA", 
    20 => "TO", 
    21 => "PA", 
    22 => "AP", 
    23 => "RR", 
    24 => "AM", 
    25 => "AC", 
    26 => "RO")

nodelabel = []
for i in x
    push!(nodelabel, i.second)
end 
push!(nodelabel, "r")

nodecolor = [colorant"greenyellow", colorant"teal", colorant"red", colorant"blue"]
map = ones(Int, n+1)
map[n+1] = 2
nodefill = nodecolor[map]
gplot(g, nodefillc=nodefill, nodelabel=nodelabel)
