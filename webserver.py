from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from queries import getRestaurantsQuery, createNewRestaurant, getRestaurant, renameRestaurant, deleteRestaurant


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = getRestaurantsQuery()

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1> <a href='/restaurants/new'> Make a New Restaurant Here </a></h1>"
                for restaurant in restaurants:
                    output += "<p> %s <br/>" % restaurant.name
                    output += "<a href='/restaurants/%s/edit'>Edit</a> <br/>" % restaurant.id
                    output += "<a href='/restaurants/%s/delete'>Delete</a> <br/>" % restaurant.id
                    output += "</p>"

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                <input name="newRestaurant" type="text" placeholder = 'New Restaurant Name' >
                <input type="submit" value="Create">
                 </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                splitedPath = str.split(self.path, '/')
                restaurantName = getRestaurant(splitedPath[2]).name

                self.send_response(200)
                self.send_header("Content-type","text/html")
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1> %s </h1>" % restaurantName
                output += "<form method='POST' enctype='multipart/form-data' action='%s'>" % self.path
                output += '''<input name="renameRestaurantName" type="text" placeholder = '%s' >
                <input type="submit" value="Rename">
                 </form>''' % restaurantName
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/delete"):
                splitedPath = str.split(self.path, '/')
                restaurantName = getRestaurant(splitedPath[2]).name

                self.send_response(200)
                self.send_header("Content-type","text/html")
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1> Are you sure you want to delete %s </h1>" % restaurantName
                output += "<form method='POST' enctype='multipart/form-data' action='%s'>" % self.path
                output += '''<input type="submit" value="Delete">
                 </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header("Content-type","text/html")
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
                <h2>What would you like me to say?</h2>
                <input name="message" type="text" >
                <input type="submit" value="Submit">
                 </form>'''
                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                return


        except IOError:
            self.send_error(404,"File Not Found "+self.path)


    def do_POST(self):
        # try:
        #     self.send_response(200)
        #     self.send_header('Content-type', 'text/html')
        #     self.end_headers()
        #     ctype, pdict = cgi.parse_header(
        #         self.headers.getheader('content-type'))
        #     if ctype == 'multipart/form-data':
        #         fields = cgi.parse_multipart(self.rfile, pdict)
        #         messagecontent = fields.get('message')
        #     output = ""
        #     output += "<html><body>"
        #     output += " <h2> Okay, how about this: </h2>"
        #     output += "<h1> %s </h1>"  %messagecontent[0]
        #     output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
        #     <h2>What would you like me to say?</h2>
        #     <input name="message" type="text" >
        #     <input type="submit" value="Submit">
        #      </form>'''
        #     output += "</body></html>"
        #     self.wfile.write(output.encode())
        #     print(output)

        try:
            if self.path.endswith("/restaurants/new"):

                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurantName = fields.get('newRestaurant')
                    createNewRestaurant(restaurantName[0])

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                splitedPath = str.split(self.path, '/')
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurantName = fields.get('renameRestaurantName')
                    renameRestaurant(splitedPath[2], restaurantName[0])

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/delete"):
                splitedPath = str.split(self.path, '/')
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    deleteRestaurant(splitedPath[2])

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


        except:
            pass

def main():
    try:
        server_address = ('',8080)
        httpServer = HTTPServer(server_address, webserverHandler)
        print("Web Server running on port 8080")
        httpServer.serve_forever()

    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        httpServer.socket.close()



if __name__ == '__main__':
    main()