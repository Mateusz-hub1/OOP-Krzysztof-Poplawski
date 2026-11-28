// Pojedyncza operacja na koncie (wpis w historii)
public class Transaction
{
    public string Typ { get; }
    public decimal Kwota { get; }
    public decimal SaldoPo { get; }
    public string Opis { get; }
    public DateTime Data { get; }

    public Transaction(string typ, decimal kwota, decimal saldoPo, string opis = "")
    {
        Typ = typ;
        Kwota = kwota;
        SaldoPo = saldoPo;
        Opis = opis;
        Data = DateTime.Now;
    }

    public override string ToString()
    {
        return $"{Data:yyyy-MM-dd HH:mm} | {Typ,-20} | {Kwota,10:+0.00;-0.00} zł " +
               $"| saldo: {SaldoPo,10:F2} zł | {Opis}";
    }
}
