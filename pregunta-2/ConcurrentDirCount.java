import java.io.*;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Callable;
import java.util.concurrent.TimeUnit;

public class ConcurrentDirCount {

    // ------ Definimos un thread pool compartido
    static ExecutorService threadPool = Executors.newFixedThreadPool(10);

    // ------ Definimos el resultado, inicialmente esta en cero
    static int result = 0;

    // ------ Definimos una funcion para incrementar los resultados
    // Esta funcion debe estar sincronizada para evitar las condiciones de carrera
    // ente los threads activos en el pool.
    static synchronized void incrementResult() {
        ConcurrentDirCount.result = ConcurrentDirCount.result + 1;
    }

    // ------ metodo estatico para emepzar el proceso de conteo
    static void count(String path) throws Exception {
        // Colocamos result en cero 
        ConcurrentDirCount.result = 0;

        // Creamos la tarea base (en el thread principal)
        ConcurrentDirCount c = new ConcurrentDirCount(path);

        // Comenzamos el proceso concurrente
        c.compute();

        // Esperamos a que todas los threads en el pool finalicen
        ConcurrentDirCount.threadPool.shutdown();
    }

    String path;

    ConcurrentDirCount(String path) {
        this.path = path;
    }

    void compute() throws Exception { 
        // Leemos el dir
        File dir = new File(this.path);

        File listDir[] = dir.listFiles();

        LinkedList<Callable<Void>> tasks = new LinkedList<Callable<Void>>();

        // Iteramos sobre los sub-directorios
        for (int i = 0; i < listDir.length; i++) {

            // Si conseguimos un directorio
            if (listDir[i].isDirectory()) {
                final int i_ = i;
                
                // Creamos una tarea para ejecutarla en otro thread
                Callable<Void> subDirTask = () -> { 
                    ConcurrentDirCount c = new ConcurrentDirCount(listDir[i_].getPath());
                    c.compute();
                    
                    return null; 
                };

                // Agregamos la nueva tarea a la lista de tareas por invocar
                tasks.add(subDirTask);
            }
            // Si conseguimos un archivo
            else {
                // Aumentamos el contador (de forma sincronizada para evitar sistuaciones de carrera)
                ConcurrentDirCount.incrementResult();
            }
        }

        // Finalmente invocamos todas las sub tareas generadas
        // Utilizamos el pool thread que se creo estaticamente 
        ConcurrentDirCount.threadPool.invokeAll(tasks);
    }
}