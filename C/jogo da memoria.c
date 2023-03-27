#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define T 5

int c;

void imprimir(int *v);
int verificar(int *v1, int *v2);
void tempo();
void resultado(int x);
int main()
{
	int vet[T], vet2[T], result, op;
	while(1)
	{
		srand(time(NULL));
		for(c = 0; c < T; c++)
		{
			vet[c] = rand() % 11;
		}
		printf("sequencia:\n");
		imprimir(vet);
		tempo();
		printf("digite a sequencia correta:\n");
		for(c = 0; c < T; c++)
		{
			scanf("%d",&vet2[c]);
		}
		
		result = verificar(vet, vet2);
		resultado(result);
		while(1)
		{
			printf("deseja continuar?\n5 yes 6 not: ");
			scanf("%d",&op);
			system("cls");
			if(op == 5 || op == 6)
				break;
		}
		if(op == 6)
			break;
	}
	printf("volte sempre :)");
}

void imprimir(int *v)
{
	for(c = 0; c < T; c++)
	{
		printf("%d\t",v[c]);
	}
}

void tempo()
{
	printf("\n");
	sleep(5);
	system("cls");
}

int verificar(int *v1, int *v2)
{
	int aux;
	for(c = 0; c < T; c++)
	{
		if(v2[c] == v1[c])
			aux = 1;
		else
			aux = 0;
	}
	return aux;
}
void resultado(int x)
{
	if(x == 1)
		printf("acertou, parabens :) !!!\n");
	else
		printf("errou, tente na proxima :(\n");
}