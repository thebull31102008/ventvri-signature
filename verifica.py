#!/usr/bin/env python3
"""verifica.py - controlla le firme delle fotografie di VENTVRI.

Ogni lunedi' VENTVRI scatta una fotografia delle sue previsioni: un file JSON con la
probabilita' che ogni tecnologia del registro salga il prossimo gradino entro la fine
di quest'anno, del prossimo e di quello dopo. Il giorno stesso, la sua impronta entra
nel registro di questo repository (registro.jsonl). L'impronta non dice niente delle
previsioni: impedisce soltanto di cambiarle dopo senza che si veda.

L'impronta e' lo SHA-256 dei byte del file, con gli a capo nella forma di Unix (\\n).
Ogni riga del registro porta anche l'impronta della riga prima (campo «precedente»):
una riga tolta, aggiunta in mezzo o cambiata rompe la catena.

Uso:  python verifica.py                       controlla la catena del registro
      python verifica.py FOTOGRAFIA.json ...   cerca nel registro l'impronta di ogni file
      python verifica.py --registro PERCORSO   un altro registro (per esempio una copia)

Serve solo Python 3, senza pacchetti da installare.
"""
import hashlib
import json
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))


def impronta_file(percorso):
    """l'impronta di una fotografia, e quanti byte conta con gli a capo di Unix"""
    dati = open(percorso, "rb").read().replace(b"\r\n", b"\n")
    return "sha256:" + hashlib.sha256(dati).hexdigest(), len(dati)


def riga(voce):
    """la forma con cui una voce sta nel registro: chiavi in ordine, niente spazi"""
    return json.dumps(voce, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def impronta_riga(testo):
    return "sha256:" + hashlib.sha256(testo.encode("utf-8")).hexdigest()


def leggi(percorso):
    """le righe del registro, come testo, senza le righe vuote"""
    if not os.path.exists(percorso):
        return []
    testo = open(percorso, "rb").read().decode("utf-8").replace("\r\n", "\n")
    return [r for r in testo.split("\n") if r.strip()]


def controlla_catena(righe):
    """i problemi della catena: numeri in fila, ogni riga legata a quella prima, forma esatta"""
    problemi, prima = [], None
    for i, testo in enumerate(righe, 1):
        try:
            voce = json.loads(testo)
        except ValueError:
            problemi.append(f"riga {i}: non e' JSON")
            prima = impronta_riga(testo)
            continue
        if riga(voce) != testo:
            problemi.append(f"riga {i}: non e' nella forma del registro (chiavi in ordine, niente spazi)")
        if voce.get("n") != i:
            problemi.append(f"riga {i}: numero {voce.get('n')}, atteso {i}")
        if voce.get("precedente") != prima:
            problemi.append(f"riga {i}: la catena e' rotta (precedente {voce.get('precedente')}, atteso {prima})")
        prima = impronta_riga(testo)
    return problemi


def main(argv):
    registro = os.path.join(QUI, "registro.jsonl")
    if "--registro" in argv:
        i = argv.index("--registro")
        registro = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    righe = leggi(registro)
    if not righe:
        print(f"il registro {registro} e' vuoto o non c'e'")
        return 1
    problemi = controlla_catena(righe)
    for p in problemi:
        print("  ✘", p)
    voci = [json.loads(r) for r in righe if r.startswith("{")]
    if not problemi:
        ultima = voci[-1]
        print(f"catena intatta: {len(voci)} fotografie firmate, l'ultima del {ultima.get('fotografia')}, "
              f"firmata il {ultima.get('firmata_il')}")
    per_impronta = {v.get("impronta"): v for v in voci}
    esito = 1 if problemi else 0
    for f in argv:
        imp, n = impronta_file(f)
        v = per_impronta.get(imp)
        if v:
            print(f"  ✔ {f}: e' la fotografia del {v.get('fotografia')}, firmata il {v.get('firmata_il')} (riga {v.get('n')})")
        else:
            print(f"  ✘ {f}: la sua impronta ({imp}) non e' nel registro: il file e' diverso da ogni fotografia firmata")
            esito = 1
    return esito


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
