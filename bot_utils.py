import requests
from datetime import datetime

class Bot_utils:
    
    def __init__(self) -> None:
        self.parking_names = {
            "Stazione": "Firenze_SMN",
            "Pieraccini": "Pieraccini_Meyer",
            "Fortezza": "Fortezza_Fiera",
            "Alberti": "Alberti",
            "S. Ambrogio": "S_Ambrogio",
            "Parterre": "Parterre",
            "Beccaria": "Beccaria",
            "Porta al Prato": "Porta_al_Prato",
            "Careggi": "Careggi",
            "San Lorenzo": "S_Lorenzo",
            "Binario 16": "Stazione_Binario_16",
            "Oltrarno": "Oltrarno",
            "Palazzo di Giustizia": "Palazzo_Giustizia"
        }
        self.parking_id_to_names = {
            "1": "Firenze_SMN",
            "2": "Pieraccini_Meyer",
            "3": "Fortezza_Fiera",
            "5": "Alberti",
            "6": "S_Ambrogio",
            "7": "Parterre",
            "8": "Beccaria",
            "9": "Porta_al_Prato",
            "11": "Careggi",
            "999": "S_Lorenzo",
            "4": "Stazione_Binario_16",
            "10": "Oltrarno",
            "13": "Palazzo_Giustizia"
        }
                                         
    def get_parking_occupancy_info(self) -> str:
        URL = "https://datastore.comune.fi.it/od/ParkFreeSpot.json"
        data = requests.get(URL).json()
        date = datetime.strptime(data[0].get("UpdateDate"), '%Y-%m-%dT%H:%M:%S.%f').strftime('%A %d %B, %H\:%M _UTC_')
        updateDate = f'Ultimo aggiornamento: *{date}*'
        to_ret = f'⏰{updateDate}\n\n'
        for parking in data:
            name = parking.get("Name").replace("-", "–")
            id = parking.get("Id")
            DETAILS_URL = f'https://datastore.comune.fi.it/od/ParkInfo_{self.parking_id_to_names.get(id)}.json'
            details_data = requests.get(DETAILS_URL).json()
            total_parking_spaces = 0
            total_parking_spaces_string = f""
            total_disabled_spaces = 0
            icon = "🟢"
            for info in details_data.get("BaseInfos"):
                if info.get("TypeName") == "Posti riservati ai disabili":
                    total_disabled_spaces = info.get("Info")
                feature_to_check = "Posti disponibili" if id != "3" else "Posti paganti"
                if info.get("TypeName") == feature_to_check:
                    total_parking_spaces = info.get("Info")
                    try:
                        percentage = int(parking.get("FreeSpot")) / int(total_parking_spaces) * 100
                        total_parking_spaces_string = f" su *{total_parking_spaces}* posti disponibili"
                    except:
                        total_parking_spaces_string = f""
                        percentage = 100
                    if percentage < 40 : icon = "🟡"
                    if percentage < 20 : icon = "🟠"
                    if percentage < 10 : icon = "🔴"
            to_ret += (f'\n🅿️ *{name} – 📍[Link a Google Maps](https://maps.google.it/maps?q={parking.get("Latitude")},{parking.get("Longitude")})*\n{icon}Posti liberi *{parking.get("FreeSpot")}*{total_parking_spaces_string}\n♿Posti riservati ai disabili {total_disabled_spaces}\n')
        return to_ret
    
    def get_parking_details(self, query) -> str:        
        URL = f'https://datastore.comune.fi.it/od/ParkInfo_{query.data}.json'
        data = requests.get(URL).json()
        tariffa = data.get('Contents').get('Value').replace('Tariffa', '\n\n💶 Tariffa').replace('Abbonamento', '\n\n💶 Abbonamento')
        posti_disponibili = f""
        for info in data.get("BaseInfos"):
            posti_disponibili += f"ℹ️ {info.get('TypeName')}: {info.get('Info')}\n"
        return f"Parcheggio Selezionato: {data.get('Name')}.\n\n{posti_disponibili}\n{tariffa}".replace('*', '')
    
    def get_parking_names(self):
        return self.parking_names
