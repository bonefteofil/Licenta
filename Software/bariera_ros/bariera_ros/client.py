import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
import requests
import threading
import json
import websocket
import time

from bariera_ros.config import URL_HTTP, URL_WS, BARIERA_ID

class ClientWS(Node):
    def __init__(self):
        super().__init__('client_ws_node')
        
        self.create_subscription(String, 'client/verificare', self.validare_numar, 1)
        self.pub_status = self.create_publisher(Bool, 'client/permisiune', 1)
        self.pub_ocupare = self.create_publisher(String, 'client/ocupare', 1)
        self.pub_display = self.create_publisher(String, 'comanda/display', 1)
        
        self.stare_conectat = False
        self.bariera_alocata = False
        
        self.ws_thread = threading.Thread(target=self.pornire_ws, daemon=True)
        self.ws_thread.start()


    def validare_numar(self, msg):
        if not self.stare_conectat or not self.bariera_alocata:
            return

        numar = msg.data
        self.get_logger().info(f'Verificare numar: {numar}')

        try:
            # Setat la 5.0 secunde pentru a permite delay-ul manual de pe server
            raspuns = requests.post(URL_HTTP, params={"numar_inmatriculare": numar}, timeout=5.0)
            raspuns.raise_for_status() 
            acces = bool(raspuns.json().get('acces', False))
        except Exception as e:
            self.get_logger().error(f"Eroare HTTP: {e}")
            acces = False

        self.pub_status.publish(Bool(data=acces))

    def pornire_ws(self):
        
        def on_message(ws, message):
            date = json.loads(message)
            
            if "status" in date:
                if date["status"] == "nealocata":
                    if self.bariera_alocata:
                        self.pub_display.publish(String(data=f"ID: {BARIERA_ID}"))
                        self.pub_ocupare.publish(String(data="NEALOCATA"))
                    self.bariera_alocata = False
                elif date["status"] == "activa":
                    self.bariera_alocata = True

            # Procesam date utile doar daca bariera a fost acceptata de server
            if self.bariera_alocata:
                if "locuri_ocupate" in date:
                    self.pub_ocupare.publish(String(data=f"O:{date['locuri_ocupate']}/{date['locuri_total']}"))

                if date.get("actiune") == "deschide":
                    self.get_logger().info('Comanda deschidere urgenta Cloud!')
                    self.pub_status.publish(Bool(data=True))

        def on_close(ws, close_status_code, close_msg):
            self.get_logger().warn("Conexiune WebSocket pierduta...")
            self.stare_conectat = False
            self.bariera_alocata = False
            self.pub_display.publish(String(data="OFFLINE"))
            self.pub_ocupare.publish(String(data="O:--/--"))
            time.sleep(6)
            self.pornire_ws() # Reconectare automata la infinit

        def on_open(ws):
            self.stare_conectat = True
            self.get_logger().info("Conexiune WebSocket stabilita!")

        def on_error(ws, error):
            pass

        ws = websocket.WebSocketApp(URL_WS, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
        ws.run_forever()

def main(args=None):
    rclpy.init(args=args)
    node = ClientWS()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            node.destroy_node()
            rclpy.shutdown()
        except Exception:
            pass

if __name__ == '__main__':
    main()