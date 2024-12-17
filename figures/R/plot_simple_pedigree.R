library(kinship2)

args <- commandArgs(trailingOnly=TRUE)

data = read.table(args[1], header=TRUE)
p = pedigree(id=data$id, dadid=data$dadid, momid=data$momid, sex=data$sex)
png(args[2])
plot(p)
dev.off()
