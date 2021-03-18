import psycopg2 as pysql

def previously_viewed(profid):
    'Conn naar db'
    try:
        # Connect met de database
        conn = pysql.connect(
            host='localhost',  # De host waarop je database runt
            database='huwebwinkel',  # Database naam
            user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
            password='IXXKnbmew'  # Wachtwoord die je opgaf bij installatie
            # port=5432 runt standaard op deze port en is alleen nodig als je de port handmatig veranderd
        )
        #Cursor
        cur = conn.cursor()
        print("\nConnection established")
        # Uitvoer query, atribuut, atribuut moet je vervangen voor de atributen die je wilt fetchen.
        # zet select * from tabel om alles van een tabel te fetchen
        cur.execute(f"select * from profiles_previously_viewed where profid = '{profid}'")
        # Je wilt alles fetchen van de query die je hebt uitgevoerd
        rows = cur.fetchall()

        print(f"\nPreviously viewed: {profid}")
        # Forloop die alles in elke row steeds alle colums af gaat. Per column die je hebt, moet je een {r[index]}
        # toevoegen om hem te printen
        for r in rows:
            print(r[1])

    except pysql.OperationalError as x:
        print(f"Connection error : {x}")

    finally:

        # Sluit de cursor
        cur.close()
        # sluit connectie
        conn.close()
        print("\nConnection closed")

previously_viewed('5a393d68ed295900010384ca')
previously_viewed('5a3945b0ed29590001038fea')
previously_viewed('5a396e36a825610001bbb368')