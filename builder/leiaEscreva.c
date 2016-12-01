#include <stdio.h>

void escrevaInteiro(int a) {
	printf("%d\n", a);
}

void escrevaFlutuante(float a) {
	printf("%f\n", a);
}

int leiaInteiro() {
	int num;
	scanf("%d", &num);
	return num;
}

float leiaFlutuante() {
	float num;
	scanf("%f", &num);
	return num;
}
