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

#most_viewed()



# Alleen in print !!
def same_cat_rec(profid):
    'Laat producten zien die overheen komen met de catogory waarnaar de klant heeft gezocht'
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
        SELECT
            profiles.id,
            profiles.segment,
            products.id,
            products.category,
            products.subcategory,
            products.subsubcategory,
            products.targetaudience
        FROM profiles_previously_viewed
            INNER JOIN profiles ON
                profiles_previously_viewed.profid = profiles.id
            INNER JOIN products ON
                profiles_previously_viewed.prodid = products.id
        WHERE profiles.id = '{profid}'
        """)
        # Je wilt alles fetchen van de query die je hebt uitgevoerd
        rows = cur.fetchall()

        # Forloop die alles in elke row steeds alle colums af gaat. Per column die je hebt, moet je een {r[index]}
        # toevoegen om hem te printen

        for r in rows:
            # max aantal producten van cat-subcat-subsubcat
            max = 10

            cat= r[3]
            subcat= r[4]
            subsubcat = r[5]

            print(f"\n{r[3]} - {r[4]} - {r[5]}:")
            cur.execute(f"""            
                SELECT id,name,category,subcategory,subsubcategory FROM products
                WHERE category = '{cat}'
                AND subcategory = '{subcat}'
                AND subsubcategory = '{subsubcat}'
            """)
            rec = cur.fetchall()
            for y in rec:
                if 0 == max:
                    break

                print(y)
                max-=1

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

#same_cat_rec('59dceb92a56ac6edb4d8b34a')
#same_cat_rec('59dcec16a56ac6edb4d93f68')
#same_cat_rec('59dcea9ba56ac6edb4d7ab18')