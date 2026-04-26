import customtkinter as ctk
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time


class TelegramScraperApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Telegram Web K Scraper")
        self.geometry("500x400")

        # UI Elements
        self.label = ctk.CTkLabel(self, text="Extractor de Usuarios Telegram Web K", font=("Arial", 16))
        self.label.pack(pady=20)

        self.btn_open = ctk.CTkButton(self, text="1. Abrir Navegador", command=self.start_browser_thread)
        self.btn_open.pack(pady=10)

        self.btn_scrape = ctk.CTkButton(self, text="2. Iniciar Extracción", command=self.start_scrape_thread,
                                        state="disabled")
        self.btn_scrape.pack(pady=10)

        self.textbox = ctk.CTkTextbox(self, width=400, height=150)
        self.textbox.pack(pady=20)

        self.driver = None

    def start_browser_thread(self):
        threading.Thread(target=self.open_browser, daemon=True).start()

    def open_browser(self):
        options = webdriver.FirefoxOptions()
        # En Firefox no suele ser necesario poner la ruta del binario,
        # pero si falla, se pone igual que en Chrome.

        try:
            self.driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )
            self.driver.get("https://web.telegram.org/k/")
            self.btn_scrape.configure(state="normal")
            self.log("Navegador Firefox listo.")
        except Exception as e:
            self.log(f"Error al abrir Firefox: {str(e)}")

    def start_scrape_thread(self):
        threading.Thread(target=self.scrape_users, daemon=True).start()

    def scrape_users(self):
        self.log("Buscando usuarios con @username...")
        try:
            # Buscamos elementos que suelen contener el nombre de usuario en la versión K
            # Nota: Los selectores pueden variar, Telegram los cambia a veces.
            elements = self.driver.find_elements(By.CSS_SELECTOR, ".peer-title")

            found_users = []
            for el in elements:
                name = el.text
                if name:
                    found_users.append(name)

            self.log(f"Se encontraron {len(found_users)} posibles nombres/usuarios.")
            for user in found_users:
                self.textbox.insert("end", f"{user}\n")

        except Exception as e:
            self.log(f"Error: {str(e)}")

    def log(self, message):
        self.textbox.insert("end", f"> {message}\n")
        self.textbox.see("end")


if __name__ == "__main__":
    app = TelegramScraperApp()
    app.mainloop()