import datetime
godzina_A = datetime.timedelta(hours=6, minutes=52)
tempo_r = datetime.timedelta(minutes=6, seconds=15)
tempo_s = datetime.timedelta(minutes=4, seconds=12)
droga_1, droga_2, droga_3 = 1.5, 4.8, 1.0
czas_c = tempo_r*droga_1 + tempo_s*droga_2 + tempo_r*droga_3
godzina_B = godzina_A + czas_c
print(godzina_B)
