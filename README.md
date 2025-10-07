# Reconocimiento de Dígitos - MNIST

Este proyecto es un sistema de reconocimiento de dígitos basado en el conjunto de datos MNIST. Incluye un modelo de red neuronal convolucional (CNN) para clasificar dígitos, una interfaz gráfica de usuario (GUI) para reconocimiento en tiempo real, e integración con Firebase para almacenar imágenes. El sistema permite a los usuarios dibujar dígitos, cargar imágenes o arrastrarlas y soltarlas para predecir dígitos (0-9) y, opcionalmente, subirlas a Firebase Storage.

## Características

- **Entrenamiento del Modelo**: Entrena un modelo CNN con el conjunto de datos MNIST para reconocer dígitos escritos a mano.
- **Interfaz Gráfica (GUI)**: Interfaz basada en Tkinter con soporte para arrastrar y soltar, que permite:
  - Dibujar dígitos en un lienzo.
  - Cargar imágenes desde archivos.
  - Predecir dígitos usando el modelo entrenado.
  - Subir imágenes a Firebase Storage y ver la URL pública.
- **Procesamiento de Imágenes**: Preprocesa imágenes para que coincidan con el formato MNIST (28x28 en escala de grises, normalizado).
- **Integración con Firebase**: Sube imágenes a Firebase Storage y obtiene URLs públicas.
- **Herramientas de Depuración**: Scripts para evaluar el modelo y depurar el preprocesamiento de imágenes.
- **Pruebas Unitarias**: Tests para componentes clave (modelo, predictor, procesador de imágenes, cargador de Firebase y GUI).


## Requisitos

- Python 3.8 o superior
- Dependencias (ver `requirements.txt`):
  - `tensorflow>=2.0`
  - `keras>=2.0`
  - `firebase-admin>=6.0`
  - `numpy>=1.19`
  - `pillow>=8.0`
  - `matplotlib>=3.3`
  - `pyrebase4>=4.5` (opcional, para compatibilidad con Firebase)
  - `tkinterdnd2>=0.3` (para funcionalidad de arrastrar y soltar)
- Un proyecto de Firebase con Storage habilitado y un archivo JSON de credenciales de servicio

## Instalación

1. **Clonar el repositorio**:
   
   git clone <url-del-repositorio>
   cd reconocimiento-digitos-mnist

2. **Crear un entorno virtual (opcional, pero recomendado)**: 
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate

3. **Instalar las dependencias**:
   pip install -r requirements.txt

4. **Configurar Firebase**:
- Crea un proyecto en console.firebase.google.com.
- Habilita Firebase Storage.
- Genera una clave de cuenta de servicio (JSON) y    colócala en la raíz del proyecto.
- Asegúrate de que las rutas de firebase_cred y firebase_bucket en main.py y src/gui.py sean correctas.


## Uso

1. **Entrenar el Modelo**:
- Para entrenar el modelo CNN en el conjunto de datos MNIST:
   python scripts/train_model.py
- Carga el conjunto de datos MNIST, entrena el modelo hasta por 10 épocas y guarda el mejor modelo en models/best_model.h5 y el modelo final en model.h5.
- Utiliza detención temprana (early stopping) para evitar el sobreajuste y muestra la arquitectura del modelo.

2. **Evaluar el Modelo**:
- Para evaluar el modelo entrenado en el conjunto de prueba de MNIST:
   python scripts/eval_model_on_mnist.py
- Muestra la precisión del modelo en el conjunto de prueba y un resumen de la arquitectura.

3. **Depurar una Imagen Individual**:
- Para preprocesar y predecir una sola imagen:
   python scripts/debug_single_image.py ruta/a/imagen.jpg
- Preprocesa la imagen, guarda la versión procesada como debug_processed.png y muestra las probabilidades predichas y el dígito.

4. **Ejecutar la GUI**:
- Para lanzar la interfaz gráfica:
   python main.py
- Funcionalidades: 
      * Dibuja dígitos en el lienzo con el ratón.
      * Haz clic en "Predecir" para predecir el dígito dibujado.
      * Haz clic en "Cargar Imagen" para cargar una imagen desde un archivo.
      * Arrastra y suelta una imagen en la ventana.
      * Haz clic en "Limpiar" para borrar el lienzo.
      * Si Firebase está configurado, las imágenes se suben y se muestra una URL pública clickable.
- Requisitos: Asegúrate de que model.h5 exista (entrena el modelo primero si es necesario) y que las credenciales de Firebase estén configuradas.

5. **Ejecutar Pruebas Unitarias**:
- Para ejecutar las pruebas unitarias de los componentes:
      python -m unittest discover tests
- Las pruebas cubren el modelo, el predictor, el procesador de imágenes, el cargador de Firebase y la inicialización de la GUI.


## Proprocesamiento de Imágenes 

- El módulo src/image_processor.py preprocesa imágenes para que coincidan con el formato MNIST:
      1. Convierte a escala de grises (0-255).
      2. Invierte si el fondo es claro (intensidad media > 127).
      3. Aplica autocontraste para mejorar la separación.
      4. Usa un desenfoque gaussiano para reducir artefactos de redimensionamiento.
      5. Aplica umbralización de Otsu para binarizar.
      6. Dilata para engrosar trazos finos.
      7. Recorta al cuadro delimitador del dígito.
      8. Escala proporcionalmente para que el lado máximo sea de 20 píxeles.
      9. Centra el dígito en un lienzo de 28x28 usando el centro de masa.
      10. Normaliza los valores de píxeles a [0,1] y da forma (1, 28, 28, 1).


## Arquitectura del Modelo

- El modelo CNN (src/model.py y scripts/train_model.py) consta de:
   * Entrada: Imágenes en escala de grises (28, 28, 1)
   * Capas:
      * Conv2D (32 filtros, 3x3, ReLU)
      * MaxPooling2D (2x2)
      * Conv2D (64 filtros, 3x3, ReLU)
      * MaxPooling2D (2x2)
      * Conv2D (64 filtros, 3x3, ReLU)
      * Flatten
      * Dense (64 unidades, ReLU)
      * Dense (10 unidades, softmax)
   * Optimizador: Adam
   * Pérdida: Entropía cruzada categórica dispersa
   * Métrica: Precisión


## Integración con Firebase

- El módulo src/firebase_utils.py gestiona la subida de imágenes a Firebase Storage:
   * Inicializa Firebase con una clave de cuenta de servicio.
   * Sube imágenes al bucket especificado con un nombre de archivo que incluye una marca de tiempo.
   * Devuelve una URL pública para la imagen subida.


## Notas

* Credenciales de Firebase: Asegúrate de que la ruta de firebase_cred apunte a un archivo JSON de cuenta de servicio válido y que firebase_bucket coincida con tu bucket de Firebase Storage.
* Archivo del Modelo: La GUI y los scripts de predicción requieren que model.h5 exista. Entrena el modelo primero si no está presente.
* Depuración: Usa debug_single_image.py para inspeccionar el preprocesamiento de imágenes y las predicciones.
* Pruebas: Las pruebas unitarias aseguran que los componentes clave funcionen correctamente, pero requieren un modelo válido (model.h5) para algunas pruebas.


## Diagrama de Flujo

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






