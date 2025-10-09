# Reconocimiento de Dígitos - MNIST

Este proyecto es un sistema de reconocimiento de dígitos basado en el conjunto de datos MNIST. Incluye un modelo de red neuronal convolucional (CNN) para clasificar dígitos, una interfaz gráfica de usuario (GUI) para reconocimiento en tiempo real, e integración con Firebase para almacenar imágenes. El sistema permite a los usuarios dibujar dígitos, cargar imágenes o arrastrarlas y soltarlas para predecir dígitos (0-9) y, opcionalmente, subirlas a Firebase Storage.

## 🌐 Demostración en Línea

Puedes probar el sistema directamente en Hugging Face Spaces sin necesidad de instalación local:

👉 [Haz clic aquí para ejecutar el sistema](https://danserrano1-digit-recognizer-cnn.hf.space/)

Este espacio está integrado con el repositorio de GitHub y carga automáticamente el modelo entrenado y la interfaz para el reconocimiento de dígitos.


## 🚀 Ejecuta el sistema localmente

Si prefieres ejecutarlo en tu equipo:

   - Clona el repositorio e instala las dependencias.

   - Configura las credenciales de Firebase (opcional).

   - Ejecuta el script principal:

         - python main.py


## Características

- Entrenamiento del Modelo: Entrena un modelo CNN con el conjunto de datos MNIST para reconocer dígitos escritos a mano.

- Interfaz Gráfica (GUI): Basada en Tkinter con soporte para arrastrar y soltar:

- Dibuja dígitos en un lienzo.

- Carga imágenes desde archivos.

- Predice dígitos con el modelo entrenado.

- Sube imágenes a Firebase Storage y obtiene una URL pública.

- Procesamiento de Imágenes: Adapta las imágenes al formato MNIST (28x28, escala de grises, normalizado).

- Integración con Firebase: Guarda las imágenes y obtiene sus URLs públicas.

- Pruebas Unitarias y Herramientas de Depuración: Validan los componentes y ayudan en el desarrollo.


## Requisitos

- Python 3.8 o superior

- Dependencias (ver requirements.txt):

- tensorflow>=2.0

- keras>=2.0

- firebase-admin>=6.0

- numpy>=1.19

- pillow>=8.0

- matplotlib>=3.3

- pyrebase4>=4.5 (opcional, para compatibilidad con Firebase)

- tkinterdnd2>=0.3 (para funcionalidad de arrastrar y soltar)

- Un proyecto de Firebase con Storage habilitado y un archivo JSON de credenciales de servicio


## Instalación

- Clonar el repositorio:

git clone <url-del-repositorio>
cd reconocimiento-digitos-mnist


- Crear un entorno virtual (opcional, pero recomendado):

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate


- Instalar las dependencias:

pip install -r requirements.txt


- Configurar Firebase:

Crea un proyecto en console.firebase.google.com
.

- Habilita Firebase Storage.

Genera una clave de cuenta de servicio (JSON) y colócala en la raíz del proyecto.

Asegúrate de que las rutas de firebase_cred y firebase_bucket en main.py y src/gui.py sean correctas.


## Uso

- Entrenar el Modelo:

python scripts/train_model.py


- Evaluar el Modelo:

python scripts/eval_model_on_mnist.py


- Depurar una Imagen Individual:

python scripts/debug_single_image.py ruta/a/imagen.jpg


- Ejecutar la GUI:

python main.py

- Ejecutar Pruebas Unitarias:

python -m unittest discover tests


## Procesamiento de Imágenes

El módulo src/image_processor.py adapta las imágenes al formato MNIST mediante:

   - Conversión a escala de grises.

   - Inversión si el fondo es claro.

   - Autocontraste y desenfoque gaussiano.

   - Umbralización (Otsu).

   - Detección y recorte del dígito.

   - Redimensionamiento proporcional (máx. 20px por lado).

   - Centrado en lienzo 28x28.

   - Normalización [0,1].


## 🧠 Arquitectura del Modelo

El modelo CNN (en src/model.py) consta de:

| **Tipo de Capa** | **Parámetros**   | **Activación** |
| ---------------- | ---------------- | -------------- |
| Conv2D           | 32 filtros (3x3) | ReLU           |
| MaxPooling2D     | (2x2)            | —              |
| Conv2D           | 64 filtros (3x3) | ReLU           |
| MaxPooling2D     | (2x2)            | —              |
| Conv2D           | 64 filtros (3x3) | ReLU           |
| Flatten          | —                | —              |
| Dense            | 64 unidades      | ReLU           |
| Dense            | 10 unidades      | Softmax        |


- Optimizador: Adam
- Pérdida: Entropía cruzada categórica dispersa
- Métrica: Precisión


## 🔥 Integración con Firebase

El módulo src/firebase_utils.py permite subir imágenes procesadas a Firebase Storage:

- Inicializa Firebase con una cuenta de servicio.

- Sube las imágenes con un nombre único (marca de tiempo).

- Devuelve una URL pública para acceso directo.


## Notas

- Asegúrate de que model.h5 exista antes de lanzar la GUI (entrena el modelo si no está presente).

- Las credenciales de Firebase deben ser válidas y apuntar al bucket configurado.

- Las pruebas unitarias requieren un modelo válido para ejecutarse correctamente.


## 🧩 Diagrama de Flujo

```mermaid
graph TD
    A[Usuario] -->|Dibuja/Carga/Arrastra| B[GUI Tkinter]
    B -->|Preprocesa imagen| C[image_processor.py]
    C -->|"Array 1,28,28,1"| D[predictor.py]
    D -->|Consulta/Inference| E[Modelo CNN - model.h5]
    E -->|Predicción| D
    D -->|Resultado| B
    B -->|Sube imagen| F[Firebase Storage]
    F -->|URL pública| B
    B -->|Muestra respuesta| A

