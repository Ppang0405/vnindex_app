import datetime
import threading

import pandas as pd
import rumps

from helper import fetch_stock_data_with_fallback


class VNIndexApp(rumps.App):
    def __init__(self):
        super(VNIndexApp, self).__init__(name="VN-Index")

        # Skip setting icon for now
        # Uncomment and add an icon.png file if you want a custom icon
        # self.icon = "icon.png"

        # Add menu items for different indices if desired
        self.menu = [
            "VN-Index",
            "VN30",
            "HNX-Index",
            None,  # Separator
            "Use Safari Scraper",
            "Use API Only", 
            None,  # Separator
            "Refresh",
        ]

        # Set default index and scraping method
        self.current_index = "VNINDEX"
        self.use_safari_scraper = False

        # Start the update timer
        self.timer = rumps.Timer(self.update_index_value, 60)  # Update every 60 seconds
        self.timer.start()

        # Initial update
        self.update_index_value()

    @rumps.clicked("VN-Index")
    def set_vnindex(self, _):
        self.current_index = "VNINDEX"
        self.update_index_value()

    @rumps.clicked("VN30")
    def set_vn30(self, _):
        self.current_index = "VN30"
        self.update_index_value()

    @rumps.clicked("HNX-Index")
    def set_hnx(self, _):
        self.current_index = "HNX"
        self.update_index_value()
        
    @rumps.clicked("Use Safari Scraper")
    def toggle_safari_scraper(self, _):
        self.use_safari_scraper = True
        print("🌐 Enabled Safari scraper mode")
        self.update_index_value()
        
    @rumps.clicked("Use API Only")
    def toggle_api_only(self, _):
        self.use_safari_scraper = False
        print("📡 Enabled API-only mode")
        self.update_index_value()

    @rumps.clicked("Refresh")
    def manual_refresh(self, _):
        self.update_index_value()

    def update_index_value(self, _=None):
        thread = threading.Thread(target=self.fetch_index)
        thread.start()

    def fetch_index(self):
        try:
            # Fetch index data
            symbol = self.current_index

            # Define date range (last 5 days)
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.datetime.now() - datetime.timedelta(days=14)).strftime(
                "%Y-%m-%d"
            )

            # Choose data source based on user preference
            if self.use_safari_scraper:
                print(f"🌐 Using Safari scraper for {symbol}")
                from safari_scraper import fetch_stock_data_safari
                data = fetch_stock_data_safari(symbol, start_date, today)
            else:
                print(f"📡 Using API with Safari fallback for {symbol}")
                data = fetch_stock_data_with_fallback(symbol, start_date, today)
                
            if not data:
                raise Exception(f"No data returned for {symbol}")

            # Convert to DataFrame for easier handling
            index_data = pd.DataFrame(data)

            # Get the latest value (close price)
            latest_value = index_data["close"].iloc[-1]

            # Get the previous close for calculating change
            prev_close = (
                index_data["close"].iloc[-2] if len(index_data) > 1 else index_data["open"].iloc[-1]
            )

            # Calculate change and percentage
            change = latest_value - prev_close
            change_pct = (change / prev_close) * 100

            # Use change data from scraper if available
            if 'changePercent' in index_data.columns and not pd.isna(index_data["changePercent"].iloc[-1]):
                change_pct = index_data["changePercent"].iloc[-1]
            
            if 'change' in index_data.columns and not pd.isna(index_data["change"].iloc[-1]):
                change = index_data["change"].iloc[-1]

            # Format the display with an up or down indicator
            source_indicator = "🌐" if self.use_safari_scraper else "📡"
            
            if change >= 0:
                self.title = f"{source_indicator} {self.current_index}: {latest_value:.2f} 🔺{abs(change_pct):.2f}%"
            else:
                self.title = f"{source_indicator} {self.current_index}: {latest_value:.2f} 🔻{abs(change_pct):.2f}%"

        except Exception as e:
            error_indicator = "🌐❌" if self.use_safari_scraper else "📡❌"
            self.title = f"{error_indicator} {self.current_index}: Error"
            print(f"Error fetching data: {e}")


if __name__ == "__main__":
    VNIndexApp().run()
