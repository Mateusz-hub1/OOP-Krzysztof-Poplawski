from datetime import datetime
from decimal import Decimal, InvalidOperation


class Transaction:
    """Pojedyncza operacja na koncie (wpis w historii)."""

    def __init__(self, typ, kwota, saldo_po, opis=""):
        self.typ = typ
        self.kwota = kwota
        self.saldo_po = saldo_po
        self.opis = opis
        self.data = datetime.now()

    def __str__(self):
        return (f"{self.data:%Y-%m-%d %H:%M} | {self.typ:<20} | {self.kwota:>+10.2f} zł "
                f"| saldo: {self.saldo_po:>10.2f} zł | {self.opis}")


class Account:
    """Konto bankowe: przechowuje saldo i historię transakcji."""

    def __init__(self, numer, wlasciciel):
        self.numer = numer
        self.wlasciciel = wlasciciel
        self._saldo = Decimal("0")   # "_" = nie zmieniamy salda bezpośrednio z zewnątrz
        self.historia = []

    @property
    def saldo(self):
        return self._saldo

    def wplac(self, kwota, typ="Wpłata", opis=""):
        if kwota <= 0:
            raise ValueError("Kwota musi być większa od zera.")
        self._saldo += kwota
        self.historia.append(Transaction(typ, kwota, self._saldo, opis))

    def wyplac(self, kwota, typ="Wypłata", opis=""):
        if kwota <= 0:
            raise ValueError("Kwota musi być większa od zera.")
        if kwota > self._saldo:
            raise ValueError("Brak wystarczających środków na koncie.")
        self._saldo -= kwota
        self.historia.append(Transaction(typ, -kwota, self._saldo, opis))

    def __str__(self):
        return f"[{self.numer}] {self.wlasciciel:<20} saldo: {self._saldo:.2f} zł"


class Bank:
    """Bank: zarządza kontami i wykonuje przelewy między nimi."""

    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.konta = {}          # numer konta -> obiekt Account
        self._nastepny_numer = 1001

    def otworz_konto(self, wlasciciel, wplata_poczatkowa=Decimal("0")):
        konto = Account(str(self._nastepny_numer), wlasciciel)
        self._nastepny_numer += 1
        self.konta[konto.numer] = konto
        if wplata_poczatkowa > 0:
            konto.wplac(wplata_poczatkowa, opis="Wpłata początkowa")
        return konto

    def znajdz_konto(self, numer):
        if numer not in self.konta:
            raise ValueError(f"Nie ma konta o numerze {numer}.")
        return self.konta[numer]

    def przelew(self, z_numeru, na_numer, kwota):
        if z_numeru == na_numer:
            raise ValueError("Nie można zrobić przelewu na to samo konto.")
        nadawca = self.znajdz_konto(z_numeru)
        odbiorca = self.znajdz_konto(na_numer)
        nadawca.wyplac(kwota, "Przelew wychodzący", f"do {odbiorca.numer} ({odbiorca.wlasciciel})")
        odbiorca.wplac(kwota, "Przelew przychodzący", f"od {nadawca.numer} ({nadawca.wlasciciel})")


# ---------- Interfejs konsolowy ----------

def czytaj_kwote(komunikat):
    while True:
        try:
            return Decimal(input(komunikat).replace(",", "."))
        except InvalidOperation:
            print("To nie jest poprawna kwota.")


def main():
    bank = Bank("WSB Bank")
    # przykładowe konta, żeby od razu było na czym testować
    bank.otworz_konto("Jan Kowalski", Decimal("1000"))
    bank.otworz_konto("Anna Nowak", Decimal("500"))

    while True:
        print(f"\n=== {bank.nazwa} ===")
        print("1. Otwórz konto")
        print("2. Lista kont")
        print("3. Wpłata")
        print("4. Wypłata")
        print("5. Przelew")
        print("6. Historia transakcji")
        print("0. Wyjście")
        wybor = input("Wybierz opcję: ").strip()

        try:
            if wybor == "1":
                wlasciciel = input("Imię i nazwisko właściciela: ").strip()
                kwota = czytaj_kwote("Wpłata początkowa (0 jeśli brak): ")
                konto = bank.otworz_konto(wlasciciel, kwota)
                print(f"Otworzono konto nr {konto.numer}.")
            elif wybor == "2":
                for konto in bank.konta.values():
                    print(konto)
            elif wybor == "3":
                konto = bank.znajdz_konto(input("Numer konta: ").strip())
                konto.wplac(czytaj_kwote("Kwota wpłaty: "))
                print(f"Wpłacono. Nowe saldo: {konto.saldo:.2f} zł")
            elif wybor == "4":
                konto = bank.znajdz_konto(input("Numer konta: ").strip())
                konto.wyplac(czytaj_kwote("Kwota wypłaty: "))
                print(f"Wypłacono. Nowe saldo: {konto.saldo:.2f} zł")
            elif wybor == "5":
                z_numeru = input("Z konta nr: ").strip()
                na_numer = input("Na konto nr: ").strip()
                bank.przelew(z_numeru, na_numer, czytaj_kwote("Kwota przelewu: "))
                print("Przelew wykonany.")
            elif wybor == "6":
                konto = bank.znajdz_konto(input("Numer konta: ").strip())
                print(f"Historia konta {konto.numer} ({konto.wlasciciel}):")
                if not konto.historia:
                    print("Brak transakcji.")
                for t in konto.historia:
                    print(t)
            elif wybor == "0":
                print("Do widzenia!")
                break
            else:
                print("Nieprawidłowy wybór.")
        except ValueError as e:
            print(f"Błąd: {e}")


if __name__ == "__main__":
    main()
