import Foundation

// MARK: - PARTE 1

// MARK: - Protocolo Secuencia
protocol Secuencia {
    associatedtype Elemento
    
    func agregar(_ elemento: Elemento)
    
    func remover() throws -> Elemento
    
    var vacio: Bool { get }
}

// MARK: - Errores asociados a secuencias
enum ErrorSecuencia: Error {
    case secuenciaVacia(String)
    case secuenciaAbstracta(String)
}

// MARK: - Clase Secuencia basada en listas
// Esta clase es "no concreta" por el programador, recordemos en swift no hay clases abstractas
class ListBasedSecuencia<T>: Secuencia {
    typealias Elemento = T
    
    var items = [T]()
    
    var vacio: Bool {
        return self.items.count == 0
    }
    
    func agregar(_ elemento: T) {}
    
    func remover() throws -> T {
        throw ErrorSecuencia.secuenciaAbstracta("Error. Esta secuencia no es concreta")
    }
}

// MARK: - Clase Pila
class Pila<T>: ListBasedSecuencia<T> {
    override func agregar(_ elemento: T) {
        self.items.append(elemento)
    }
    
    override func remover() throws -> T {
        if self.vacio {
            throw ErrorSecuencia.secuenciaVacia("Error. La pila esta vacia")
        }
        return items.removeLast()
    }
}

// MARK: - Clase Cola
class Cola<T>: ListBasedSecuencia<T> {
    override func agregar(_ elemento: T) {
        items.append(elemento)
    }
    
    override func remover() throws -> T {
        if self.vacio {
            throw ErrorSecuencia.secuenciaVacia("Error. La cola esta vacia")
        }
        return items.removeFirst()
    }
}

// MARK: - PARTE 2

// MARK: - Clase grafo
final class Grafo {
    private let listAdy: [(Int, Int)]
    
    init(listAdy: [(Int, Int)]) {
        self.listAdy = listAdy
    }
    
    func adyacencias(of nodo: Int) -> [Int] {
        return self.listAdy.filter { (base, target) in
            return base == nodo
        }.map { (_, target) in
            return target
        }
    }
}

// MARK: - Clase busqueda
class Busqueda {
    final let grafo: Grafo
    final var closed: Set<Int> = []
    
    init(in grafo: Grafo) {
        self.grafo = grafo
    }
    
    final func buscar(D: Int, H: Int) -> Int {
        self.open(nodo: D)
        var count = 0
        
        while !self.done() {
            guard let next = self.select() else { return -1 }
            self.closed.insert(next)
            
            if next == H {
                return count
            }
            
            count += 1
            
            for ady in self.grafo.adyacencias(of: next) {
                if !self.descartar(nodo: ady) {
                    self.open(nodo: ady)
                }
            }
        }
        
        return -1
    }
    
    func open(nodo: Int) {}
    
    func select() -> Int? { return nil }
    
    func done() -> Bool { return true }
    
    func descartar(nodo: Int) -> Bool { return true }
}

// No colocamos la secuencia en Busqueda porque en swift los generics son invariantes entre si.

// MARK: - Clase DFS
class DFS: Busqueda {
    var pila = Pila<Int>()
    
    override func open(nodo: Int) {
        self.pila.agregar(nodo)
    }
    
    override func select() -> Int? {
        return try? self.pila.remover()
    }
    
    override func done() -> Bool {
        return self.pila.vacio
    }
    
    override func descartar(nodo: Int) -> Bool {
        return self.closed.contains(nodo)
    }
}

// MARK: - Clase BFS
class BFS: Busqueda {
    var cola = Cola<Int>()
    var opened: Set<Int> = []
    
    override func open(nodo: Int) {
        self.cola.agregar(nodo)
        self.opened.insert(nodo)
    }
    
    override func select() -> Int? {
        return try? self.cola.remover()
    }
    
    override func done() -> Bool {
        return self.cola.vacio
    }
    
    override func descartar(nodo: Int) -> Bool {
        return self.closed.contains(nodo) || self.opened.contains(nodo)
    }
}


let g = Grafo(listAdy: [(1,2), (2,8), (8,6), (2,3), (3,4), (4,5), (5,6), (7, 9)])

print(BFS(in: g).buscar(D: 1, H: 8)) // 2
print(DFS(in: g).buscar(D: 1, H: 8)) // 6
print(DFS(in: g).buscar(D: 1, H: 9)) // -1
