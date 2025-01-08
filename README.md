
# FinancialPy

FinancialPy este o aplicație web interactivă care simulează o platformă de trading, oferind utilizatorilor posibilitatea de a investi într-un mediu virtual, folosind un cont paper account. Aplicația permite căutarea și explorarea diverselor stock-uri, iar pentru fiecare stock selectat, utilizatorii pot accesa o pagină dedicată cu informații detaliate, inclusiv un grafic al evoluției prețului, un tabel cu prețurile actuale și sugestii oferite de botul integrat. Botul nostru, Budescu, adaugă o notă interactivă, oferind predicții și recomandări personalizate pentru fiecare stock. FinancialPy include și un portofoliu virtual, unde utilizatorii pot urmări performanța stock-urilor „achiziționate” și pot vedea marja de profit aferentă fiecărei investiții. De asemenea, aplicația permite gestionarea completă a tranzacțiilor, utilizatorii având opțiuni de cumpărare și vânzare a stock-urilor, iar balanța contului virtual se actualizează automat după fiecare operațiune. Proiectul este conceput pentru a oferi o experiență educativă și realistă, fiind un instrument ideal pentru cei care doresc să învețe și să exerseze investițiile pe piața de capital.


Link github: https://github.com/rares567/IA4-homework.git

Limbaje/tehnologii folosite: Jinja, Flask, SQLite3, AlpacaAPI

Pentru a utiliza aplicația, începe prin actualizarea căii către mediul virtual și rulează scriptul run_all.py pentru a inițializa baza de date si a da run aplicatiei. Apoi o poti accesa la http://127.0.0.1:5000/. Introdu numele sau simbolul unui stock în bara de căutare și apasă Enter. După afișarea rezultatului, apasă butonul albastru View pentru a accesa pagina dedicată stock-ului, unde vei găsi un grafic al evoluției prețului, un tabel cu prețurile actuale și bot-ul Budescu, care oferă predicții despre stock. Tot aici poți achiziționa stock-uri selectând un număr care nu depășește balanța virtuală, iar apoi vei fi redirecționat către portofoliu, unde poți urmări evoluția acestora. Dacă dorești să vinzi, din pagina portofoliului poți reveni la pagina stock-ului, unde sub opțiunea Buy vei găsi opțiunea Sell. După vânzare, balanța se actualizează automat. Această aplicație este dedicată învățării și practicii pentru piața reală de capital.

Contribuție individuală:

Rizea Eduard a făcut bot-ul si a contribuit la baza de date.

Manda Ștefan a implementat frontend-ul.

Bănilă Rareș a făcut portofoliul de stock-uri si backend-ul. 

Probleme întampinate: API-ul a fost kinda outdated și a trebuit să ne mulăm pe el.
Git-ul cu request-uri-le de pull și merge și conflictele au fost o problemă aparte.
Restul problemelor pot fi considerate inconveniente minore.
