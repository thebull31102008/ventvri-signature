# VENTVRI — le firme delle fotografie

VENTVRI è un osservatorio delle tecnologie che arrivano. Segue alcune centinaia di traguardi tecnologici, e per ognuno stima quando salirà il prossimo gradino della sua scala: dimostrata, in vendita, in crescita, di massa.

Ogni lunedì un programma automatico scatta una **fotografia** delle previsioni: un file con la probabilità che ogni tecnologia salga il prossimo gradino entro la fine di quest'anno, del prossimo e di quello dopo. Le previsioni si giudicano dopo, con le regole scritte prima di vedere un solo esito: un anno si giudica in via provvisoria il 1° gennaio e in via definitiva il 1° aprile dell'anno dopo.

Un giudizio così vale solo se le previsioni non sono state ritoccate dopo. Questo repository serve a provarlo.

## Cosa c'è qui

Solo le **impronte** delle fotografie, non le fotografie. Un'impronta è una sequenza di 64 caratteri calcolata dal file (SHA-256): non dice niente del contenuto, ma basta cambiare una virgola del file perché cambi del tutto.

- `registro.jsonl`: una riga per fotografia, in ordine;
- `verifica.py`: il programma che controlla le firme. È lo stesso codice con cui VENTVRI le calcola.

Ogni riga del registro porta anche l'impronta della riga prima (campo `precedente`). Così il registro è una catena: non si può togliere, aggiungere in mezzo o cambiare una riga senza romperla.

## Il sigillo di Bitcoin

Chi possiede un repository, in teoria, ne può riscrivere la storia. Per questo ogni impronta è anche **sigillata nella blockchain di Bitcoin**, il registro pubblico copiato su decine di migliaia di computer nel mondo, che nessuno può cambiare: nemmeno noi.

Il sigillo lo fa [OpenTimestamps](https://opentimestamps.org), un servizio aperto e gratuito: raccoglie le impronte di chiunque, le riunisce in una sola e la scrive in una transazione di Bitcoin. In cambio dà una prova, un file `.ots`, che collega l'impronta a quel blocco. Viaggia solo l'impronta. VENTVRI non compra, non vende e non consiglia criptovalute: usa il registro di Bitcoin come un notaio.

- `bitcoin/AAAA-MM-GG.json.ots`: la prova di ogni fotografia;
- `bitcoin.json`: per ogni fotografia, il blocco di Bitcoin, la sua ora e i due esploratori pubblici su cui il programma l'ha controllato (mempool.space e blockstream.info).

Il blocco arriva qualche ora dopo la firma: fino ad allora la prova è «in attesa».

**Come si controlla un sigillo.** Su [opentimestamps.org](https://opentimestamps.org) si trascina il file `.ots`: la pagina mostra l'impronta sigillata, che è quella del registro, e il blocco di Bitcoin con la sua data. Quando le fotografie saranno pubbliche, si trascina anche la fotografia, e la pagina controlla tutto da sola. Chi ha un nodo Bitcoin può usare il programma ufficiale: `ots verify 2026-10-12.json.ots`.

## Come si controlla

Serve Python 3, senza pacchetti da installare.

```
python verifica.py                        controlla la catena del registro
python verifica.py 2026-10-12.json        dice se il file è una fotografia firmata, e quando
```

Senza programmi: l'impronta è lo SHA-256 dei byte del file, con gli a capo nella forma di Unix (`\n`). Su Linux e macOS, `sha256sum 2026-10-12.json` (o `shasum -a 256`) dà lo stesso numero del campo `impronta`, senza il prefisso `sha256:`.

## Cosa prova, e cosa no

- **Prova** che una fotografia con quell'impronta esisteva quando la sua riga è entrata in questo repository, e, con il sigillo, prima del blocco di Bitcoin che la contiene. Il blocco è la data più solida: non la può cambiare nessuno. `firmata_il` è il giorno in cui il programma ha calcolato l'impronta.
- **Non prova** che le previsioni siano buone: quello lo dice il Rendiconto, con il punteggio di Brier, accanto a quello di due avversari, l'orologio (la storia delle tecnologie) e il caso (lo stesso ritmo per tutti).
- **Le prime fotografie** sono state scattate prima che nascesse la firma, il 14 ottobre 2026: sono firmate tutte insieme il giorno della prima firma, e sigillate su Bitcoin il giorno del primo sigillo. Per loro la prova vale da quei giorni. Dalla fotografia successiva, firma e sigillo arrivano il giorno stesso della fotografia.

## I campi di una riga

| campo | cosa dice |
|---|---|
| `n` | il numero della riga, da 1 |
| `fotografia` | il giorno della fotografia |
| `file` | dove sta la fotografia nell'archivio di VENTVRI |
| `impronta` | lo SHA-256 del file |
| `byte` | quanti byte conta il file, con gli a capo di Unix |
| `firmata_il` | il giorno in cui l'impronta è stata calcolata |
| `precedente` | l'impronta della riga prima (per la prima riga, `null`) |
| `metodo_v`, `punteggio_v` | le versioni del metodo e delle regole del punteggio con cui è stata scattata |
| `traguardi`, `porte` | quante tecnologie e quanti colli di bottiglia contiene |

L'impronta di una riga è lo SHA-256 del suo testo esatto (UTF-8, chiavi in ordine alfabetico, nessuno spazio).

VENTVRI è una ricerca personale, non una consulenza finanziaria.
