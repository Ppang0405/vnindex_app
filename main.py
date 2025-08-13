import datetime
import threading

import pandas as pd
import rumps

from helper import fetch_stock_data


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
            "Refresh",
        ]

        # Set default index
        self.current_index = "VNINDEX"

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

    @rumps.clicked("Refresh")
    def manual_refresh(self, _):
        self.update_index_value()

    def update_index_value(self, _=None):
        thread = threading.Thread(target=self.fetch_index)
        thread.start()

    def fetch_index(self):
        try:
            # Fetch index data using VNDIRECT API
            symbol = self.current_index

            # Define date range (last 5 days)
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.datetime.now() - datetime.timedelta(days=14)).strftime(
                "%Y-%m-%d"
            )

            # Fetch data from VNDIRECT API
            data = fetch_stock_data(symbol, start_date, today)
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

            # Format the display with an up or down indicator
            if change >= 0:
                self.title = f"{self.current_index}: {latest_value:.2f} 🔺{abs(change_pct):.2f}%"
            else:
                self.title = f"{self.current_index}: {latest_value:.2f} 🔻{abs(change_pct):.2f}%"

        except Exception as e:
            self.title = f"{self.current_index}: Error"
            print(f"Error fetching data: {e}")


if __name__ == "__main__":
    VNIndexApp().run()
