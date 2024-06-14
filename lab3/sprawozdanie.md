| Imię        | Nazwisko    | Numer Indeksu |
| :---        |    :----:   |          ---: |
| Mateusz     | Kowalczyk   | 268533        |

# Sprawozdanie Moduł 4 - Akwizycja danych w systemie testowym/kontroli jakości

## Zadanie 1: Napisz skrypt pobierający próbki Analog Input (AI) oraz Digital Input (DI)
### Hardware:
![makieta](makieta1.jpg)
### Kod:
```python
import nidaqmx
from nidaqmx.constants import LineGrouping
import time

device_name = 'myDAQ2'

# Utworzenie taska
with nidaqmx.Task() as ai_task, nidaqmx.Task() as di_task:
    # Konfiguracja kanału wejścia analogowego (AI)
    ai_task.ai_channels.add_ai_voltage_chan(f"{device_name}/ai0")
    
    # Konfiguracja kanału wejścia cyfrowego (DI)
    di_task.di_channels.add_di_chan(f"{device_name}/port0/line0", line_grouping=LineGrouping.CHAN_PER_LINE)
    
    # Pobieranie próbek w pętli
    try:
        while True:
            # Odczyt próbek AI
            ai_data = ai_task.read()
            print(f"Analog Input (AI) value: {ai_data:.2f} V")
            
            # Odczyt próbek DI
            di_data = di_task.read()
            print(f"Digital Input (DI) value: {di_data}")
            
            # delay
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("Zatrzymano pobieranie próbek.")
```

## Zadanie 2: Stwórz moduł do ciągłej akwizycji z AI
    - Proces akwizycji opakowany w klasie i umieszczony w oddzielnym module
    - Konfigurowalne wejście, częstotliwość oraz zakres pomiaru
    - F-cja Start uruchamia akwizycję w oddzielnym wątku
    - F-cja Stop zatrzymuje akwizycję
    - Pętla uruchamiana co 100ms wkłada próbki do bufora wewnatrz klasy
    - Funkcje `get_samples` odczytuje i usuwa próbki z bufora klasy

### Hardware:
![makieta](makieta2.jpg)
### Kod:

## Zadanie 3: Aplikacja wykorzystująca moduł z ćwiczenia 2 z GUI (Tktinner)
    - Start, Stop akwizycji (wyświetlamy wartości ale nie zapisujemy ich)
    - Start, Stop początku pomiaru/ okresu oceniania
    - Ustawienie częstotliwości, długości pomiaru
    - Rysowanie pobieranych danych na wykresie
    - Limit min,max ocena oraz wizualna informacja czy w trakcie pomiaru zmieszczono się w limicie
    - Zapis do pliku, nazwa pliku generowana automatycznie
    - Możliwość pracy automatycznej - po każdym pomiarze, odliczamy określony czas i zaczynamy od nowa
        - wizualna informacja o stanie w którym znajduje się aktualnie program
    - Do testów możesz wykorzystać elementy makiety (potencjometr, czujnik zblizeniowy, przełącznik)
### Hardware:
![makieta](makieta3.jpg)
### Kod:

## Zadanie 4: stwórz moduł generujący na AO 
![makieta](makieta4.jpg)
### Hardware:
### Kod:




