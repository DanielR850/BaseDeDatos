-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS BellezaDB;
USE BellezaDB;

-- Tabla: Rol (antes Tipo_Usuario)
CREATE TABLE Rol (
  ID_Usuario INT AUTO_INCREMENT PRIMARY KEY,
  NombreRol VARCHAR(20) NOT NULL UNIQUE
);

-- Tabla: MetodoPago
CREATE TABLE MetodoPago (
  ID_Metodo INT AUTO_INCREMENT PRIMARY KEY,
  Nombre VARCHAR(20) NOT NULL UNIQUE
);

-- Tabla: Variante_Servicio
CREATE TABLE Variante_Servicio (
  ID_Variante INT AUTO_INCREMENT PRIMARY KEY,
  Nombre_Variante VARCHAR(30) NOT NULL UNIQUE
);

-- Tabla: Cliente
CREATE TABLE Cliente (
  ID_Cliente INT AUTO_INCREMENT PRIMARY KEY,
  Nombre VARCHAR(30) NOT NULL,
  PrimerApellido VARCHAR(15) NOT NULL,
  SegundoApellido VARCHAR(15),
  Telefono VARCHAR(13) NOT NULL UNIQUE
);

-- Tabla: Empleado (con NombreEmpleado en lugar de Nombre)
CREATE TABLE Empleado (
  ID_Empleado INT AUTO_INCREMENT PRIMARY KEY,
  ID_Usuario INT NOT NULL,
  NombreEmpleado VARCHAR(25) NOT NULL,
  PrimerApellido VARCHAR(15) NOT NULL,
  SegundoApellido VARCHAR(15),
  Contraseña VARCHAR(60) NOT NULL,
  FOREIGN KEY (ID_Usuario) REFERENCES Rol(ID_Usuario)
);

-- Tabla: Servicio
CREATE TABLE Servicio (
  ID_Servicio INT AUTO_INCREMENT PRIMARY KEY,
  ID_Variante INT NOT NULL,
  Nombre_Servicio VARCHAR(50) NOT NULL UNIQUE,
  Precio DECIMAL(4,2) NOT NULL,
  FOREIGN KEY (ID_Variante) REFERENCES Variante_Servicio(ID_Variante)
);

-- Tabla: Inventario
CREATE TABLE Inventario (
  ID_Producto INT AUTO_INCREMENT PRIMARY KEY,
  Nombre_Producto VARCHAR(30) NOT NULL,
  Marca VARCHAR(30) NOT NULL,
  Stock INT NOT NULL,
  Precio_Compra DECIMAL(7,2) NOT NULL
);

-- Tabla intermedia: Servicio_Producto
CREATE TABLE Servicio_Producto (
  ID_Servicio INT NOT NULL,
  ID_Producto INT NOT NULL,
  Cantidad_Usada INT NOT NULL,
  PRIMARY KEY (ID_Servicio, ID_Producto),
  FOREIGN KEY (ID_Servicio) REFERENCES Servicio(ID_Servicio),
  FOREIGN KEY (ID_Producto) REFERENCES Inventario(ID_Producto)
);

-- Tabla: Cita
CREATE TABLE Cita (
  ID_Cita INT AUTO_INCREMENT PRIMARY KEY,
  ID_Cliente INT NOT NULL,
  ID_Empleado INT NOT NULL,
  Fecha DATE NOT NULL,
  Hora TIME NOT NULL,
  FOREIGN KEY (ID_Cliente) REFERENCES Cliente(ID_Cliente),
  FOREIGN KEY (ID_Empleado) REFERENCES Empleado(ID_Empleado)
);

-- Tabla: Pago
CREATE TABLE Pago (
  ID_Pago INT AUTO_INCREMENT PRIMARY KEY,
  Monto DECIMAL(5,2) NOT NULL,
  ID_Metodo INT NOT NULL,
  ID_Cita INT NOT NULL UNIQUE,
  FOREIGN KEY (ID_Metodo) REFERENCES MetodoPago(ID_Metodo),
  FOREIGN KEY (ID_Cita) REFERENCES Cita(ID_Cita)
);

-- Tabla intermedia: Cita_Servicio
CREATE TABLE Cita_Servicio (
  ID_Cita INT NOT NULL,
  ID_Servicio INT NOT NULL,
  Cantidad INT NOT NULL,
  PRIMARY KEY (ID_Cita, ID_Servicio),
  FOREIGN KEY (ID_Cita) REFERENCES Cita(ID_Cita),
  FOREIGN KEY (ID_Servicio) REFERENCES Servicio(ID_Servicio)
);

-- Tabla: Promocion
CREATE TABLE Promocion (
  ID_Promocion INT AUTO_INCREMENT PRIMARY KEY,
  Descripcion VARCHAR(1000),
  Descuento DECIMAL(4,2),
  Fecha_Inicio DATE NOT NULL,
  Fecha_Fin DATE,
  ID_Servicio INT NOT NULL,
  FOREIGN KEY (ID_Servicio) REFERENCES Servicio(ID_Servicio)
);

-- Tabla: Costos_extra
CREATE TABLE Costos_extra (
  ID_Costo INT AUTO_INCREMENT PRIMARY KEY,
  ID_Cita INT NOT NULL UNIQUE,
  Descripcion VARCHAR(500),
  Monto DECIMAL(6,2),
  FOREIGN KEY (ID_Cita) REFERENCES Cita(ID_Cita)
);  