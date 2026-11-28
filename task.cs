// Zadanie 1: kalkulator dwóch liczb
using System.Globalization;

Console.OutputEncoding = System.Text.Encoding.UTF8;
CultureInfo.CurrentCulture = CultureInfo.InvariantCulture; // kropka jako separator dziesiętny

Console.Write("Podaj pierwszą liczbę: ");
double a = double.Parse(Console.ReadLine().Replace(',', '.'));
Console.Write("Podaj drugą liczbę: ");
double b = double.Parse(Console.ReadLine().Replace(',', '.'));
Console.Write("Podaj operację (+, -, *, /): ");
string op = Console.ReadLine().Trim();

if (op == "+")
    Console.WriteLine($"Wynik: {a + b}");
else if (op == "-")
    Console.WriteLine($"Wynik: {a - b}");
else if (op == "*")
    Console.WriteLine($"Wynik: {a * b}");
else if (op == "/")
{
    if (b == 0)
        Console.WriteLine("Błąd: nie można dzielić przez zero.");
    else
        Console.WriteLine($"Wynik: {a / b}");
}
else
    Console.WriteLine("Nieznana operacja.");
