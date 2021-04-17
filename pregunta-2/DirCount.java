import java.io.*;
import java.util.*;

class DirCount {
    public static void main(String[] args) {
        String path = "/Users/pintojoao/Documents/trimestre/current/Lenguajes-de-programacion/Evaluaciones/CI3641-exam-3/";

        try {
            ConcurrentDirCount.count(path);
            System.out.println("\nResult: ");
            System.out.println(ConcurrentDirCount.result);
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}