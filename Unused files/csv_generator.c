#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/*
 * Compile with 'gcc csv_generator.c -o generator'
 * Run with ./generator (mac/linux) or .\generator.exe (windows)
 *
 * You don't need to change anything outside the #define statements below. Simply set the numbers
 * to modify percentage chances (for the MALFORMED_ macros) or to 1/0 to enable/disable the error forcing
 * (for the FORCE_ macros)
 */

//set percentages of various corruptions
//malformed filename = date in filename will be invalid (in the future) (0-100%)
#define MALFORMED_FILENAME 0
// malformed data = data will be out of range or batch number will be duplicated (0-100%)
#define MALFORMED_DATA 0
// malformed header = header will contain incorrect column names (0-100%)
#define MALFORMED_HEADER 0
// batch numbers will be duplicated (0/1)
#define FORCE_BATCH_DUPLICATION 0
// datapoints will be out of range (0/1)
#define FORCE_DATA_OUT_OF_RANGE 0

// change number of entries in CSV file (max_entries = lines, reading_count = readingX (10 by default))
#define MAX_ENTRIES 10
#define READING_COUNT 10

// record used batch numbers
int batches[MAX_ENTRIES], batch_ptr = 0;

// roll a percentage chance with a threshold
int roll(int pc){
	int val = rand()%100;
	return val < pc;
}

/**
 * Create a file with specified name
 * @param filename the name of the file to be created
 * @return a file pointer
 */
FILE *create_file(char *filename){
	FILE *f = fopen(filename, "w+");
	return f;
}

/**
 * Print the headers to the specified file
 * @param f The file pointer to print to
 */
void print_headers(FILE *f){
	if(! roll(MALFORMED_HEADER)) {
		fprintf(f, "\"batch_id\",\"timestamp\",\"reading1\",\"reading2\",\"reading3\",\"reading4\",\"reading5\",\"reading6\",\"reading7\",\"reading8\",\"reading9\",\"reading10\"\n");
	}
	else {
		fprintf(f, "\"bach_id\",\"timestmp\",\"reading1\",\"reading2\",\"reading3\",\"reading4\",\"reading5\",\"reading4\",\"reading7\",\"reading8\",\"reading9\",\"reading10\"\n");
	}
}

/**
 * Add an entry to the CSV file
 * @param f The file pointer
 */
void add_entry(FILE *f){
	int batch = rand()%200;
	if(FORCE_BATCH_DUPLICATION) batch = 7;
	else if(roll(MALFORMED_DATA) && batch_ptr != 0) batch = batches[0];
	else for(int i = 0; i < batch_ptr; i++) {
		if(batch == batches[i]) {
			batch++;
			i = 0;
		}
	}

	batches[batch_ptr++] = batch;

	float readings[READING_COUNT];
	time_t time_now = time(NULL);
	struct tm pretty_time = *localtime(&time_now);

	for(int i = 0; i < READING_COUNT; i++){
		readings[i] = (((float)rand())/((float)RAND_MAX)) * 9.9999f;
	}
	if(roll(MALFORMED_DATA) || FORCE_DATA_OUT_OF_RANGE)
		fprintf(f, "%d,\"%02d:%02d:%02d\",%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f\n",
				batch, pretty_time.tm_hour, pretty_time.tm_min, pretty_time.tm_sec, readings[0], readings[1], readings[2],
			readings[3]-17.f, readings[4], readings[5] + 10.f, readings[6], readings[7],
				readings[8], readings[9]);
	else fprintf(f, "%d,\"%02d:%02d:%02d\",%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f\n",
				 batch, pretty_time.tm_hour, pretty_time.tm_min, pretty_time.tm_sec, readings[0], readings[1], readings[2],
				 readings[3], readings[4], readings[5], readings[6], readings[7],
				 readings[8], readings[9]);
}

int main(void) {
	srand(time(NULL));
	char *filename = malloc(sizeof(char) * 29);
	strcpy(filename, "MED_DATA_");

	// generate a time string and roll the chance of it being a malformed name
	time_t time_now = time(NULL);
	int corrupt_filename = roll(MALFORMED_FILENAME);
	struct tm pretty_time = *localtime(&time_now);
	char datetime[22];
	sprintf(datetime, "%04d%02d%02d%02d%02d%02d.csv", pretty_time.tm_year + 1900 + corrupt_filename * (1 + (rand() % 10)),
			pretty_time.tm_mon + 1, pretty_time.tm_mday, pretty_time.tm_hour, pretty_time.tm_min, pretty_time.tm_sec);
	strcpy(filename + (sizeof(char) * 9), datetime);

	printf("[*] Creating file %s\n", filename);
	FILE *csv_file = create_file(filename);
	if(csv_file == NULL){
		printf("[!] File I/O error. Exiting.\n");
		exit(0);
	}

	print_headers(csv_file);

	for(int i = 0; i < MAX_ENTRIES; i++){
		printf("[+] Adding entry %d to file.\n", i);
		add_entry(csv_file);
	}

	fclose(csv_file);

	printf("[*] Wrote data to %s\n", filename);
	return 0;
}
