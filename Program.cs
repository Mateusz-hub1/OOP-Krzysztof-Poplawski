// Zadanie 2: System bankowy – klasy Account, Transaction, Bank
using System.Globalization;

Console.OutputEncoding = System.Text.Encoding.UTF8;
CultureInfo.CurrentCulture = CultureInfo.InvariantCulture;

var bank = new Bank("WSB Bank");
// przykładowe konta, żeby od razu było na czym testować
bank.OtworzKonto("Jan Kowalski", 1000);
bank.OtworzKonto("Anna Nowak", 500);

while (true)
{
    Console.WriteLine($"\n=== {bank.Nazwa} ===");
    Console.WriteLine("1. Otwórz konto");
    Console.WriteLine("2. Lista kont");
    Console.WriteLine("3. Wpłata");
    Console.WriteLine("4. Wypłata");
    Console.WriteLine("5. Przelew");
    Console.WriteLine("6. Historia transakcji");
    Console.WriteLine("0. Wyjście");
    string wybor = Czytaj("Wybierz opcję: ");

    try
    {
        switch (wybor)
        {
            case "1":
            {
                string wlasciciel = Czytaj("Imię i nazwisko właściciela: ");
                decimal kwota = CzytajKwote("Wpłata początkowa (0 jeśli brak): ");
                var konto = bank.OtworzKonto(wlasciciel, kwota);
                Console.WriteLine($"Otworzono konto nr {konto.Numer}.");
                break;
            }
            case "2":
                foreach (var konto in bank.Konta)
                    Console.WriteLine(konto);
                break;
            case "3":
            {
                var konto = bank.ZnajdzKonto(Czytaj("Numer konta: "));
                konto.Wplac(CzytajKwote("Kwota wpłaty: "));
                Console.WriteLine($"Wpłacono. Nowe saldo: {konto.Saldo:F2} zł");
                break;
            }
            case "4":
            {
                var konto = bank.ZnajdzKonto(Czytaj("Numer konta: "));
                konto.Wyplac(CzytajKwote("Kwota wypłaty: "));
                Console.WriteLine($"Wypłacono. Nowe saldo: {konto.Saldo:F2} zł");
                break;
            }
            case "5":
            {
                string zNumeru = Czytaj("Z konta nr: ");
                string naNumer = Czytaj("Na konto nr: ");
                bank.Przelew(zNumeru, naNumer, CzytajKwote("Kwota przelewu: "));
                Console.WriteLine("Przelew wykonany.");
                break;
            }
            case "6":
            {
                var konto = bank.ZnajdzKonto(Czytaj("Numer konta: "));
                Console.WriteLine($"Historia konta {konto.Numer} ({konto.Wlasciciel}):");
                if (konto.Historia.Count == 0)
                    Console.WriteLine("Brak transakcji.");
                foreach (var t in konto.Historia)
                    Console.WriteLine(t);
                break;
            }
            case "0":
                Console.WriteLine("Do widzenia!");
                return;
            default:
                Console.WriteLine("Nieprawidłowy wybór.");
                break;
        }
    }
    catch (Exception e) when (e is ArgumentException or InvalidOperationException or KeyNotFoundException)
    {
        Console.WriteLine($"Błąd: {e.Message}");
    }
}

static string Czytaj(string komunikat)
{
    Console.Write(komunikat);
    return (Console.ReadLine() ?? "").Trim();
}

static decimal CzytajKwote(string komunikat)
{
    while (true)
    {
        string tekst = Czytaj(komunikat).Replace(',', '.');
        if (decimal.TryParse(tekst, NumberStyles.Number, CultureInfo.InvariantCulture, out decimal kwota))
            return kwota;
        Console.WriteLine("To nie jest poprawna kwota.");
    }
}
