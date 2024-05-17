from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages

# biblioteca para renderizar mapas
import folium
from pumaguaAPP.models import bebederos
from pumaguaAPP.models import Reporte


# Queries para busquedas específicas
from django.db.models import Q

# Geolocalización
from folium.plugins import LocateControl

# codificador y decodificador para archivos JSON
import json
import os


# Create your views here.
def index(request):
    # Consuta de todos los bebederos para mostrarlos en el mapa
    datosBebederos = bebederos.objects.all()
    # Creamos el mapa con los parámetros correspondientes
    m = folium.Map(location=[19.32, -99.18], zoom_start=13, height=500)
    LocateControl().add_to(m)

    # Se lee el archivo JSON de las rutas del pumabus y se traza un camino en el mapa
    with open("rutas_pumabus.json") as json_file:
        parseo_rutas = json.load(json_file)

    # Se agrega cada ruta del pumabus a la capa del mapa que muestra las rutas
    gr1 = folium.FeatureGroup(name="Ruta 1", show=False).add_to(m)
    folium.PolyLine(
        parseo_rutas[0]["coordenadas"],
        tooltip="Ruta 1",
        color="#bdd348",
        stroke=True,
        weight=5,
    ).add_to(gr1)

    gr2 = folium.FeatureGroup(name="Ruta 2", show=False).add_to(m)
    folium.PolyLine(
        parseo_rutas[1]["coordenadas"],
        tooltip="Ruta 2",
        color="#ffe32c",
        stroke=True,
        weight=5,
    ).add_to(gr2)

    gr3 = folium.FeatureGroup(name="Ruta 3", show=False).add_to(m)
    folium.PolyLine(
        parseo_rutas[2]["coordenadas"],
        tooltip="Ruta 3",
        color="#015c3a",
        stroke=True,
        weight=5,
    ).add_to(gr3)

    gr4 = folium.FeatureGroup(name="Ruta 4", show=False).add_to(m)
    folium.PolyLine(
        parseo_rutas[3]["coordenadas"],
        tooltip="Ruta 4",
        color="#714c27",
        stroke=True,
        weight=5,
    ).add_to(gr4)

    gr5 = folium.FeatureGroup(name="Ruta 5", show=False).add_to(m)
    folium.PolyLine(
        parseo_rutas[4]["coordenadas"],
        tooltip="Ruta 5",
        color="#02a8db",
        stroke=True,
        weight=5,
    ).add_to(gr5)

    gr6 = folium.FeatureGroup(name="Ruta 6", show=False).add_to(m)
    folium.PolyLine(
        parseo_rutas[5]["coordenadas"],
        tooltip="Ruta 6",
        color="#e46b2d",
        stroke=True,
        weight=5,
    ).add_to(gr6)

    gr7 = folium.FeatureGroup(name="Ruta 7", show=False).add_to(m)
    folium.PolyLine(
        parseo_rutas[6]["coordenadas"],
        tooltip="Ruta 7",
        color="#d9992f",
        stroke=True,
        weight=5,
    ).add_to(gr7)

    gr8 = folium.FeatureGroup(name="Ruta 8", show=False).add_to(m)
    folium.PolyLine(
        parseo_rutas[7]["coordenadas"],
        tooltip="Ruta 8",
        color="#013555",
        stroke=True,
        weight=5,
    ).add_to(gr8)

    gr9 = folium.FeatureGroup(name="Ruta 9", show=False).add_to(m)
    folium.PolyLine(
        parseo_rutas[8]["coordenadas"],
        tooltip="Ruta 9",
        color="#6d1829",
        stroke=True,
        weight=5,
    ).add_to(gr9)

    gr10 = folium.FeatureGroup(name="Ruta 10", show=False).add_to(m)
    folium.PolyLine(
        parseo_rutas[9]["coordenadas"],
        tooltip="Ruta 10",
        color="#261c15",
        stroke=True,
        weight=5,
    ).add_to(gr10)

    gr11 = folium.FeatureGroup(name="Ruta 11", show=False).add_to(m)
    folium.PolyLine(
        parseo_rutas[10]["coordenadas"],
        tooltip="Ruta 11",
        color="#4c4e8f",
        stroke=True,
        weight=5,
    ).add_to(gr11)

    gr12 = folium.FeatureGroup(name="Ruta 12", show=False).add_to(m)
    folium.PolyLine(
        parseo_rutas[11]["coordenadas"],
        tooltip="Ruta 12",
        color="#BD7EB4",
        stroke=True,
        weight=5,
    ).add_to(gr12)

    gr13 = folium.FeatureGroup(name="Ruta 13", show=False).add_to(m)
    folium.PolyLine(
        parseo_rutas[12]["coordenadas"],
        tooltip="Ruta 13",
        color="#8FD7D4",
        stroke=True,
        weight=5,
    ).add_to(gr13)

    bicipuma = folium.FeatureGroup(name="Ruta Bicipuma", show=False).add_to(m)
    folium.PolyLine(
        parseo_rutas[13]["coordenadas"],
        tooltip="Ruta Bicipuma",
        color="#00C528",
        stroke=True,
        weight=5,
    ).add_to(bicipuma)

    folium.LayerControl().add_to(m)

    mensaje = ""

    # Capturamos si se está buscando algun bebedero en la barra de búsqueda
    if "q" in request.GET:
        # obtenemos que es lo que se está buscando
        q = request.GET["q"]
        # Buscacmos con una consulta multiple si existen coincidencias
        multiple_q = Q(
            Q(nombre__icontains=q)
            | Q(ubicacion__icontains=q)
            | Q(institucion__icontains=q)
            | Q(palabras_clave__icontains=q)
        )
        data = bebederos.objects.filter(multiple_q)

        # si no se encuentra un resultado se notifica
        if data.count() == 0:
            mensaje = "No se encontraron bebederos."
        # Si se encuentra un resultado este se muestra en el mapa
        else:
            mensaje = "Mostrando " + str(data.count()) + " bebederos."
        # Iteramos los resultado que concidieron con la búsqueda y se muestran en el mapa
        for coordenada in data:
            datos = (coordenada.latitud, coordenada.longitud)
            folium.Marker(
                datos,
                tooltip=coordenada.nombre,
                popup="<h5><b>"
                + coordenada.nombre
                + "</b></h5>\n"
                + "<h4>Ubicación: "
                + coordenada.ubicacion
                + "</h4>"
                + '<img src="'
                + imagenes_bebederos(coordenada.id_bebedero)
                + '" width="150px">'
                + '<a href="https://www.google.com"> Hola Marco  </a>',
                icon=folium.Icon(icon="glyphicon glyphicon-remove-circle", color="red"),
            ).add_to(m)
    # Caso en donde no se busca nada y se le muestra al ususario el mapa con todos los bebederos
    else:
        mensaje = "Mostrando todos los bebederos disponibles en CU."
        for coordenada in datosBebederos:
            datos = (coordenada.latitud, coordenada.longitud)
            folium.Marker(
                datos,
                tooltip=coordenada.nombre,
                popup=f"""<h5><b>{coordenada.nombre}</b></h5>
                <h4>Ubicación: {coordenada.ubicacion}</h4>
                <img src="{imagenes_bebederos(coordenada.id_bebedero)}"
                width="150px" style="border-radius: 8px"> <a href="https://www.youtube.com" targer="_blank">llink</a>""",
                icon=folium.Icon(icon="glyphicon glyphicon-tint"),
            ).add_to(m)

    f = folium.Figure(height=500)
    f.add_child(m)
    contexto = {"map": m._repr_html_(), "feedback_resultados": mensaje}

    return render(request, "index.html", contexto)


def imagenes_bebederos(id_bebedero):
    ruta = "static/pumaguaAPP/"
    imagen = str(id_bebedero) + ".jpg"
    if os.path.exists(os.getcwd() + ruta + imagen):
        ruta = ruta + imagen
    else:
        ruta = ruta + "default.png"
    return ruta

def cargaReportes(request):
    # Obtener todos los bebederos de la base de datos
    bebederos_list = bebederos.objects.values_list('id_bebedero', 'nombre')
    # print(bebederos_list)
    # Pasar los nombres de los bebederos al contexto del template
    context = {
        'bebederos': bebederos_list
    }
    if request.method == 'POST':
        # mandar a inicio.
        print(request.POST)    
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        id_bebedero = request.POST.get('bebedero')
        
        bebedero = bebederos.objects.get(pk=id_bebedero)
        reporte = Reporte(nombre=nombre, email=email, bebedero=bebedero)
        reporte.save()
        messages.success(request, "Formulario enviado correctamente")        
        return redirect(to="pumaguaAPP:cargaReportes")
       
    return render(request, 'reportes.html', context)    


def nombre1(request):
    return render(request, "nombre1.html")


def nombre2(request):
    return render(request, "nombre2.html")
