using JSON3
using Strings
using DelimitedFiles
using FreqTables

## wczytujemy dane
m1 = vcat(readlines("./data-raw/kprm-new-data.json"), readlines("./data-raw/kprm-old-data.json"))

## parsujemy i zmieniamy
ogloszenia = [JSON3.read(i) for i in m1]

## zapisujemy firmy
[i[3] for i in ogloszenia] |> unique |> sort |> (x -> writedlm("data/kprm-firmy.txt", x))

## wyniki naboru
results = match.(r"(anulowano nabór|nabór zakończony bez wyboru|nabór zakończony wyborem|informacja o zatrudnieniu|nie zatrudniono|brak ofert|nie wyłoniono|nabór zakończony bez zatrudnienia|nabór zakończony zatrudnieniem|oferty kandydatek/kandydatów nie spełniały|decyzja kandydatki/kandydata o rezygnacji)", [i[7] for i in ogloszenia])

@assert sum(isnothing.(results)) == 0

#[i[7] for i in ogloszenia[findall(isnothing.(results) .== 1)]]

## ile ofert zakończyło się rezultatem
[i.match for i in results] |> freqtable |> (x -> sort(x, rev = true))

## przyczyna anulowania
anulowane = [i.match for i in results] .== "anulowano nabór"
anulowane = [i[7] for i in ogloszenia[findall(anulowane .== 1)]] 
anulowane = replace.(anulowane, "Wyniki naboru: anulowano nabór" => "") 
anulowane = replace.(anulowane, "|" => "") 
writedlm("data/kprm-anulowane.txt", anulowane |> freqtable |> (x -> sort(x, rev = true)))

## wśród anulowanych są takie oferty, które były aktualne ale nie było ofert  -- proste warunki, trzeba inne te wpisać
anulowane[contains.(lowercase.(anulowane), r"^(brak (ofert|kandyda|nadesł)|nie wpłynęła)")]

## kategorie
### zakonczony - ok (nawet jak zrezygnowali)
### zakonczony - nie bylo nikogo
### zakonczony - nie spełniały wymagań
### zakonczony - blad / usuniecie oferty