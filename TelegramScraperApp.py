import customtkinter as ctk
import threading
import random
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager


class TelegramScraperApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Telegram Web K Scraper (Firefox Edition)")
        self.geometry("600x500")

        # Elementos de la Interfaz
        self.label = ctk.CTkLabel(self, text="Extractor de Usuarios - Telegram Web K", font=("Arial", 18, "bold"))
        self.label.pack(pady=20)

        self.btn_open = ctk.CTkButton(self, text="1. Abrir Firefox (Seguro)", command=self.start_browser_thread,
                                      fg_color="#FF5722", hover_color="#E64A19")
        self.btn_open.pack(pady=10)

        self.btn_scrape = ctk.CTkButton(self, text="2. Iniciar Extracción Humana", command=self.start_scrape_thread,
                                        state="disabled")
        self.btn_scrape.pack(pady=10)

        self.textbox = ctk.CTkTextbox(self, width=500, height=200)
        self.textbox.pack(pady=20)

        self.driver = None

    def log(self, message):
        self.textbox.insert("end", f"> {message}\n")
        self.textbox.see("end")

    def start_browser_thread(self):
        threading.Thread(target=self.open_browser, daemon=True).start()

    def open_browser(self):
        self.log("Configurando Firefox con medidas anti-detección...")

        options = FirefoxOptions()

        # Ajustes para parecer un usuario real y ocultar Selenium
        # 1. Cambiar el User-Agent (Mac estándar)
        options.set_preference("general.useragent.override",
                               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0")

        # 2. Desactivar la bandera de automatización (webdriver = false)
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)

        # 3. Desactivar el chequeo de compatibilidad de Marionette
        options.set_preference("marionette.enabled", True)

        try:
            service = FirefoxService(GeckoDriverManager().install())
            self.driver = webdriver.Firefox(service=service, options=options)

            self.driver.get("https://web.telegram.org/k/")
            self.btn_scrape.configure(state="normal")
            self.log("Firefox abierto. Por favor, logueate y entra a un grupo.")
            self.log("Recuerda abrir la lista de miembros antes de extraer.")
        except Exception as e:
            self.log(f"Error al abrir Firefox: {str(e)}")

    def start_scrape_thread(self):
        threading.Thread(target=self.scrape_logic, daemon=True).start()

    def scrape_logic(self):
        self.log("Iniciando extracción con pausas aleatorias...")

        try:
            # Simulamos que el script "mira" la pantalla antes de actuar
            time.sleep(random.uniform(2, 4))

            # Buscamos los elementos de la lista de miembros
            # En Web K, los nombres suelen estar en elementos con la clase '.peer-title'
            elements = self.driver.find_elements(By.CSS_SELECTOR, ".peer-title")

            if not elements:
                self.log("No se detectaron usuarios. ¿Tienes abierta la lista de miembros?")
                return

            usuarios_extraidos = []

            for index, el in enumerate(elements):
                # Cada 5 usuarios, hacemos una pausa más larga para simular lectura humana
                if index % 5 == 0 and index > 0:
                    time.sleep(random.uniform(1.5, 3))

                nombre = el.text
                if nombre and nombre not in usuarios_extraidos:
                    usuarios_extraidos.append(nombre)
                    self.textbox.insert("end", f"Encontrado: {nombre}\n")
                    self.textbox.see("end")

            self.log(f"Fin del proceso. Total: {len(usuarios_extraidos)} usuarios visibles.")

        except Exception as e:
            self.log(f"Error durante el scraping: {str(e)}")


if __name__ == "__main__":
    app = TelegramScraperApp()
    app.mainloop()