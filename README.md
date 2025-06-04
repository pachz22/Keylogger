# 🧠 Windows Keylogger con Información del Sistema y Webhook

Este proyecto es un **keylogger** para Windows escrito en Python. Captura pulsaciones de teclas, información del sistema y actividad de ventanas, enviando los datos a un **webhook de Discord**.

> ⚠️ **Advertencia**: Este proyecto es solo para fines **educativos**, **de pruebas personales** o como ejemplo de desarrollo. El uso indebido de este software puede violar leyes locales e internacionales. **Eres el único responsable de cómo utilices este código.**

---

## ✨ Características

- 🔐 Captura pulsaciones del teclado (keylogger).
- 🪟 Muestra el título de la ventana activa.
- 📄 Guarda logs localmente y los envía automáticamente.
- 🖥️ Recopila información del sistema:
  - Nombre del equipo
  - Nombre de usuario
  - IP pública
  - SO y versión
  - Procesos activos
- 🔗 Envío automático de datos al iniciar vía [Discord Webhook](https://discord.com/developers/docs/resources/webhook).
- 🎨 Uso de `Embed` para mejor presentación visual en Discord.
- 🧾 Archivo de log cifrado por UUID aleatorio.
- 🧙 Silencioso: oculta la consola al ejecutarse.

---

## 🧰 Requisitos

- Python 3.6+
- Paquetes:

```bash
pip install dhooks pynput psutil requests pywin32
