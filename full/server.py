import socket

lastCaller = 'Not Yet Set'

def generate_html(set_by):
    html = """<!DOCTYPE html>
    <html>
        <head> <title>IDA ESP32</title>
        <style>
            html {
                font-family: Helvetica;
                display: inline-block;
                margin: 0px auto;
                text-align: center;
            }

            h1 {
                color: #0F3376;
                padding: 2vh;
            }

            p {
                font-size: 1.5rem;
            }

            .button {
                display: inline-block;
                background-color: #e7bd3b;
                border: none;
                border-radius: 4px;
                color: white;
                padding: 16px 40px;
                text-decoration: none;
                font-size: 30px;
                margin: 2px;
                cursor: pointer;
            }

            .button2 {
                background-color: #4286f4;
            }
        </style>
        </head>
        <body>
            <h1>IDA Horsens</h1>
            <p>Set By: <strong>""" + set_by + """</strong></p>
            <p>
              <a href="/?led=off"><button class="button">OFF</button></a>
              <a href="/?led=on"><button class="button button2">ON</button></a>
            </p>
        </body>
    </html>
    """

    return html

def start_service(do_lightOn, do_lightOff):
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(5)

    print("listening on", addr)

    while True:
        conn, addr = s.accept()
        print("Got a connection from %s" % str(addr[0]))
        request = conn.recv(1024)
        request = str(request)
        print('Content = %s' % request)
        led_on = request.find("/?led=on")
        led_off = request.find("/?led=off")

        if led_on == 6:
            print("LED ON")
            do_lightOn()

        if led_off == 6:
            print("LED OFF")
            do_lightOff()

        response = generate_html(lastCaller)
        lastCaller = str(addr[0])

        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-Type: text/html\n")
        conn.send("Connection: close\n\n")
        conn.sendall(response)
        conn.close()
