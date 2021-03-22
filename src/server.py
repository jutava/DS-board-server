from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
#import logging

PORT = 8079
DIMENSION = 500

FORMAT = 'utf-8'

MAX_STATES = 100
EVAL = "BETTER"  # BAD or BETTER


class WhiteBoard:
    def __init__(self):
        self.pixels = [["WHITE"] * DIMENSION for i in range(DIMENSION)]
        self.curState = 1
        self.recentStates = {}
        self.population = 0

    def changePixel(self, new_state):
        self.curState = self.curState + 1
        try:
            state, x, y, color = new_state.values()
        except ValueError:
            print("Incorrect new state format")
            return False
        self.pixels[x][y] = color
        # Check dictionary for MAX_STATES and remove the oldest entry if needed
        stateKeys = list(self.recentStates.keys())
        if self.population >= MAX_STATES:
            self.recentStates.pop(stateKeys[-1])
        else:
            self.population = self.population + 1
        self.recentStates[str(self.curState)] = {"x": x, "y": y, "color": color}
        print(f"State:{self.curState}, POST: ({x},{y}): {color}")
        return True # Succeed


    def getPixels(self, state):
        # Return type depending on evaluation method
        print("GET:", state)
        print("Latest state:",self.curState)
        if EVAL == "BAD":
            return self.pixels
        if EVAL == "BETTER":
            # if client is new or it is too far behind
            # --> return full board
            # else return most recent states client current to the latest
            if (state == 0) or ((self.curState - state) > MAX_STATES): 
                print("return board")
                return self.pixels
            else:
                subset = {str(key): self.recentStates[str(key)] for key in list(range(state+1,self.population+1))}
                print("return", subset)
                return subset

class myServer(BaseHTTPRequestHandler):
    # Redefined 
    def __init__(self, request, client_address, server):
        self.board = WhiteBoard()
        super().__init__(request, client_address, server)

    def _set_get_response(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()

    def _set_post_response(self, res):
        if res:
            self.send_response(200)
        else:
            self.send_response(409)
        self.send_header('content-type', 'text/html')
        self.end_headers()


    def do_GET(self):
        state = int(parse_qs(urlparse(self.path).query)["state"][0])
        #logging.info("")
        self._set_get_response()
        self.wfile.write(json.dumps(self.board.getPixels(state)).encode(FORMAT))

    def do_POST(self):
        content_length = int(self.headers['content-length'])
        post_data = json.loads(self.rfile.read(content_length))
        #logging.info("")
        res = self.board.changePixel(post_data)
        self._set_post_response(res)

def main():
    httpd = HTTPServer(("0.0.0.0", PORT), myServer)
    print(f"Server running on port {PORT} with {DIMENSION}x{DIMENSION} board")
    #logging.info('Starting server...\n')
    #setattr(httpd, 'board', WhiteBoard())
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
       pass
    httpd.server_close()
    #logging.info('Stopping server...\n')


if __name__ == '__main__':
    main()