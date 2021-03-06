import psycopg2 as pysql
##########################
# Colin van Lienden
# rec-engine
##########################


#########################
## MEEST BEKENEN REC   ##
#########################
#Slaat data op in een tabel!
def most_viewed():
    'Slaat een lijst met meest verkochten producten op in een nieuwe tabel in de database'
    try:
        # Connect met de database
        conn = pysql.connect(
            host='localhost',  # De host waarop je database runt
            database='DATABASENAME',  # Database naam
            user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
            password='PASSWORD'  # Wachtwoord die je opgaf bij installatie
            # port=5432 runt standaard op deze port en is alleen nodig als je de port handmatig veranderd
        )
        #Cursor
        cur = conn.cursor()
        print("\nConnection established")

        # Uitvoer query
        #Maak gebruik van een nieuwe tabel voor het opslaan van data
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


#########################
## SAME CATOGORY REC   ##
#########################
# Alleen in print !!
def same_cat_rec(profid):
    'Laat producten zien die overheen komen met de catogory waarnaar de klant heeft gezocht'
    try:
        # Connect met de database
        conn = pysql.connect(
            host='localhost',  # De host waarop je database runt
            database='DATABASENAME',  # Database naam
            user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
            password='PASSWORD'  # Wachtwoord die je opgaf bij installatie
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
            products.subsubcategory
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
            #Zoeken naar producten met het zelfde cat, subcat, subsubcat
            cur.execute(f"""            
                SELECT id,name,category,subcategory,subsubcategory FROM products
                WHERE category = '{cat}'
                AND subcategory = '{subcat}'
                AND subsubcategory = '{subsubcat}'
            """)

            records = cur.fetchall()
            #print aantal producten uit de data van hierboven
            for y in records:
                if 0 == max:
                    break

                print(y)
                max-=1

    except pysql.OperationalError as x:
        print(f"Connection error : {x}")

    finally:
        # commit inserts
        # conn.commit()
        # Sluit de cursor
        cur.close()
        # sluit connectie
        conn.close()
        print("\nConnection closed")
#test data
#same_cat_rec('59dceb92a56ac6edb4d8b34a')
#same_cat_rec('59dcec16a56ac6edb4d93f68')
#same_cat_rec('59dcea9ba56ac6edb4d7ab18')

#######################
## SEGMENT REC       ##
#######################
# Alleen in print !!
def same_seg_rec(profid):
    'Laat producten zien die overheen komen met het segment van de klant (meest verkochten producten van dat segtment)'
    try:
        # Connect met de database
        conn = pysql.connect(
            host='localhost',  # De host waarop je database runt
            database='DATABASENAME',  # Database naam
            user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
            password='PASSWORD'  # Wachtwoord die je opgaf bij installatie
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
            products.id
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

        print('Andere kochten ook:')
        for r in rows:
            # max aantal producten meest bekeken door segment overeenkomst
            max = 10
            #print(r)
            cur.execute(f"""
            SELECT
                profiles.segment,
                products.id,
                COUNT(*) AS aantal
            FROM profiles_previously_viewed
                INNER JOIN profiles ON
                    profiles_previously_viewed.profid = profiles.id
                INNER JOIN products ON
                    profiles_previously_viewed.prodid = products.id
            WHERE profiles.segment = '{r[1]}'
            GROUP BY profiles.segment, products.id
            HAVING COUNT(*) > 1
            ORDER BY aantal DESC
            """)

            records = cur.fetchall()
            #print aantal producten uit de data van hierboven
            for y in records:
                if 0 == max:
                    break

                print(y[1])
                max-=1
            break


    except pysql.OperationalError as x:
        print(f"Connection error : {x}")

    finally:
        # commit inserts
        # conn.commit()
        # Sluit de cursor
        cur.close()
        # sluit connectie
        conn.close()
        print("\nConnection closed")

#test data
#same_seg_rec('59dceb92a56ac6edb4d8b34a')
#same_seg_rec('59dcec16a56ac6edb4d93f68')
#same_seg_rec('59dcea9ba56ac6edb4d7ab18')
