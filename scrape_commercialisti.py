"""
Scraper per lista commercialisti italiani
Estrae contatti da fonti pubbliche (Pagine Gialle, Google Maps, LinkedIn)

Uso: python scrape_commercialisti.py --city "Milano" --output leads.csv
"""

import csv
import json
import re
import time
import argparse
from dataclasses import dataclass, asdict
from typing import List, Optional
import urllib.parse

@dataclass
class Lead:
    nome_studio: str
    titolare: str
    email: str
    telefono: str
    indirizzo: str
    citta: str
    fonte: str
    linkedin: str = ""
    note: str = ""

# Comuni italiani principali per targeting
CITTA_TARGET = [
    "Milano", "Roma", "Torino", "Napoli", "Bologna",
    "Firenze", "Genova", "Palermo", "Bari", "Catania",
    "Venezia", "Verona", "Padova", "Trieste", "Brescia",
    "Parma", "Modena", "Reggio Emilia", "Bergamo", "Monza"
]

def generate_google_maps_search_url(city: str) -> str:
    """Generate Google Maps search URL for commercialisti in a city"""
    query = f"commercialista {city}"
    encoded = urllib.parse.quote(query)
    return f"https://www.google.com/maps/search/{encoded}"

def generate_pagine_gialle_url(city: str) -> str:
    """Generate Pagine Gialle search URL"""
    city_slug = city.lower().replace(" ", "-")
    return f"https://www.paginegialle.it/ricerca/commercialisti/{city_slug}"

def generate_linkedin_search_url(city: str) -> str:
    """Generate LinkedIn search URL (requires login)"""
    query = f"commercialista {city}"
    encoded = urllib.parse.quote(query)
    return f"https://www.linkedin.com/search/results/people/?keywords={encoded}"

def extract_email_from_text(text: str) -> List[str]:
    """Extract email addresses from text using regex"""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return list(set(re.findall(pattern, text)))

def extract_phone_from_text(text: str) -> List[str]:
    """Extract Italian phone numbers from text"""
    patterns = [
        r'\+39\s?\d{2,4}\s?\d{6,8}',  # +39 format
        r'0\d{1,4}[\s.-]?\d{6,8}',     # Landline
        r'3\d{2}[\s.-]?\d{6,7}',       # Mobile
    ]
    phones = []
    for pattern in patterns:
        phones.extend(re.findall(pattern, text))
    return list(set(phones))

def create_manual_search_guide(cities: List[str], output_file: str = "search_guide.md"):
    """
    Create a guide for manual lead collection
    (Automated scraping of Google/PagineGialle requires API keys or may violate ToS)
    """
    
    guide = """# Guida Raccolta Lead Commercialisti

## Metodo 1: Google Maps (Più Efficace)

Per ogni città, cerca "commercialista [città]" su Google Maps.
Raccogli: Nome studio, Telefono, Email (se presente), Indirizzo.

### Link diretti:
"""
    
    for city in cities:
        url = generate_google_maps_search_url(city)
        guide += f"- [{city}]({url})\n"
    
    guide += """
## Metodo 2: Pagine Gialle

### Link diretti:
"""
    
    for city in cities:
        url = generate_pagine_gialle_url(city)
        guide += f"- [{city}]({url})\n"
    
    guide += """
## Metodo 3: LinkedIn Sales Navigator

Cerca "commercialista" + città. Filtra per "People".
Nota: Richiede account LinkedIn (Premium per messaggi diretti).

## Metodo 4: Ordine dei Commercialisti

Ogni provincia ha un albo pubblico. Esempi:
- Milano: https://www.odcec.mi.it/
- Roma: https://www.odcec.roma.it/
- Torino: https://www.odcec.torino.it/

Gli albi spesso hanno elenchi pubblici con email.

## Template CSV

Salva i lead in questo formato:
```
nome_studio,titolare,email,telefono,indirizzo,citta,fonte,linkedin,note
"Studio Rossi","Dott. Mario Rossi","m.rossi@studiorossi.it","02 1234567","Via Roma 1","Milano","Google Maps","","Specializzato PMI"
```

## Obiettivo: 100 Lead in 3 ore

- 20 minuti per città
- 5 città = 100 lead circa
- Priorità: email > telefono (per cold outreach)
"""
    
    with open(output_file, 'w') as f:
        f.write(guide)
    
    print(f"Guida salvata in {output_file}")
    return guide


def create_sample_leads_csv(output_file: str = "leads_sample.csv"):
    """Create a sample CSV with the correct structure"""
    
    sample_leads = [
        Lead(
            nome_studio="Studio Bianchi & Associati",
            titolare="Dott. Giuseppe Bianchi",
            email="info@studiobianchi.it",
            telefono="02 8901234",
            indirizzo="Via Montenapoleone 10",
            citta="Milano",
            fonte="Google Maps",
            linkedin="",
            note="Studio medio, 5 dipendenti"
        ),
        Lead(
            nome_studio="Rossi Commercialisti",
            titolare="Dott.ssa Maria Rossi",
            email="m.rossi@rossicomm.it",
            telefono="06 5678901",
            indirizzo="Via del Corso 100",
            citta="Roma",
            fonte="Pagine Gialle",
            linkedin="linkedin.com/in/mariarossi",
            note="Specializzata startup"
        ),
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=asdict(sample_leads[0]).keys())
        writer.writeheader()
        for lead in sample_leads:
            writer.writerow(asdict(lead))
    
    print(f"CSV di esempio salvato in {output_file}")


def create_email_extraction_bookmarklet():
    """
    Create a JavaScript bookmarklet to extract emails from any webpage
    Save as bookmark and click on any page to extract emails
    """
    
    js_code = """
javascript:(function(){
    var emails = document.body.innerHTML.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g);
    if(emails){
        var unique = [...new Set(emails)];
        prompt('Email trovate ('+unique.length+'):', unique.join(', '));
    }else{
        alert('Nessuna email trovata');
    }
})();
    """.strip()
    
    print("\n📌 BOOKMARKLET ESTRAZIONE EMAIL")
    print("=" * 50)
    print("Crea un nuovo bookmark nel browser e incolla questo codice come URL:")
    print()
    print(js_code)
    print()
    print("Poi clicca sul bookmark su qualsiasi pagina per estrarre le email.")
    
    return js_code


def main():
    parser = argparse.ArgumentParser(description='Tool raccolta lead commercialisti')
    parser.add_argument('--cities', nargs='+', default=CITTA_TARGET[:5], 
                       help='Città target (default: prime 5)')
    parser.add_argument('--output', default='leads.csv',
                       help='File output CSV')
    parser.add_argument('--guide', action='store_true',
                       help='Genera guida manuale')
    parser.add_argument('--sample', action='store_true',
                       help='Genera CSV di esempio')
    parser.add_argument('--bookmarklet', action='store_true',
                       help='Mostra bookmarklet estrazione email')
    
    args = parser.parse_args()
    
    print("🎯 RispostaFacile.ai - Lead Scraper")
    print("=" * 50)
    
    if args.guide:
        create_manual_search_guide(args.cities)
    
    if args.sample:
        create_sample_leads_csv(args.output)
    
    if args.bookmarklet:
        create_email_extraction_bookmarklet()
    
    if not (args.guide or args.sample or args.bookmarklet):
        # Default: genera tutto
        create_manual_search_guide(args.cities, "search_guide.md")
        create_sample_leads_csv("leads_sample.csv")
        create_email_extraction_bookmarklet()
        
        print("\n✅ File generati:")
        print("   - search_guide.md (guida raccolta lead)")
        print("   - leads_sample.csv (template CSV)")
        print("\n📊 Obiettivo: 100 lead in 3 ore")
        print("   Segui la guida e compila il CSV.")


if __name__ == "__main__":
    main()
