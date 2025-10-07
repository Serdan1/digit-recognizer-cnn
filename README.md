# Proyecto MNIST Dashboard

## Descripción
Este proyecto implementa una aplicación de reconocimiento de dígitos manuscritos utilizando una Red Neuronal Convolucional (CNN) entrenada con el dataset MNIST. La aplicación permite cargar, arrastrar o pintar imágenes de dígitos dibujados (por ejemplo, hechos en Paint), procesarlas automáticamente y obtener una predicción precisa..

Además, las imágenes procesadas se suben automáticamente a Firebase Storage, obteniendo una URL pública.

La interfaz gráfica está desarrollada con Tkinter y extendida con tkinterdnd2 para permitir drag-and-drop de imágenes directamente en la ventana.

## Características
- Predicción de dígitos manuscritos con una CNN entrenada (precisión MNIST 97-98%).
- Interfaz gráfica interactiva con:
   Lienzo para dibujar números.
   Carga manual de imágenes.
   soporte de arrastrar y soltar (Drag & Drop).
- Integración con Firebase Storage para almacenar y compartir imágenes mediante URLs públicas.
- Preprocesamiento robusto de imágenes (binarización, centrado, escalado proporcional).
- Mensajes de depuración en consola para facilitar el desarrollo y diagnóstico


## Requisitos
- **Python 3.8 o superior**
- Librerías requeridas (instalables vía `pip`):
  - `tensorflow` (para el modelo CNN)
  - `keras` (integrado con TensorFlow)
  - `firebase-admin` (para interacción con Firebase Storage)
  - `numpy` (para cálculos matriciales)
  - `pillow` (para procesamiento de imágenes)
  - `matplotlib` (para visualización durante el entrenamiento)
  - `pyrebase4` (para autenticación Firebase, opcional)
  - `tkinterdnd2` (para drag-and-drop en Tkinter)
- Una cuenta de Firebase con credenciales (`firebase-credentials.json`) configurada.

- pip install -r requirements.txt

## Instalación

### Clonar el repositorio
1. Asegúrate de tener Git instalado.
2. Clona el repositorio:
   git clone https://github.com/Serdan1/proyecto-mnist-dashboard.git
   cd proyecto-mnist-dashboard
   pip install tensorflow keras firebase-admin numpy pillow matplotlib pyrebase4 tkinterdnd2

3. Configura Firebase:
- Ve a la consola de Firebase, selecciona tu proyecto, y genera un archivo de servicio (`firebase-credentials.json`).
- Coloca este archivo en la carpeta `config/` del proyecto.



### Generar el modelo
1. Entrenar el modelo
- python scripts/train_model.py
Esto descargará MNIST, entrenará una CNN (32-64-64 filters + Dense) y guardará el modelo como: model.h5
2. Evaluar el modelo 
- python scripts/eval_model_on_mnist.py
  Si es correcto verás: MNIST test accuracy: 0.97...



## Uso
1. Ejecuta la aplicación:
  python main.py
2. Dibujar un número en el canvas y hacer clic en “Predecir”.
   → Se mostrará el dígito reconocido y se subirá a Firebase.
3. Cargar imagen desde tu equipo:
   Haz clic en “Cargar Imagen” y selecciona un .png o .jpg.
4. Arrastrar y soltar imágenes sobre la ventana.
   Ideal para imágenes hechas en Paint u otro editor.
5. Abrir la URL generada para ver la imagen en  Firebase Storage.
  

## Estructura del Proyecto
digit-recognizer-cnn/
│
├── src/
│   ├── gui.py                  # Interfaz gráfica (Tkinter)
│   ├── predictor.py            # Carga del modelo y realiza predicciones
│   ├── image_processor.py      # Procesamiento de imágenes
│   ├── firebase_utils.py       # Integración con Firebase Storage
│   ├── model.py               # Definición y entrenamiento del modelo CNN
│
├── scripts/
│   ├── train_model.py         # Entrena y guarda el modelo (model.h5)
│   ├── eval_model_on_mnist.py # Evalúa el modelo en el dataset oficial MNIST
│   ├── debug_single_image.py  # Evalúa el modelo con una sola imagen (pruebas)
│
├── tests/
│   ├── test_model.py          # Tests para el modelo
│   ├── test_predictor.py      # Tests para las predicciones
│   ├── test_gui.py            # Tests para la interfaz gráfica
│
├── proyecto-mnist-dashboard-firebase-adminsdk-fbsvc-57d1f6e9be.json # Credenciales de Firebase
├── main.py                    # Punto de entrada para ejecutar la GUI
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Documentación del proyecto

## Desempeño
- Precisión modelo CNN (MNIST test): ~97–98% tras 5–10 épocas.
- Tiempo de predicción: ~70 ms por imagen en CPU estándar.
- Subida Firebase: depende de conexión (<1 s normalmente).
- Procesamiento imagen personalizada: centrado + binarización → mejora notablemente la precisión con dibujos externos.


## Contribución
1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad:
   git checkout -b feature/nueva-funcionalidad
3. Realiza tus cambios y confirma:
   git add .
   git commit -m "Descripción de los cambios"
4. Envía la rama:
   git push origin feature/nueva-funcionalidad
5. Abre un Pull Request en GitHub.


## Notas de Desarrollador
- El pipeline de preprocesamiento adapta las imágenes externas para que se asemejen a los dígitos MNIST:
      Fondo negro / dígito blanco.
      Escalado proporcional a 20px.
      Centrado en base al centro de masa.
- El modelo utiliza ReLU en convolucionales y softmax en la salida.
- No se utiliza dropout en la versión final (puedes añadirlo fácilmente para robustez extra).
- Se imprimen los Top 3 resultados en consola para depurar casos ambiguos.



## Diagrama del Funcionamiento del Sistema
```mermaid
flowchart TD
    A[👤 Usuario] -->|Dibuja/Carga/Arrastra imagen| B[🖼 GUI Tkinter]
    B -->|Preprocesa imagen| C[🧪 image_processor.py]
    C --> D[🤖 predictor.py]
    D -->|Realiza predicción| E[📊 Modelo CNN - model.h5]
    E --> D
    D -->|Muestra resultado| B
    B -->|Sube imagen| F[☁️ Firebase Storage]
    F -->|Devuelve URL| B
    B -->|Muestra resultado| A

##Proyecto finalizado y funcional:
- CNN correctamente entrenada
- Predicciones precisas con imágenes externas
- GUI interactiva con Firebase integrada