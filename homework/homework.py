"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel
import pandas as pd
import zipfile
import os


def clean_campaign_data():
    #crear el dataframe para ingresar los datos
    clientes = pd.DataFrame(columns=["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"])
    campaign= pd.DataFrame(columns=["client_id", "number_contacts", "contact_duration", "previous_campaign_contacts", "previous_outcome", "campaign_outcome", "last_contact_date"])
    economics = pd.DataFrame(columns=["client_id", "cons_price_idx", "euribor_three_months"])

    #Primero ingresar los datos en el dataframe y después realizar la limpieza
    directorio="files/input/"
    for archivo in os.listdir(directorio):
        ruta_zip=os.path.join(directorio,archivo)
        with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
            # Listar archivos en el ZIP
            nombres_archivos = zip_ref.namelist()
            zip=pd.read_csv(zip_ref.open(nombres_archivos[0]), sep=",", header=0)
            columnas_clientes= clientes.columns.intersection(zip.columns)
            clientes = pd.concat([clientes, zip[columnas_clientes]], ignore_index=True)

            zip["last_contact_date"] = "2022"  + "-" + zip["month"].map(str) + "-"+zip["day"].map(str)
            columnas_campaign= campaign.columns.intersection(zip.columns)
            campaign = pd.concat([campaign, zip[columnas_campaign]], ignore_index=True)

            columnas_economics= economics.columns.intersection(zip.columns)
            economics = pd.concat([economics, zip[columnas_economics]], ignore_index=True)
    
    #limpiar los datos
    #clientes
    clientes["job"] = clientes["job"].str.replace(".", "")
    clientes["job"] = clientes["job"].str.replace("-", "_")
    clientes["education"] = clientes["education"].str.replace(".", "_")
    clientes["education"] = clientes["education"].str.replace("unknown", "pd.NA")
    clientes["credit_default"] = clientes["credit_default"].map(lambda x: 1 if x == "yes" else 0)
    clientes["mortgage"] = clientes["mortgage"].map(lambda x: 1 if x == "yes" else 0)
    
    #campaign
    campaign["previous_outcome"] = campaign["previous_outcome"].map(lambda x: 1 if x == "success" else 0)
    campaign["campaign_outcome"] = campaign["campaign_outcome"].map(lambda x: 1 if x == "yes" else 0)
    campaign["last_contact_date"] = pd.to_datetime(campaign['last_contact_date'], format='%Y-%b-%d')

    
    #guardar los dataframes
    clientes.to_csv("files/output/client.csv", index=False)
    campaign.to_csv("files/output/campaign.csv", index=False)
    economics.to_csv("files/output/economics.csv", index=False)
    
            
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    return


if __name__ == "__main__":
    clean_campaign_data()
