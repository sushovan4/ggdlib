#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <dirent.h>
#include <string.h>
#define MAX_LEN 256
#define C_V 0.75
#define C_E 1.0

double ggd(int m, int n, double V1[m][2], double V2[n][2], int adjMat1[m], int adjMat2[n], int i, int j, int pi[m]);
double dist(double p1[2], double p2[2]);
int indexOf(int s, int arr[], int n);

void main() {
    char* source = "data/Letter/json/LOW/";
    DIR *folder;
    FILE *file;
    struct dirent *entry;
    int files = 0;

    folder = opendir(source);
    if(folder == NULL)
        puts("Unable to read directory");
    else {
        while(entry=readdir(folder)) {
            files++;
            char fName[100];
            char* token;
            strcpy(fName, source);
            strcat(fName, entry->d_name);
            file = fopen(fName, "r" );
            char line[MAX_LEN];
            while (fgets(line, MAX_LEN, file)) {
                token = strtok(line, ", ");
                for(int i=0;i<2;i++) {
                    if(i==0) {   
                    printf("%s\t",token);
                    token = strtok(NULL, ", ");
                } else {
                    printf("%d\n",atoi(token));
                }       
            }
                // Remove trailing newline
                line[strcspn(line, "\n")] = 0;
                printf("%s\n", line);
            }
            fclose(file);
        }
    }
    closedir(folder);

    int m = 2; int n = 2;
    double V1[m][2];
    double V2[n][2];
    int adjMat1[m * m];
    int adjMat2[n * n];
    int pi[m];
    //double d = ggd(m, n, V1, V2, adjMat1, adjMat2, 0, -1, pi);
}

double ggd(int m, int n, double V1[m][2], double V2[n][2], int adjMat1[m * m], int adjMat2[n * n], int i, int j, int pi[]) {    
    if(i == m) {
        double cost = 0;
        for(int i = 0; i < m; i++) {
            // vertex translation
            if(j != -1)
                cost = cost + C_V * dist(V1[i], V2[pi[i]]);
        };

        for (int i = 0; i < m; i++)
            for (int j = i + 1; j < m; j++) {
                if(adjMat1[m * i + j] == 1)
                    if (pi[i] == -1 || pi[j] == -1 || adjMat2[n * pi[i] + pi[j]] == 0)
                    // Edge deletion from V1
                    cost = cost + C_E * dist(V1[i], V1[j]);
                else
                    // Edge translation
                    cost =  cost + C_E * fabs(dist(V1[i], V1[j]) - dist(V2[pi[i]], V2[pi[j]]));
            }

        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++) {
                if (adjMat2[n * i + j] == 1 && ((indexOf(i, pi, m) == -1) || (indexOf(j, pi, m) == -1) 
                || (adjMat1[m * indexOf(i, pi, m) + indexOf(j, pi, m)] == 0)))
                    // Edge deletion from V2
                    cost = cost + C_E * dist(V2[i], V2[j]);
            }  
        return cost;
    }
    
    pi[i] = -1;
    double out = ggd(m , n, V1, V2, adjMat1, adjMat2, i + 1, j, pi);
  
    for(int k = 0; k < n; k++) {
        if(k == j)
            continue;
        pi[i] = k;
        double d = ggd(m , n, V1, V2, adjMat1, adjMat2, i + 1, k, pi);
        if(d < out)
            out = d;
    }
    return out;
}

double dist(double p1[2], double p2[2]) {
    return sqrt( (p1[0] - p2[0]) * (p1[0] - p2[0]) 
        + (p1[1] - p2[1]) * (p1[1] - p2[1]) );
}

int indexOf(int s, int arr[], int n) {
    for(int i = 0; i < n; i++)
        if(arr[i] == s)
            return i;
    return -1;
}