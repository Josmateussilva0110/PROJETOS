Este aplicativo baseado em Django foi desenvolvido para ajudar os usuários a gerenciar suas tarefas e anotações associadas de maneira eficiente. Ele fornece uma interface amigável para criar, visualizar, editar e excluir tarefas e anotações, além de recursos adicionais como marcar tarefas como importantes ou concluídas e filtrar tarefas com base em seu status ou data.  


# Funcionalidades  

• Autenticação de Usuário Funcionalidade segura de login e logout.  
• Criar, visualizar, editar e excluir tarefas.  
• Marcar tarefas como importantes.  
• Marcar tarefas como concluídas.  
• Restaurar tarefas concluídas para o status ativo.  

### Gerenciamento de Anotações:
• Adicionar anotações às tarefas.  
• Editar e excluir anotações.   
• Visualizar tarefas do dia atual.  
• Visualizar tarefas importantes.  
• Visualizar tarefas concluídas.  

# Instalação  
• Python 3.6+  
• Django 3.0+  
• Uma ferramenta de ambiente virtual como 'venv'  

# Como usar  
```python
  git clone https://github.com/seuusuario/anotacoes.git
cd anotacoes
```

```python
  python -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
```

```python
  python manage.py createsuperuser
```

```python
  python manage.py runserver
```

```python
  Abra o navegador e vá para http://127.0.0.1:8000.
```
