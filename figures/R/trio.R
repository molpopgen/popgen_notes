library(kinship2)

p = pedigree(id=c(0, 1, 2), dadid=c(NA, NA, 0), momid=c(NA, NA, 1), sex=c(0, 1, 1))
png("figures/trio.png")
plot(p)
dev.off()
