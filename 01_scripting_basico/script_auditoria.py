import requests
import json                                #en estas 3 librerias solo las copie y pegue de los pasados codigos
from requests.auth import HTTPBasicAuth

requests.packages.urllib3.disable_warnings()

HOST = "devnetsandboxiosxec9k.cisco.com"
USUARIO = "usuario"                        #en estas 3 partes solo lo que hice fue agregarle el contenido de lo que es ya que el profe nos dio ese para hacer pruebas
PASSWORD = "contrasena"        #aqui ya es cosa de cada quien para que funcione bueno yo lo hice con el que abrio el profe y funciono

url = "https://devnetsandboxiosxec9k.cisco.com/restconf/data/ietf-interfaces:interfaces"
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"        #este lo copie igual del documento en drive, pero como tal es lo que quiero recibir y lo que yo mando
}
auth = HTTPBasicAuth(USUARIO, PASSWORD)

try:           #era para que intentara 
    response = requests.get(url, headers=headers, auth=auth, verify=False)

    if response.status_code == 200:
        data = response.json()
        interfaces = data["ietf-interfaces:interfaces"]["interface"]

        inventario = []                     #aqui vamos a guardar las interfaces que tengan ip
        for iface in interfaces:
            direcciones = iface.get("ietf-ip:ipv4", {}).get("address", []) #busco si tiene ip la interfaz, si no va regresar una lista vacia
            if direcciones:  # solo las que tienen IP
                inventario.append({  #agrega algo al final de la lista
                    "nombre": iface.get("name"),      #el nombre de la interfz
                    "ip": direcciones[0].get("ip"),    #su ip
                    "mascara": direcciones[0].get("netmask"),# su mascara
                    "habilitada": iface.get("enabled", False)# y si esta prendida
                })

        with open("inventario_interfaces.json", "w") as archivo:  #creamos el archivo Json y guardamos ahi la lista
            json.dump(inventario, archivo, indent=4)       #me apoye con la IA y me djo que es para que se vea ordenado el JSON el indent y tambie el dump toma la lista  y la escribe en el json

        print(f"Listo: se guardaron {len(inventario)} interfaces con IP en inventario_interfaces.json")  #len lo uso para cuantos elemntos tiene la lista
    else:
        print(f"Error HTTP {response.status_code}: {response.text}")

except requests.exceptions.RequestException as e:  # es para si falla va hacer el otro
    print(f"Error de conexión: {e}")