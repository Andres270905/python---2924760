CREATE TABLE usuario (
  id_usuario INT PRIMARY KEY, 
  nombre_usuario VARCHAR(100),
  apellido_usuario VARCHAR(100),
  telefono_usuario VARCHAR(15),
  direccion VARCHAR(100),
  email VARCHAR(50) UNIQUE,
  tipo_usuario ENUM('vendedor', 'comprador')
  contrasena VARCHAR(255) NOT NULL,
);

CREATE TABLE productos (
  id_producto INT PRIMARY KEY,
  nombre_producto VARCHAR(100),
  descripcion VARCHAR(100),
  precio_producto INT,  
  categoria ENUM('frutas', 'verduras', 'tuberculos'),
  disponible INT
);

CREATE TABLE mercancia (
  id_mercancia INT PRIMARY KEY,
  id_producto INT,
  id_usuario INT, 
  FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario) ON DELETE CASCADE,
  FOREIGN KEY (id_producto) REFERENCES productos (id_producto) ON DELETE CASCADE
);

CREATE TABLE metodo_envio (
  id_pedido INT PRIMARY KEY,
  metodo ENUM('Domicilio', 'Punto_de_entrega')
);

CREATE TABLE factura (
  id_factura INT AUTO_INCREMENT PRIMARY KEY,
  fecha DATE,
  hora TIME,
  cantidad INT,
  medio_de_pago ENUM('efectivo', 'tarjeta', 'pse'),
  id_pedido INT,
  FOREIGN KEY (id_pedido) REFERENCES metodo_envio (id_pedido)
);

CREATE TABLE detalle_de_factura (
  id_detalle_factura INT PRIMARY KEY,
  id_mercancia INT,
  id_factura INT auto_increment,  
  FOREIGN KEY (id_mercancia) REFERENCES mercancia (id_mercancia),
  FOREIGN KEY (id_factura) REFERENCES factura (id_factura)
);

INSERT INTO usuario VALUES 
  (1010761295, 'Andrés Felipe', 'Castellanos', '3125383097', 'calle 38a sur', 'adres@mail.com', 'comprador','Gordo270905'),
  (1034280328, 'Alan David', 'Rodriguez', '3123535138', 'carrera 23 67', 'adarorin@mail.com', 'vendedor','Alan1234'),
  (1016716232, 'Byron Alexander', 'Lopez', '3152690475', 'diagonal 43 b', 'bylop@mail.com', 'vendedor','Byron1234');

INSERT INTO productos VALUES 
  (0001, 'Mango', 'dulce', 3650, 'frutas', 56),
  (0002, 'Papa', 'diversas preparaciones', 5600, 'tuberculos', 26),
  (0003, 'lechuga', 'crujiente y fresca', 3850, 'verduras', 18);

INSERT INTO mercancia VALUES 
  (56, 0001, 1010761295),
  (26, 0002, 1034280328),
  (18, 0003, 1016716232);

INSERT INTO metodo_envio VALUES 
  (10001, 'Domicilio'),
  (10002, 'Punto_de_entrega'),
  (10003, 'Domicilio');


INSERT INTO factura VALUES 
  (NULL, '2024-05-15', '20:28:09', 2, 'efectivo', 10001),
  (NULL, '2024-02-19', '06:36:20', 6, 'tarjeta', 10002),
  (NULL, '2024-09-27', '11:29:35', 1, 'pse', 10003);


INSERT INTO detalle_de_factura VALUES 
  (1000001, 56, 1),
  (1000002, 26, 2),
  (1000003, 18, 3);