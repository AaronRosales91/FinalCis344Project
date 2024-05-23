from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep
from restaurantDatabase import RestaurantDatabase
import cgi

class RestaurantPortalHandler(BaseHTTPRequestHandler):
    
    def __init__(self, *args, **kwargs):
        self.database = RestaurantDatabase()
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        try:
            if self.path == '/addReservation':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                customer_name = form.getvalue("customer_name")
                reservation_time = form.getvalue("reservation_time")
                number_of_guests = int(form.getvalue("number_of_guests"))
                special_requests = form.getvalue("special_requests")
                
                self.database.add_reservation(customer_name, reservation_time, number_of_guests, special_requests)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self._write_html_response("Reservation has been added")

            elif self.path == '/addSpecialRequest':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                reservation_id = int(form.getvalue("reservation_id"))
                special_requests = form.getvalue("special_requests")
                
                self.database.add_special_request(reservation_id, special_requests)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self._write_html_response("Special request has been added")

            elif self.path == '/deleteReservation':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                reservation_id = int(form.getvalue("reservation_id"))
                
                self.database.delete_reservation(reservation_id)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self._write_html_response("Reservation has been deleted")

            elif self.path == '/searchPreferences':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                customer_id = int(form.getvalue("customer_id"))
                
                preferences = self.database.search_preferences(customer_id)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self._write_html_response(f"Preferences found: {preferences}")

        except Exception as e:
            self.send_error(500, f"Internal server error: {e}")

    def do_GET(self):
        try:
            if self.path == '/':
                records = self.database.get_all_reservations()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self._write_html_reservation_list(records)

            elif self.path == '/addReservation':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self._write_html_form('Add Reservation', [
                    ('customer_name', 'Customer Name'),
                    ('reservation_time', 'Reservation Time (YYYY-MM-DD HH:MM:SS)'),
                    ('number_of_guests', 'Number of Guests'),
                    ('special_requests', 'Special Requests')
                ])

            elif self.path == '/addSpecialRequest':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self._write_html_form('Add Special Request', [
                    ('reservation_id', 'Reservation ID'),
                    ('special_requests', 'Special Requests')
                ])

            elif self.path == '/deleteReservation':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self._write_html_form('Delete Reservation', [
                    ('reservation_id', 'Reservation ID')
                ])

            elif self.path == '/searchPreferences':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self._write_html_form('Search Preferences', [
                    ('customer_id', 'Customer ID')
                ])

            elif self.path == '/viewReservations':
                records = self.database.view_all_reservations()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self._write_html_reservation_list(records)

            else:
                self.send_error(404, 'File Not Found: %s' % self.path)

        except Exception as e:
            self.send_error(500, f"Internal server error: {e}")

    def _write_html_response(self, message):
        self.wfile.write(b"<html><head><title>Restaurant Portal</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h1>Restaurant Portal</h1>")
        self.wfile.write(b"<hr>")
        self.wfile.write(b"<div> <a href='/'>Home</a>| \
                          <a href='/addReservation'>Add Reservation</a>|\
                          <a href='/viewReservations'>View Reservations</a>|\
                          <a href='/addSpecialRequest'>Add Special Request</a>|\
                          <a href='/deleteReservation'>Delete Reservation</a>|\
                          <a href='/searchPreferences'>Search Preferences</a></div>")
        self.wfile.write(b"<hr>")
        self.wfile.write(f"<h3>{message}</h3>".encode())
        self.wfile.write(b"</center></body></html>")

    def _write_html_form(self, title, fields):
        self.wfile.write(b"<html><head><title>" + title.encode() + b"</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h1>" + title.encode() + b"</h1>")
        self.wfile.write(b"<form method='POST' action='" + self.path.encode() + b"'>")
        for field_name, field_label in fields:
            self.wfile.write(f"{field_label}: <input type='text' name='{field_name}'><br>".encode())
        self.wfile.write(b"<input type='submit' value='Submit'>")
        self.wfile.write(b"</form></center>")
        self.wfile.write(b"</body></html>")

    def _write_html_reservation_list(self, records):
        self.wfile.write(b"<html><head><title>Restaurant Portal</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h1>Restaurant Portal</h1>")
        self.wfile.write(b"<hr>")
        self.wfile.write(b"<div> <a href='/'>Home</a>| \
                          <a href='/addReservation'>Add Reservation</a>|\
                          <a href='/viewReservations'>View Reservations</a>|\
                          <a href='/addSpecialRequest'>Add Special Request</a>|\
                          <a href='/deleteReservation'>Delete Reservation</a>|\
                          <a href='/searchPreferences'>Search Preferences</a></div>")
        self.wfile.write(b"<hr><h2>All Reservations</h2>")
        self.wfile.write(b"<table border=2> \
                            <tr><th> Reservation ID </th>\
                                <th> Customer ID </th>\
                                <th> Reservation Time </th>\
                                <th> Number of Guests </th>\
                                <th> Special Requests </th></tr>")
        for row in records:
            self.wfile.write(b' <tr> <td>')
            self.wfile.write(str(row[0]).encode())
            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[1]).encode())
            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[2]).encode())
            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[3]).encode())
            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[4]).encode())
            self.wfile.write(b'</td></tr>')
        
        self.wfile.write(b"</table></center>")
        self.wfile.write(b"</body></html>")

def run(server_class=HTTPServer, handler_class=RestaurantPortalHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
