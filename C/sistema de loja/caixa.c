#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <unistd.h>
#include <string.h>



typedef struct
{
    char nome[1000];
    int codigo;
    float preco;
}Loja;

/////////////////////////////////////////////////////////////
void abertura();
void criar_arquivo();
int menu_incial();
void cadastrar_produtos();
void visualizar();
int alterar();
void alterar_nome();
void alterar_preco();
void alterar_nome_preco();
float compra_cliente();
float calcular_compra(int codigos, int qnt);
int exibir_dados(int codigo);
void animacao();
int menu_de_pagamento(float total_compra);
float calcular_troco(float total_compra);
float calcular_desconto(float total_compra, int quantidade);
int opc_nota_fiscal();
void nota_fiscal(int codigo, int qnt);
void continuacao_nota(float total_compra, float troco);
void codigo_senha_cartao();
int situacao_parcelas();
int menu_parcelas(float total_compra);
void divisao_compra(int parcelas, float total_compra);
int menu_empresarial();
////////////////////////////////////////////////////////////


int main()
{
    int qnt, i, opc, escolha, escolha_pagamento, situacao, parcelas;
    int continuar, prosseguir, opc_empresarial;
    float desconto, troco = 0, total_compra;
    while(1)
    {
        criar_arquivo();
        opc = menu_incial();
        if(opc == 1)
        {
            system("cls");
            opc_empresarial = menu_empresarial();
            switch(opc_empresarial)
            {
                case 1:
                    printf("QUANTIDADE DE PRODUTOS: ");
                    scanf("%d",&qnt);
                    for(i = 0; i < qnt; i++)
                    {
                        printf("PRODUTO %d\n",i+1);
                        cadastrar_produtos();
                    }
                    break;
                case 2:
                    visualizar();
                    break;
                case 3:
                    system("cls");
                    escolha = alterar();
                    if(escolha == 1)
                        alterar_nome();
                    if(escolha == 2)
                        alterar_preco();
                    if(escolha == 3)
                        alterar_nome_preco();
                    break;
                case 4:
                    break;
                default:
                    printf("opcao invalida!\n");
                    break;
            }
        }
        if(opc == 2)
        {
            abertura();
            total_compra = compra_cliente();
            animacao();
            escolha_pagamento = menu_de_pagamento(total_compra);
            switch (escolha_pagamento)
            {
                case 1:
                    if(total_compra <= 100)
                    {
                        troco = calcular_troco(total_compra);
                    }
                    if(total_compra > 100 && total_compra <= 200)
                    {
                        printf("COMPRAS ACIMA DE 100 R$ GANHA DESCONTO DE 10%%\n");
                        desconto = calcular_desconto(total_compra, 10);
                        printf("desconto = %.2f\n",desconto);
                        troco = calcular_troco(desconto);
                    }
                    if(total_compra > 200 && total_compra <= 500)
                    {
                        printf("COMPRAS ACIMA DE 200 R$ GANHA DESCONTO DE 15%%\n");
                        desconto = calcular_desconto(total_compra, 15);
                        printf("desconto = %.2f\n",desconto);
                        troco = calcular_troco(desconto);
                    }
                    if(total_compra > 500)
                    {
                        printf("COMPRAS ACIMA DE 500 R$ GANHA DESCONTO DE 25%%\n");
                        desconto = calcular_desconto(total_compra, 25);
                        printf("desconto = %.2f\n",desconto);
                        troco = calcular_troco(desconto);
                    }
                    continuacao_nota(total_compra, troco);
                    printf("TROCO = %.2f\n",troco);
                    animacao();
                    break;
                case 2:
                    printf("INSIRA O CODIGO DO CARTAO: \n");
                    codigo_senha_cartao();
                    system("cls");
                    printf("INSIRA A SENHA DO CARTAO: \n");
                    codigo_senha_cartao();
                    printf("OPERACAO REALIZADA COM SUCESSO\n");
                    continuacao_nota(total_compra, troco);
                    animacao();
                    break;
                case 3:
                    printf("DESEJA VER CITUACAO DA COMPRA\n(1- sim/0- nao): ");
                    situacao = situacao_parcelas();
                    if(situacao)
                    {
                        system("cls");
                        parcelas = menu_parcelas(total_compra);
                        divisao_compra(parcelas, total_compra);
                    }
                    printf("CONTINUAR COMPRA\n(1- sim/ 0- nao): ");
                    continuar = situacao_parcelas();
                    if(continuar)
                    {
                        printf("INSIRA O CODIGO DO CARTAO: \n");
                        codigo_senha_cartao();
                        system("cls");
                        printf("INSIRA A SENHA DO CARTAO: \n");
                        codigo_senha_cartao();
                        system("cls");
                        parcelas = menu_parcelas(total_compra);
                        divisao_compra(parcelas, total_compra);
                        if(parcelas >= 1 && parcelas <= 3)
                            printf("COMPRA REALIZADA COM SUCESSO\n");
                        else
                            printf("COMPRA CANCELADA\n");
                        continuacao_nota(total_compra, troco);
                    }
                    else
                        printf("COMPRA CANCELADA.\n");
                    break;
                case 4:
                    printf("FINALIZANDO\n");
                    break;
                default:
                    break;  
            }
            printf("continuar operacao (1- sim/ 0- nao): ");
            prosseguir = situacao_parcelas();
            if(prosseguir == 0)
                break;
            else
                system("cls");
        }
    }
    printf("PROGRAMA FINALIZADO COM SUCESSO.\n");
}

void criar_arquivo()
{
    Loja vazio = {"", 0, 0.0};
    int i;
    FILE *arquivo;
    arquivo = fopen("produtos.bin","rb");
    if(arquivo == NULL)
    {
        arquivo = fopen("produtos.bin","wb");
        for(i = 0; i < 100000; i++)
        {
            fwrite(&vazio, sizeof(Loja), 1, arquivo);
        }
        fclose(arquivo);
    }
    else
    {
        arquivo = fopen("produtos.bin","rb");
        for(i = 0; i < 100000; i++)
        {
            fwrite(&vazio, sizeof(Loja), 1, arquivo);
        }
        fclose(arquivo);
    }
}

void cadastrar_produtos()
{
    Loja itens;
    int codigo;
    FILE *arquivo = fopen("produtos.bin","rb+");
    if(arquivo == NULL)
        printf("ERRO, arquivo nao criado\n");
    else
    {
        while(1)
        {
            printf("digite o codigo: ");
            scanf("%d",&codigo);
            fseek(arquivo, (codigo-1)*sizeof(Loja), SEEK_SET);
            fread(&itens, sizeof(Loja), 1, arquivo);
            if(itens.codigo != 0)
            {
                printf("Codigo ja foi cadastrado! tente novamente.\n");
                animacao();
            }
            else
            {
                itens.codigo = codigo;
                break;
            }
        }
        printf("NOME: ");
        fflush(stdin);
        scanf("%[^\n]",itens.nome);
        fflush(stdin);
        printf("PRECO: ");
        scanf("%f",&itens.preco);
        fseek(arquivo, (codigo-1)*sizeof(Loja), SEEK_SET);
        fwrite(&itens, sizeof(Loja), 1, arquivo);
        fclose(arquivo);
    }
}

void abertura()
{
    printf("========================\n");
    printf("\tCAIXA MTS\n");
    printf("========================\n");
}

void visualizar()
{
    Loja itens;
    long tamanho;
    FILE *arquivo = fopen("produtos.bin","rb");
    if(arquivo == NULL)
    {
        printf("ERRO, arquivo nao aberto\n");
        return;
    }
    printf("----------DADOS CADASTRADOS----------\n");
    fseek(arquivo, 0, SEEK_END);
    tamanho = ftell(arquivo);
    if (tamanho == 0)
    {
        printf("nao ha produtos cadastrados.\n");
    }
    else
    {
        rewind(arquivo);
        while(fread(&itens, sizeof(Loja), 1, arquivo) == 1)
        {
            if(itens.codigo != 0)
            {
                printf("codigo = %d nome = %s preco = %.2f\n",itens.codigo,itens.nome,itens.preco);
                printf("\n");
            }
        }
    }
    fclose(arquivo);
}

int alterar()
{
    int opc;
    while(1)
    {
        printf("-----OPCOES-----\n");
        printf("1- NOME\n2- PRECO\n3- (NOME/PRECO)\n4-CANCELAR\n>>> ");
        scanf("%d",&opc);
        if(opc <= 4 && opc >= 0)
            break;
        else
        {
            printf("opcao invalida, digite novamente\n");
            animacao();
        }
    }
    return opc;
}

void alterar_nome()
{
    Loja item;
    int codigo, posicao, aux = 0;
    FILE *arquivo = fopen("produtos.bin", "r+b");
    if (arquivo == NULL)
    {
        printf("ERRO: nao foi possivel abrir o arquivo.\n");
        return;
    }
    while(fread(&item, sizeof(Loja), 1, arquivo) == 1)
    {
        if(item.codigo != 0)
        {
            printf("codigo %d nome = %s\n",item.codigo, item.nome);
            printf("\n");
        }
    }
    while(1)
    {
        printf("Digite o codigo do produto a ser alterado: ");
        scanf("%d", &codigo);
        rewind(arquivo);
        while (fread(&item, sizeof(Loja), 1, arquivo) == 1)
        {
            if (item.codigo == codigo)
            {
                aux = 1;
                break;
            }
            posicao = ftell(arquivo);
        }
        if(!aux)
        {
            printf("produto nao encontrado\n");
        }
        if(aux)
            break;
    }
    printf("Novo nome: ");
    fflush(stdin);
    scanf(" %[^\n]", item.nome);
    fflush(stdin);
    fseek(arquivo, posicao, SEEK_SET);
    fwrite(&item, sizeof(Loja), 1, arquivo);
    printf("preco alterado com sucesso\n");
    fclose(arquivo);
}

void alterar_preco()
{
    Loja item;
    int codigo, posicao, aux = 0;
    FILE *arquivo = fopen("produtos.bin", "r+b");
    if (arquivo == NULL)
    {
        printf("ERRO: nao foi possivel abrir o arquivo.\n");
        return;
    }
    while(fread(&item, sizeof(Loja), 1, arquivo) == 1)
    {
        if(item.codigo != 0)
        {
            printf("codigo %d preco = %.2f\n",item.codigo, item.preco);
            printf("\n");
        }
    }
    while(1)
    {
        printf("Digite o codigo do produto a ser alterado: ");
        scanf("%d", &codigo);
        rewind(arquivo);
        while (fread(&item, sizeof(Loja), 1, arquivo) == 1)
        {
            if (item.codigo == codigo)
            {
                aux = 1;
                break;
            }
            posicao = ftell(arquivo);
        }
        if(!aux)
        {
            printf("produto nao encontrado\n");
        }
        if(aux)
            break;
    }
    printf("novo preco (R$): ");
    scanf("%f",&item.preco);
    fseek(arquivo, posicao, SEEK_SET);
    fwrite(&item, sizeof(Loja), 1, arquivo);
    printf("preco alterado com sucesso.\n");
    fclose(arquivo);
}

void alterar_nome_preco()
{
    Loja item;
    int codigo, posicao, aux = 0;
    FILE *arquivo = fopen("produtos.bin", "r+b");
    if (arquivo == NULL)
    {
        printf("ERRO: nao foi possivel abrir o arquivo.\n");
        return;
    }
    while(fread(&item, sizeof(Loja), 1, arquivo) == 1)
    {
        if(item.codigo != 0)
        {
            printf("codigo %d nome = %s preco = %.2f\n",item.codigo, item.nome, item.preco);
            printf("\n");
        }
    }
    while(1)
    {
        printf("Digite o codigo do produto a ser alterado: ");
        scanf("%d", &codigo);
        rewind(arquivo);
        while (fread(&item, sizeof(Loja), 1, arquivo) == 1)
        {
            if (item.codigo == codigo)
            {
                aux = 1;
                break;
            }
            posicao = ftell(arquivo);
        }
        if(!aux)
        {
            printf("produto nao encontrado\n");
        }
        if(aux)
            break;
    }
    printf("Novo nome: ");
    fflush(stdin);
    scanf(" %[^\n]", item.nome);
    fflush(stdin);
    printf("novo preco (R$): ");
    scanf("%f",&item.preco);
    fseek(arquivo, posicao, SEEK_SET);
    fwrite(&item, sizeof(Loja), 1, arquivo);
    printf("preco alterado com sucesso.\n");
    fclose(arquivo);
}

float compra_cliente()
{
    int codigos, qnt, aux;
    float total = 0.0;
    while(1)
    {
        printf("Digite o codigo do produto (-1 sair): ");
        scanf("%d", &codigos);
        system("cls");
        if(codigos == -1)
            break;
        aux = exibir_dados(codigos);
        if(aux)
        {
            printf("quantidade: ");
            scanf("%d",&qnt);
            total += calcular_compra(codigos, qnt);
        }
        nota_fiscal(codigos, qnt);
    }
    return total;
}

float calcular_compra(int codigos, int qnt)
{
    float total = 0;
    FILE *arquivo = fopen("produtos.bin", "rb");
    if (arquivo == NULL)
    {
        printf("ERRO: nao foi possivel abrir o arquivo.\n");
        return 0;
    }

    Loja item;
    while(fread(&item, sizeof(Loja), 1, arquivo) == 1)
    {
        if(item.codigo == codigos)
        {
            total += (item.preco * qnt);
            break;
        }
    }

    fclose(arquivo);
    return total;
}

int exibir_dados(int codigo)
{
    Loja item;
    FILE *arquivo = fopen("produtos.bin", "rb");
    if (arquivo == NULL)
    {
        printf("ERRO: nao foi possivel abrir o arquivo.\n");
        return 0;
    }
    while (fread(&item, sizeof(Loja), 1, arquivo) == 1)
    {
        if (item.codigo == codigo)
        {
            printf("Codigo: %d\n", item.codigo);
            printf("Nome: %s\n", item.nome);
            printf("Preco: %.2f\n", item.preco);
            fclose(arquivo);
            return 1;
        }
    }
    printf("Produto nao encontrado.\n");
    fclose(arquivo);
    return 0;
}

void animacao()
{
    sleep(1);
    system("cls");
}

int menu_de_pagamento(float total_compra)
{
    int opc;
    while(1)
    {
        printf("TOTAL DA COMPRA = %.2f R$\n",total_compra);
        printf("-----OPCOES DE PAGAMENTO-----\n");
        printf("[1] ....... A VISTA\n[2] ....... DEBITO\n[3] ....... CREDITO\n[4] ....... FINALIZAR\n");
        printf("\nSUA ESCOLHA? ");
        scanf("%d",&opc);
        if(opc <= 4 && opc > 0)
            break;
        else
        {
           printf("opcao invalida, digite novamente\n");
           animacao();
        } 
    }
    return opc;
}

float calcular_troco(float total_compra)
{
    float troco = 0, valor_pagar;
    printf("INSIRA O VALOR A PAGAR (R$): ");
    scanf("%f",&valor_pagar);
    if(valor_pagar > total_compra)
    {
        troco = valor_pagar - total_compra;
    }
    else
    {
        while(valor_pagar < total_compra)
        {
            printf("----------------------------------\n");
            printf("TOTAL DA COMPRA = %.2f\n",total_compra);
            printf("----------------------------------\n");
            printf("VALOR NAO SUFICIENTE...\npor favor,\nDIGITE NOVAMENTE: ");
            scanf("%f",&valor_pagar);
            animacao();
            if(valor_pagar >= total_compra)
                troco = valor_pagar - total_compra;
        }
    }
    return troco;
}

float calcular_desconto(float total_compra, int quantidade)
{
    float desconto;
    desconto = total_compra - (total_compra * quantidade / 100);
    return desconto;
}

int opc_nota_fiscal()
{
    int nota;
    while(1)
    {
        printf("DESEJA nota fiscal? (1- sim/0- nao): ");
        scanf("%d",&nota);
        if(nota <= 1 && nota >= 0)
            break;
        else
            printf("opcao invalida, digite novamente\n");
    }
    return nota;
}

void nota_fiscal(int codigo, int qnt)
{
    Loja item;
    FILE *arquivo = fopen("produtos.bin", "rb");
    if (arquivo == NULL)
    {
        printf("ERRO: nao foi possivel abrir o arquivo.\n");
        fclose(arquivo);
        return;
    }
    FILE *arquivo2;
    arquivo2 = fopen("nota_fiscal.txt","a+");
    if (arquivo2 == NULL)
    {
        printf("ERRO: nao foi possivel abrir o arquivo.\n");
        fclose(arquivo2);
        return;
    }
    while (fread(&item, sizeof(Loja), 1, arquivo) == 1)
    {
        if (item.codigo == codigo)
        {
            fprintf(arquivo2, "+------------------------------+--------------+------------------+\n");
        fprintf(arquivo2, "| produto                      |     preco    |     quantidade   |\n");
            fprintf(arquivo2, "+------------------------------+--------------+------------------+\n");
            fprintf(arquivo2, "| %-28s |  %-11.2f |  %-11d     |\n",item.nome, item.preco, qnt);
            fprintf(arquivo2, "+------------------------------+--------------+------------------+\n");
            fclose(arquivo2);
        }
    }
    fclose(arquivo2);
    fclose(arquivo);
}

void continuacao_nota(float total_compra, float troco)
{
    FILE *arquivo2;
    arquivo2 = fopen("nota_fiscal.txt","a");
    if (arquivo2 == NULL)
    {
        printf("ERRO: nao foi possivel abrir o arquivo.\n");
        fclose(arquivo2);
        return;
    }
    fprintf(arquivo2, "Total da Compra: %.2f\n", total_compra);
    fprintf(arquivo2, "Troco: %.2f\n", troco);
    fprintf(arquivo2, "********* OBRIGADO PELA PREFERENCIA *********\n");
    fclose(arquivo2);
}

void codigo_senha_cartao()
{
    char codigo[6];
    int tamanho_codigo;
    while(1)
    {
        printf("6 digitos: ");
        scanf("%s", codigo);
        tamanho_codigo = strlen(codigo);
        if(tamanho_codigo == 6)
            break;
        else
        {
            printf("ERRO NA LEITURA...\ntente novamente\n");
            animacao();
        }
    }
}

int situacao_parcelas()
{
    int opc;
    while(1)
    {
        printf("\nsua opcao>>> ");
        scanf("%d",&opc);
        if(opc <= 1 && opc >= 0)
            break;
        else
            printf("opcao invalida, digite novamente\n");
    }
    return opc;
}

int menu_parcelas(float total_compra)
{
    int escolha;
    while(1)
    {
        printf("TOTAL DA COMPRA = %.2f R$\n",total_compra);
        printf("----------OPCOES DE PARCELAMENTO----------\n");
        printf("1 ....... 3X\n2 ....... 6X\n3 ....... 10X\n4 ....... CANCELAR\n");
        printf("sua escolha >>> ");
        scanf("%d", &escolha);
        if(escolha <= 4 && escolha >= 1)
            break;
        else
        {
            printf("opcao invalida, digite novamente\n");
            animacao();
        }
    }
    return escolha;
}

void divisao_compra(int parcelas, float total_compra)
{
    float tot_parcelas;
    if(parcelas == 1)
    {
        tot_parcelas = total_compra / 3;
        printf("O VALOR %.2f R$ FICOU DIVIDIDO EM 3X DE %.2f R$\n",total_compra, tot_parcelas);
    }
    if(parcelas == 2)
    {
        tot_parcelas = total_compra / 6;
        printf("O VALOR %.2f R$ FICOU DIVIDIDO EM 6X DE %.2f R$\n",total_compra, tot_parcelas);
    }
    if(parcelas == 3)
    {
        tot_parcelas = total_compra / 10;
        printf("O VALOR %.2f R$ FICOU DIVIDIDO EM 10X DE %.2f R$\n",total_compra, tot_parcelas);
    }
    if(parcelas == 4)
    {
        printf("cancelando...\n");
    }
}

int menu_empresarial()
{
    int opc;
    while(1)
    {
        printf("---------- OPCOES ----------\n");
        printf("1- cadastrar produtos\n2- visualizar produtos\n3- alterar produtos\n4- sair: \n");
        printf("sua opcao >>> ");
        scanf("%d",&opc);
        if(opc >= 1 && opc <= 4)
            break;
        else
        {
            printf("opcao invalida, digite novamente\n");
            animacao();
        }
    }
    return opc;
}

int menu_incial()
{
    int opc;
    while(1)
    {
        printf("---------- MENU ----------\n");
        printf("1- modo empresarial\n2- modo comercial: \n");
        printf("sua opcao >>> ");
        scanf("%d",&opc);
        if(opc >= 1 && opc <= 2)
            break;
        else
        {
            printf("opcao invalida, digite novamente\n");
            animacao();
        }  
    }
    return opc;
}
