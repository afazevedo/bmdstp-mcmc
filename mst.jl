function MST(G,c,n)
    data = prim_mst(G, c)
    mst = LightGraphs.SimpleGraph(n)
    cost = 0
    for k in 1:n-1
        i = src(data[k])
        j = dst(data[k])
        add_edge!(mst, i, j)
        cost = cost + c[i,j]
    end
    return cost, mst
end

custo, mst = MST(g, c, n)
gplot(mst, nodelabel=nodelabel)
diameter(mst)