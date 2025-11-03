from persona import Persona

class Aspirante(Persona):
    def __init__(self, primerNombre, segundoNombre, primerApellido, segundoApellido, 
                 tipoDocumento, numeroDocumento, fechaNacimiento, genero, direccion, telefono):
        super().__init__(primerNombre, segundoNombre, primerApellido, segundoApellido, 
                         tipoDocumento, numeroDocumento, fechaNacimiento, genero, direccion, telefono)
        
        
