# Sistema de Gestión para Comercios

Prototipo de **sistema de gestión simple para pequeños comercios**, desarrollado en Python como proyecto de práctica y exploración de desarrollo asistido con IA.

El objetivo del proyecto es demostrar cómo un sistema de gestión básico puede ser construido de forma modular y extensible, pensado para **tiendas físicas pequeñas, puestos móviles o emprendimientos** que necesitan controlar ventas, inventario y clientes sin depender de software empresarial complejo o costoso.

La visión a futuro es que este sistema pueda evolucionar hacia una **aplicación accesible desde el navegador (tipo app web)** para que un comercio pueda utilizarlo fácilmente desde una notebook o PC utilizando Google Chrome.

---

# Características principales

El sistema actualmente funciona como una aplicación **CLI (Command Line Interface)** y permite gestionar los aspectos básicos de un negocio:

### Gestión de Inventario

* Alta de productos
* Eliminación de productos
* Visualización de inventario
* Alertas de stock bajo
* Transferencias de productos

### Ventas

* Registro de ventas
* Asociación de ventas a un empleado
* Asociación opcional a clientes
* Historial de ventas
* Resumen de ingresos

### Clientes

* Registro de clientes
* Búsqueda de clientes
* Eliminación de clientes
* Asociación de clientes a ventas

### Facturación

* Generación de facturas desde ventas
* Historial de facturas
* Exportación de facturas a:

  * TXT
  * PDF

### Caja chica

* Apertura de caja
* Registro de ingresos
* Registro de gastos
* Historial de movimientos

### Reportes

* Resumen de inventario
* Producto más vendido
* Producto menos vendido
* Reporte financiero diario

### Sistema de usuarios

* Registro de empleados
* Login de usuario
* Ventas registradas por empleado

### Persistencia de datos

Los datos se almacenan en archivos **JSON**, lo que permite que la información persista entre ejecuciones.

---

# Arquitectura del proyecto

El proyecto está organizado de forma modular para facilitar su mantenimiento y expansión.

```
Sistema-de-gestion-para-comercios
│
├── main.py                # Punto de entrada del sistema
├── cli_handlers.py        # Manejo de los menús del sistema
├── auth.py                # Sistema de login y empleados
├── dashboard.py           # Panel general del negocio
│
├── inventory.py           # Lógica de inventario
├── product.py             # Modelo de producto
├── sale.py                # Modelo de ventas
├── sales_analysis.py      # Reportes de ventas
│
├── customer.py            # Gestión de clientes
├── invoice.py             # Facturación
├── petty_cash.py          # Caja chica
│
├── data_managment.py      # Persistencia JSON
│
├── *.json                 # Archivos de datos persistentes
```

---

# Cómo ejecutar el sistema

Requisitos:

* Python 3.10 o superior

Clonar el repositorio:

```bash
git clone https://github.com/firmanija/Sistema-de-gestion-para-comercios-.git
cd Sistema-de-gestion-para-comercios-
```

Ejecutar el sistema:

```bash
python main.py
```

Si no existen empleados registrados, el sistema permitirá crear el primer usuario administrador.

---

# Objetivo del proyecto

Este proyecto fue desarrollado como **práctica de programación y diseño de software**, explorando el uso de herramientas de inteligencia artificial para acelerar el desarrollo.

Busca demostrar:

* diseño modular en Python
* organización de un sistema de gestión
* persistencia de datos
* flujo de usuarios y autenticación
* arquitectura extensible para futuras interfaces

---

# Posibles mejoras futuras

* Interfaz web (Flask / FastAPI)
* Aplicación accesible desde navegador
* Roles y permisos de usuario
* Base de datos SQL
* Dashboard visual con gráficos
* Sistema multi-usuario en red
* Exportación de reportes avanzados
* Integración con POS

---

# Autor

Bruno Firmano

Proyecto desarrollado como práctica y exploración de desarrollo de software asistido por IA.

