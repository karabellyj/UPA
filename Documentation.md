## Zvolené téma: Kurzy devizového trhu

### Řešitelé: (Jozef Karabelly [xkarab03], Martin Eršek [xersek00])

### Zvolené dotazy a formulace vlastního dotazu:

- vytvořte popisné charakteristiky pro alespoň 10 zvolených měn (využijte krabicové grafy, histogramy, atd.) [skupina A]
- najděte skupiny měn s podobným chováním (skupiny měn, které obvykle současně posilují/oslabují) [skupina B]
- vytvorte rebríček mien, ktoré v danom období boli najviac/najmenej volatilné

### Stručná charakteristika zvolené datové sady:
Súbory s dátami kurzov devízového trhu obsahujú názov krajiny a meny, trojmiestnu skratku danej meny, množstvo meny za daný kurz a kurz v danom dni. Súbory sú textového formatú poskytnutého ČNB z URL adresy formátu: 

https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt?date=DD.MM.RRRR

, kde je možné špecifikovať dátum GET parametrom. Toto umožňuje následné stiahnutie a spracovanie pomocou algoritmov, pretože formát súborov je podobný CSV, avšak namiesto `,` sú hodnoty oddelené `|`. Prvý riadok obsahuje dátum a za týmto riadok nasleduje hlavička formátu:

`země|měna|množství|kód|kurz`

Na ďalších riadkoch nasledujú dáta kurzov, kde každý riadok obsahuje jednu menu napr.: `Austrálie|dolar|1|AUD|23,282`. Zvolené dotazy budú zodpovedané hlavne s dátami v stĺpcoch `množství`, `kód`, `kurz` a zvyšné stĺpce budú použité na lepšie formátovanie zobrazených dát. 

### Zvolený způsob uložení surových dat:
Pre ukladanie dát je zvolená NoSQL databáza Apache Cassandra, ktorá má nasledovné charakteristiky:
- Tzv. „wide-column store“ NoSQL databáza, teda používa tabuľky, sĺpce a riadky, podobne ako relačné databázy. Avšak narozdiel od RDBMS rôzne riadky v rovnakej tabuľke nemusia zdieľať rovnakú množinu stĺpcov a stĺpce môžu byť pridávané do jedného alebo viacerých riadkov v tabuľke.

- Dáta v tabuľke sú indexované pomocou „partition“ a „clustering“ klúčov, tzn. primárny kľúč sa delí na tieto dve časti, tj. dve skupiny sĺpcov. Ostatné stĺpce môžu byť indexované zvlášť od primárneho kľúča.

- „Partition key“ rozdeluje dáta v tabuľke medzi uzly tak, že používa hash tabuľku pre nájdenie uzlu, kde sú dáta časti tabuľky uložené.

- „Clustering key“ usporiadúva dáta v každej časti tabuľky, kde používa B+ strom na indexovanie dát na jednom uzly.

- Podporuje aj nastavenie TTL (time-to-live), teda po vypršaní sú dané riadky vymazané.
