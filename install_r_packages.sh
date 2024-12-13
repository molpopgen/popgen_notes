packages=(kinship2)

for p in ${packages}
do
    R --no-save --quiet -e "install.packages('$p', repos='http://cran.us.r-project.org')"
done
