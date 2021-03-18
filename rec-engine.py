import psycopg2 as pysql
##########################
# Colin van Lienden
# rec-engine
##########################

def most_viewed():
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
        # Uitvoer query
        cur.execute(f"""            
        DROP TABLE IF EXISTS most_viewed;
            create table most_viewed(
                prodid varchar(255),
                viewed int
            );

        SELECT prodid, COUNT(*) AS viewed
                        FROM profiles_previously_viewed
                        GROUP BY prodid
                        HAVING COUNT(*) > 1
                        ORDER BY viewed DESC;
        """)
        # Je wilt alles fetchen van de query die je hebt uitgevoerd
        rows = cur.fetchall()

        # Forloop die alles in elke row steeds alle colums af gaat. Per column die je hebt, moet je een {r[index]}
        # toevoegen om hem te printen
        print('write data to database...')
        for r in rows:
            cur.execute('''insert into most_viewed (prodid, viewed) values (%s, %s)''',
                        (r[0],r[1]))

    except pysql.OperationalError as x:
        print(f"Connection error : {x}")

    finally:
        # commit inserts
        conn.commit()
        # Sluit de cursor
        cur.close()
        # sluit connectie
        conn.close()
        print("\nConnection closed")

most_viewed()
