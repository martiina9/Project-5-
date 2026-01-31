# 📝 Task Manager a automatizované testy

Jednoduchá Python aplikace pro správu úkolů s CRUD operacemi a sledovaním statusu úkolů, s MySQL databází a automatizovanými testy.

---

### 🗂 Struktura projektu
<img width="372" height="342" alt="image" src="https://github.com/user-attachments/assets/973da397-cdbf-4699-802e-872e3b64181e" />


- Ve složce src se nachází main script pro aplikaci Task Manager a skript funkcí vytvořených pro testování
- Ve složce tests se nachází testovací skripty a skript pro vytvoření a nastavení testovací databáze v MySQL
  
---
### 📋 Požadavky
- Python 3,8+
- MySQL
- mysql-connector-python
- pytest (pro testování)
---  
### 🛠️ Postup

1. Klonuj repozitář
  ```
  git clone <url-repo>
  cd task_manager
```
3. Vytvoř virtuální prostředí
  ```
  python -m venv venv
  # Linux/Mac
  source venv/bin/activate
  # Windows
  venv\Scripts\activate
```
 3. Nainstaluj requirements
  ```
  pip install -r requirements.txt
```

---
## 📝 Task Manager

### 🚀 Funkce

-  ✅ Přidávání nových úkolů  
-  📋 Zobrazení všech úkolů  
-  🔄 Aktualizace stavu úkolu: `not started` | `in process` | `done`  
-  ❌ Mazání úkolů

### ▶️ Spuštění aplikace:    
```
python src/task_manager.py
```
- Postupuj podle pokynů v terminálu  
- Přidávej, prohlížej, aktualizuj a maž úkoly  
- Ověř si data tabulce task_crud v MySQL  

---
## 🧪 Testování

📌 Poznámky:  
- Testování pomocí Pytest pro automatizované testy
- Protože původní skript Task Manageru obsahuje funkce s input() a print(), jsou vytvořené samostatné funkce pro testování
- V MySQL se vytvoří samostatná testovací databáze, používa se mysql.connector pro připojení k ní
- Každá funkce má 1 pozitivní ✅ a 1 negativní test ❌
- Výsledkem testů je True/False pro úspěch každé operace
- Po každém testu se obsah tabulky vytvořené pro testování vymaže
  
  
  
⚡ Testují funkce:  
  - Přidání úkolu do databáze (add_task_to_db)
  - Aktualizace statusu úkolu (update_task_status)
  - Odstranění úkolu (remove_task_from_db)
  - Testovací databáze a tabulky pro unit testy



### 🧪 Spuštění testů
```
  python -m pytest -v #pro podrobnější výsledky
  python -m pytest  #pro stručné výsledky
```

