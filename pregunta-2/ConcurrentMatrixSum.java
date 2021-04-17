import java.io.*;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Callable;
import java.util.function.Function;

public class ConcurrentMatrixSum {

    int[][] A;
    int[][] B;

    // ----- no hace falta crear un setter con synchronized pues las operaciones son independientes
    int[][] result;

    ConcurrentMatrixSum(int[][] A, int[][] B) throws IllegalArgumentException {
        // ------ Validando

        if (A.length != B.length) {
            throw new IllegalArgumentException("A y B deben tener las mismas dimensiones.");
        }

        for (int i = 0; i < A.length; i++){
            if (A[i].length != B[i].length || A[i].length != A[0].length) {
                throw new IllegalArgumentException("A y B deben ser matrices con las mismas dimensiones.");
            }
        }

        this.A = A;
        this.B = B;
        this.result = new int[this.A.length][this.A[0].length];
    }

    void compute() throws Exception {
        LinkedList<Callable<Integer>> tasks = new LinkedList<Callable<Integer>>();

        // ------ Creando tareas independientes para calcular result[i][j]
        // No hace falta sincronizar
        for (int i = 0; i < this.result.length; i++) {
            for (int j = 0; j < this.result[0].length; j++) {

                final int i_ = i;
                final int j_ = j;

                Callable<Integer> task = () -> {
                    this.result[i_][j_] = this.A[i_][j_] + this.B[i_][j_];
                    return this.result[i_][j_];
                };

                tasks.add(task);
            }
        }
        
        // ------ Creamos un thread pool (Executor)
        // Creamos n * m threads, de forma que cada tarea de calculo result[i][j] se asigne a un thread 
        ExecutorService executor = Executors.newFixedThreadPool(this.result.length * this.result[0].length);

        // ------ Invocamos todas las tareas
        executor.invokeAll(tasks);

        // ------ Esperamos a que todas las tareas terminen
        executor.shutdown();
    }
}