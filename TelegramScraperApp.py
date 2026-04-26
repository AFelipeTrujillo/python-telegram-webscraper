import customtkinter as ctk
import threading
import random
import time
import os
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

        # UI Elements
        self.label = ctk.CTkLabel(self, text="User Extractor - Telegram Web K", font=("Arial", 18, "bold"))
        self.label.pack(pady=20)

        self.btn_open = ctk.CTkButton(self, text="1. Open Firefox (Secure)", command=self.start_browser_thread,
                                      fg_color="#FF5722", hover_color="#E64A19")
        self.btn_open.pack(pady=10)

        self.btn_scrape = ctk.CTkButton(self, text="2. Start Human-Like Extraction", command=self.start_scrape_thread,
                                        state="disabled")
        self.btn_scrape.pack(pady=10)

        self.textbox = ctk.CTkTextbox(self, width=500, height=200)
        self.textbox.pack(pady=20)

        self.driver = None

    def log(self, message):
        """Helper to log messages into the UI textbox."""
        self.textbox.insert("end", f"> {message}\n")
        self.textbox.see("end")

    def start_browser_thread(self):
        """Launches the browser initialization in a separate thread to keep UI responsive."""
        threading.Thread(target=self.open_browser, daemon=True).start()

    def open_browser(self):
        self.log("Configuring Firefox with anti-detection measures...")

        options = FirefoxOptions()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        profile_path = os.path.join(script_dir, "telegram_profile")

        if not os.path.exists(profile_path):
            os.makedirs(profile_path)

        options.add_argument("-profile")
        options.add_argument(profile_path)

        # Anti-detection and stealth settings
        # 1. Override User-Agent to match a standard Mac user
        options.set_preference("general.useragent.override",
                               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0")

        # 2. Disable the 'webdriver' flag (prevents sites from seeing 'navigator.webdriver = true')
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)

        # 3. Enable Marionette for Selenium communication
        options.set_preference("marionette.enabled", True)

        try:
            # Automatic driver installation and browser launch
            service = FirefoxService(GeckoDriverManager().install())
            self.driver = webdriver.Firefox(service=service, options=options)

            self.driver.get("https://web.telegram.org/k/")
            self.btn_scrape.configure(state="normal")
            self.log("Firefox opened. Please log in and navigate to a group.")
            self.log("Note: Open the members list sidebar before extracting.")
        except Exception as e:
            self.log(f"Error opening Firefox: {str(e)}")

    def start_scrape_thread(self):
        """Launches the scraping logic in a separate thread."""
        threading.Thread(target=self.scrape_logic, daemon=True).start()

    def scrape_logic(self):
        self.log("Starting extraction with random delays...")

        try:
            # Simulate initial 'reading' time before acting
            time.sleep(random.uniform(2, 4))

            # Locate member list elements. In Web K, titles usually have the '.peer-title' class.
            # Note: Selectors may change if Telegram updates their web version.
            elements = self.driver.find_elements(By.CSS_SELECTOR, ".peer-title")

            if not elements:
                self.log("No users detected. Is the members list actually open?")
                return

            extracted_users = []

            for index, el in enumerate(elements):
                # Every 5 users, take a longer pause to simulate human reading/scrolling
                if index % 5 == 0 and index > 0:
                    time.sleep(random.uniform(1.5, 3))

                name = el.text
                if name and name not in extracted_users:
                    extracted_users.append(name)
                    self.textbox.insert("end", f"Found: {name}\n")
                    self.textbox.see("end")

            self.log(f"Extraction finished. Total: {len(extracted_users)} visible users.")

        except Exception as e:
            self.log(f"Error during scraping: {str(e)}")


if __name__ == "__main__":
    app = TelegramScraperApp()
    app.mainloop()