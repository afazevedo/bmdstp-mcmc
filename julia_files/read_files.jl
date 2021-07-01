using DelimitedFiles, Gurobi, JuMP, MathOptInterface, LightGraphs, Colors, GraphPlot 

function read_graph(n, path)
    L = Int(n/2) 
    c = zeros(n, n)

    for i in 1:n
        for j in i:n
            c[i,j] = readdlm(path, Int64)[i,j]
            c[j,i] = c[i,j]
        end 
    end

    g = SimpleGraph(n)

    for i in 1:n
        for j in 1:n
            if i != j && c[i,j] > 0.00001
                add_edge!(g, i, j)
            end 
        end 
    end

path = pwd()*"\\instances\\estados_brasil.txt"
