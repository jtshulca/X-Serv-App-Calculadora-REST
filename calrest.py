#!/usr/bin/python3

#Version con un recurso por tipo de operacion (“/suma”, “resta”, etc.). 
#Se actualiza con PUT, que envia los operandos (ej: 4,5), se consulta con GET,
#que devuelve el resultado (ej: 4+5=9).

import webapp

class CalculadoraRest(webapp.webApp):

    def parse(self, request):
        try:
            metodo = request.split(' ',2)[0]
            recurso = request.split(' ',2)[1]
            try:
                cuerpo = request.split('\r\n\r\n')[1]
            except IndexError:
                cuerpo =""
        except IndexError:
            return None

        peticion = [metodo, recurso, cuerpo]
        return peticion

    def process(self, peticion):

        operaciones = ["suma", "resta", "multiplicacion", "division"]
        try:
            metodo = peticion[0]
            recurso = peticion[1][1:]
            cuerpo = peticion[2]
        except TypeError:
            httpCode = "400 Bad Request"
            htmlResp = "<html><body>Error<html><body>"
            return (httpCode, htmlResp)

        if metodo == "GET":
            try:
                result = self.result
                infoGet = self.respGet
                httpCode = "200 OK"
                htmlResp = "<html><body>" + infoGet + "</body></html>"
            except AttributeError:
                httpCode = "400 Bad Request"
                htmlResp = "<html><body>Introduce una operación: /suma/resta/multiplicacion" +\
                           "/division y añade numeros con PUT</body></html>"

        elif metodo == "PUT":
            try:
                self.num1 = float(cuerpo.split(" ")[0])
                self.num2 = float(cuerpo.split(" ")[1])
            except ValueError:
                httpCode = "400 Bad Request"
                htmlResp = "<html><body>Se introducen los numeros separados por un espacio<html><body>"
                return (httpCode, htmlResp)
                
            if recurso == operaciones[0]:
                self.result = self.num1 + self.num2
                self.respGet = "Suma: " + str(self.num1) + " + " + str(self.num2 ) + \
                                " = " + str(self.result)
                httpCode = "200 OK"
                htmlResp = "<html><body>Comprueba el resultado mediante el metodo GET<html><body>"
                
            elif recurso == operaciones[1]:
                self.result = self.num1 - self.num2
                self.respGet = "Resta: " + str(self.num1) + " - " + str(self.num2 ) + \
                                " = " + str(self.result)
                httpCode = "200 OK"
                htmlResp = "<html><body>Comprueba el resultado mediante el metodo GET<html><body>"
                
            elif recurso == operaciones[2]:
                self.result = self.num1 * self.num2
                self.respGet = "Multiplicación: " + str(self.num1) + " * " + str(self.num2 ) + \
                                " = " + str(self.result)
                httpCode = "200 OK"
                htmlResp = "<html><body>Comprueba el resultado mediante el metodo GET<html><body>"
  
            elif recurso == operaciones[3]:
                self.result = self.num1 / self.num2
                self.respGet = "División: " + str(self.num1) + " / " + str(self.num2 ) + \
                                    " = " + str(self.result)
                httpCode = "200 OK"
                htmlResp = "<html><body>Comprueba el resultado mediante el metodo GET<html><body>"               
            else:
                httpCode = "404 Not Found"
                htmlResp = "<html><body>No has dicho que operación quieres hacer<html><body>"

        else:
            httpCode = "405 Method Not Allowed"
            htmlResp = "Metodo no admitido"

        return (httpCode, htmlResp)

if __name__ == "__main__":
	testWebApp = CalculadoraRest('localhost', 1234)
