library(pedtools)
library(kinship2)

df = read.table("figures/R/two_sibs.txt", header=TRUE)
p = ped(id=df$id, fid=df$dadid, mid=df$momid, sex=df$sex)
m = marker(p, "1" = "1/2", "2" = "3/4", "3" = "1/3", "4" = "2/3")

png("figures/two_sibs_markers.png")
plot(p, marker=m)
dev.off()
