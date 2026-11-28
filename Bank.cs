// Logika
public class Bank
{
    public string Nazwa { get; }
    private readonly Dictionary<string, Account> konta = new(); 
    private int nastepnyNumer = 1001;

    public Bank(string nazwa)
    {
        Nazwa = nazwa;
    }

    public IEnumerable<Account> Konta => konta.Values;

    public Account OtworzKonto(string wlasciciel, decimal wplataPoczatkowa = 0)
    {
        var konto = new Account(nastepnyNumer.ToString(), wlasciciel);
        nastepnyNumer++;
        konta[konto.Numer] = konto;
        if (wplataPoczatkowa > 0)
            konto.Wplac(wplataPoczatkowa, opis: "Wpłata początkowa");
        return konto;
    }

    public Account ZnajdzKonto(string numer)
    {
        if (!konta.TryGetValue(numer, out var konto))
            throw new KeyNotFoundException($"Nie ma konta o numerze {numer}.");
        return konto;
    }

    public void Przelew(string zNumeru, string naNumer, decimal kwota)
    {
        if (zNumeru == naNumer)
            throw new InvalidOperationException("Nie można zrobić przelewu na to samo konto.");
        var nadawca = ZnajdzKonto(zNumeru);
        var odbiorca = ZnajdzKonto(naNumer);
        nadawca.Wyplac(kwota, "Przelew wychodzący", $"do {odbiorca.Numer} ({odbiorca.Wlasciciel})");
        odbiorca.Wplac(kwota, "Przelew przychodzący", $"od {nadawca.Numer} ({nadawca.Wlasciciel})");
    }
}
