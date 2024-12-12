import redis


client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

def agregar_receta():
    receta_id = client.incr("receta_id")  
    key = f"receta:{receta_id}"
    nombre = input("Nombre: ")
    ingredientes = input("Ingredientes: ")
    pasos = input("Pasos: ")
    receta = {
        "nombre": nombre,
        "ingredientes": ingredientes,
        "pasos": pasos
    }
    resultado = client.hset(key, mapping=receta)
    if resultado:
        print(f"Receta agregada con el ID: {receta_id}")
    else:
        print("Error al agregar la receta.")

def actualizar_receta():
    ver_recetas()
    receta_id = input("Ingrese el ID de la receta a actualizar: ")
    key = f"receta:{receta_id}"
    if not client.exists(key):
        print(f"No existe una receta con el ID {receta_id}.")
        return
    print("Ingrese los datos a cambiar (en blanco para no cambiar):")
    nombre = input("Nombre: ") or None
    ingredientes = input("Ingredientes: ") or None
    pasos = input("Pasos: ") or None
    cambios = {}
    if nombre:
        cambios["nombre"] = nombre
    if ingredientes:
        cambios["ingredientes"] = ingredientes
    if pasos:
        cambios["pasos"] = pasos
    if cambios:
        client.hset(key, mapping=cambios)
        print("Receta actualizada.")
    else:
        print("No se realizaron cambios.")

def eliminar_receta():
    ver_recetas()
    receta_id = input("Ingrese el ID de la receta a eliminar: ")
    key = f"receta:{receta_id}"
    if client.delete(key):
        print(f"Receta con ID {receta_id} ha sido eliminada.")
    else:
        print(f"No se encontró la receta con ID {receta_id}.")

def ver_recetas():
    keys = client.keys("receta:*")
    if not keys:
        print("No hay recetas disponibles.")
        return
    print("\nLista de recetas:")
    for key in keys:
        receta_id = key.split(":")[1]
        receta = client.hgetall(key)
        print(f"ID: {receta_id} | Nombre: {receta['nombre']} | Ingredientes: {receta['ingredientes']} | Pasos: {receta['pasos']}")
    print()

def menu():
    print("\nLibro de Recetas")
    print("a) Agregar nueva receta")
    print("b) Actualizar receta")
    print("c) Eliminar receta")
    print("d) Ver recetas")
    print("e) Salir")

def main():
    while True:
        menu()
        opcion = input("Opción: ")
        if opcion == "a":
            agregar_receta()
        elif opcion == "b":
            actualizar_receta()
        elif opcion == "c":
            eliminar_receta()
        elif opcion == "d":
            ver_recetas()
        elif opcion == "e":
            print("Saliendo")
            break
        else:
            print("Opción no valida. Intente de nuevo.")

if __name__ == "__main__":
    main()