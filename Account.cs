// Konto bankowe: przechowuje saldo i historię transakcji
public class Account
{
    public string Numer { get; }
    public string Wlasciciel { get; }
    public decimal Saldo { get; private set; }   // odczyt z zewnątrz, zmiana tylko w tej klasie
    public List<Transaction> Historia { get; } = new();

    public Account(string numer, string wlasciciel)
    {
        Numer = numer;
        Wlasciciel = wlasciciel;
    }

    public void Wplac(decimal kwota, string typ = "Wpłata", string opis = "")
    {
        if (kwota <= 0)
            throw new ArgumentException("Kwota musi być większa od zera.");
        Saldo += kwota;
        Historia.Add(new Transaction(typ, kwota, Saldo, opis));
    }

    public void Wyplac(decimal kwota, string typ = "Wypłata", string opis = "")
    {
        if (kwota <= 0)
            throw new ArgumentException("Kwota musi być większa od zera.");
        if (kwota > Saldo)
            throw new InvalidOperationException("Brak wystarczających środków na koncie.");
        Saldo -= kwota;
        Historia.Add(new Transaction(typ, -kwota, Saldo, opis));
    }

    public override string ToString() => $"[{Numer}] {Wlasciciel,-20} saldo: {Saldo:F2} zł";
}