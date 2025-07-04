# Guia de Instalação - Gerador de QR Code Intranet

## Instalação Rápida

### 1. Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 2. Download e Extração
```bash
# Extraia o projeto para o diretório desejado
cd /caminho/para/seu/projeto
```

### 3. Instalação das Dependências
```bash
# Entre no diretório do projeto
cd intranet_qr

# Instale as dependências
pip install -r requirements.txt
```

### 4. Configuração do Banco de Dados
```bash
# Execute as migrações
python manage.py makemigrations
python manage.py migrate
```

### 5. Execução
```bash
# Inicie o servidor
python manage.py runserver 0.0.0.0:8000
```

### 6. Acesso
Abra seu navegador e acesse: `http://localhost:8000`

## Instalação para Produção

### 1. Configurações de Segurança
Edite o arquivo `intranet_qr/settings.py`:

```python
# Altere para False em produção
DEBUG = False

# Configure os hosts permitidos
ALLOWED_HOSTS = ['seu-dominio.com', 'ip-do-servidor']

# Configure uma SECRET_KEY segura
SECRET_KEY = 'sua-chave-secreta-aqui'
```

### 2. Banco de Dados PostgreSQL (Recomendado)
```bash
# Instale o driver PostgreSQL
pip install psycopg2-binary

# Configure no settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'qrcode_db',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Servidor Web com Gunicorn
```bash
# Instale o Gunicorn
pip install gunicorn

# Execute com Gunicorn
gunicorn intranet_qr.wsgi:application --bind 0.0.0.0:8000
```

### 4. Nginx (Proxy Reverso)
Configuração exemplo para Nginx:

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /caminho/para/intranet_qr/staticfiles/;
    }

    location /media/ {
        alias /caminho/para/intranet_qr/media/;
    }
}
```

### 5. Coleta de Arquivos Estáticos
```bash
# Colete os arquivos estáticos
python manage.py collectstatic
```

## Solução de Problemas

### Erro: "No module named 'qrcode'"
```bash
pip install qrcode[pil]
```

### Erro: "No module named 'PIL'"
```bash
pip install Pillow
```

### Erro de Migração
```bash
# Remova migrações e recrie
rm qrcode_generator/migrations/0001_initial.py
python manage.py makemigrations qrcode_generator
python manage.py migrate
```

### Porta já em uso
```bash
# Use uma porta diferente
python manage.py runserver 0.0.0.0:8080
```

## Backup e Manutenção

### Backup do Banco de Dados
```bash
# SQLite
cp db.sqlite3 backup_$(date +%Y%m%d).sqlite3

# PostgreSQL
pg_dump qrcode_db > backup_$(date +%Y%m%d).sql
```

### Limpeza de Logs
```bash
# Limpe logs antigos se necessário
python manage.py shell
>>> from qrcode_generator.models import QRCodeHistory
>>> QRCodeHistory.objects.filter(created_at__lt='2024-01-01').delete()
```

## Suporte

Para suporte técnico ou dúvidas sobre a instalação, consulte:
- README.md para documentação completa
- Logs do Django em caso de erros
- Documentação oficial do Django: https://docs.djangoproject.com/

