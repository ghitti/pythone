def discount(prices, isPet, nItems):

    # Verifica se c'è almeno un animale
    has_pet = any(isPet)
    
    # Conta il numero di articoli che non sono animali
    non_pet_items = sum(1 for item in isPet if not item)
    
    # Se c'è almeno un animale e almeno 5 altri articoli, applica lo sconto
    if has_pet and non_pet_items >= 5:
        # Calcola la somma dei prezzi degli articoli che non sono animali
        non_pet_total = sum(prices[i] for i in range(nItems) if not isPet[i])
        # Applica lo sconto del 20%
        return non_pet_total * 0.2
    else:
        # Nessuno sconto applicabile
        return 0

def main():
    print("Programma per calcolo sconto negozio animali")
    print("Inserisci il prezzo seguito da Y se animale, N se altro")
    print("Inserisci -1 per terminare l'input")
    
    prices = []
    isPet = []
    
    while True:
        # Utilizzo di split() per separare il prezzo e l'indicazione Y/N
        user_input = input("Inserisci prezzo e Y/N per indicare se animale (o -1 per terminare): ")
        
        # Controllo se l'utente ha inserito il valore sentinella
        if user_input == "-1":
            break
            
        # Divide l'input in due parti: prezzo e tipo
        parts = user_input.split()
        
        # Verifica che l'input sia nel formato corretto
        if len(parts) != 2:
            print("Formato non valido. Usa: prezzo Y/N (es: 25.50 N)")
            continue
            
        try:
            price = float(parts[0])
            pet_input = parts[1].upper()
            
            # Verifica che il tipo sia Y o N
            if pet_input not in ['Y', 'N']:
                print("Il tipo deve essere Y o N")
                continue
                
            is_pet = (pet_input == 'Y')
            
            prices.append(price)
            isPet.append(is_pet)
            
        except ValueError:
            print("Prezzo non valido. Inserisci un numero seguito da Y/N")
    
    nItems = len(prices)
    
    if nItems == 0:
        print("Nessun articolo inserito.")
        return
    
    # Calcola e visualizza lo sconto
    sconto = discount(prices, isPet, nItems)
    
    # Calcola il totale
    totale = sum(prices)
    
    # Visualizza il riepilogo
    print("\nRiepilogo acquisto:")
    print(f"Numero totale di articoli: {nItems}")
    print(f"Importo totale: {totale:.2f} €")
    print(f"Sconto applicato: {sconto:.2f} €")
    print(f"Importo finale: {totale - sconto:.2f} €")

if __name__ == "__main__":
    main()