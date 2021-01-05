using JSON3
using Strings
using DelimitedFiles

m1 = vcat(readlines("./data-raw/kprm-new-data.json"), readlines("./data-raw/kprm-old-data.json"))
firmy = [JSON3.read(i)[3] for i in m1]

unique(firmy) |> sort |> (x -> writedlm("data/kprm-firmy.txr", x))

