import java.io.*;
import java.util.*;

class MatrixSum {
    public static void main(String[] args) {
        int[][] A = {
            {1,2,3,4,5},
            {5,6,7,8,9},
            {10,11,12,13,14}
        };

        int[][] B = {
            {-1,0,-3,-4,-5},
            {-5,-6,-7,0,-9},
            {-10,-11,-12,-13, 0}
        };

        System.out.println("\nA:");
        MatrixSum.printMatrix(A);
        System.out.println("\nB:");
        MatrixSum.printMatrix(B);

        try {
            ConcurrentMatrixSum c = new ConcurrentMatrixSum(A, B);
            c.compute();

            System.out.println("\nA + B:");
            MatrixSum.printMatrix(c.result);
        } catch (Exception e) {
            System.out.println(e);
        }
    }

    static void printMatrix(int[][] X) {
        for (int i = 0; i < X.length; i++) {
            System.out.println(Arrays.toString(X[i]));
        }
    }
}