# 🤖 Telegram CC Store Bot

Bot profissional para Telegram com sistema de venda de cartões de crédito, integração Pix, verificação de canal e painel administrativo avançado.

## ✨ Funcionalidades

### Usuário
- ✅ Verificação obrigatória de inscrição no canal
- ✅ Perfil com saldo e histórico de compras
- ✅ Compra de cartões por nível (Black, Infinite, Corporate, Business, Classic, Platinum)
- ✅ Verificação automática de cartões via API Checker
- ✅ Depósito com integração Pix
- ✅ Histórico de transações
- ✅ Prazo de devolução com contagem regressiva

### Administrador
- ✅ Adicionar cartões em massa (`/addcc`)
- ✅ Gerenciar saldo de usuários (`/addsaldo`, `/resaldo`, `/getsaldo`)
- ✅ Criar vouchers de saldo (`/addgift`)
- ✅ Listar usuários (`/users`)
- ✅ Enviar mensagens em massa (`/send`)
- ✅ Alterar preços de níveis (`/alteraritem`)
- ✅ Menu de administrador (`/menu`)

## 🚀 Como Começar

### Pré-requisitos
- Python 3.9+
- pip
- Git
- Token de Bot do Telegram (@BotFather)

### 1. Clonar o Repositório

```bash
git clone https://github.com/alquimicst-hxr/telegram-cc-store-bot.git
cd telegram-cc-store-bot
```

### 2. Criar Ambiente Virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Copie `.env.example` para `.env`:

```bash
cp .env.example .env
```

Edite `.env` com seus dados:

```env
AAE5KjeWx5syJJ3DvPyOX_O0nUrttIytzZU⁶i
OWNER_ID=7848571699
CHANNEL_USERNAME=@haxorstorecc
CHANNEL_ID=-1001234567890
```

### 5. Rodar o Bot

```bash
python main.py
```

Se tudo estiver certo, você verá:
```
🤖 Bot de Telegram rodando com sucesso!
```

## 📂 Estrutura de Arquivos

```
telegram-cc-store-bot/
├── .env                    # Variáveis de ambiente (NÃO commitar)
├── .env.example            # Template de variáveis
├── .gitignore              # Arquivos ignorados no Git
├── requirements.txt        # Dependências Python
├── README.md               # Este arquivo
├── main.py                 # Arquivo principal
└── app/
    ├── __init__.py
    ├── config.py           # Configurações gerais
    ├── database.py         # Gerenciamento de banco de dados SQLite
    ├── pix_service.py      # Integração Pix (estrutura)
    ├── utils.py            # Funções auxiliares
    ├── handlers.py         # Handlers de usuário
    └── admin.py            # Handlers de administrador
```

## 🔧 Configuração do Bot

### Variáveis Importantes

| Variável | Descrição | Exemplo |
|----------|-----------|----------|
| `BOT_8843258561:AAE5KjeWx5syJJ3DvPyOX_O0nUrttIytzZUTOKEN` | Token do bot no Telegram | `123456:ABC-DEF1234ghIkl-zyx57W2v23ew11` |
| `OWNER_ID` | ID do dono do bot | `7848571699` |
| `CHANNEL_USERNAME` | Username do canal de verificação | `@haxorstorecc` |
| `CHANNEL_ID` | ID numérico do canal | `-1001234567890` |
| `CHECKER_URL` | URL da API de verificação de cartões | `https://jokercchk.squareweb.app/api/check` |
| `DEPOSIT_MINIMUM` | Valor mínimo de depósito | `10.0` |
| `PRAZO_DEVOLUCAO_MINUTOS` | Tempo de devolução do cartão | `5` |

### Obter IDs do Telegram

**ID do Usuário:**
- Envie `/start` ao bot
- O ID aparece no console ou no banco de dados

**ID do Canal:**
- Adicione o bot como admin no canal
- Envie uma mensagem no canal
- Verifique o `chat_id` nos logs

## 💳 Como Adicionar Cartões

### Formato
```
/addcc NUMERO|MES|ANO|CVV|NIVEL|VALOR
```

### Exemplos
```
/addcc 5276600064049219|12|2024|721|black|45
/addcc 4532015112830366|06|2025|123|platinum|22
/addcc 6011111111111117|03|2026|456|classic|18
```

### Múltiplos Cartões (uma linha por cartão)
```
/addcc 5276600064049219|12|2024|721|black|45
5447317485524324|05|2027|822|infinite|35
6011000990139424|11|2025|654|corporate|30
```

## 💰 Sistema de Saldo

### Administrador
- `/addsaldo [ID] [VALOR]` - Adicionar saldo
- `/resaldo [ID] [VALOR]` - Remover saldo
- `/getsaldo [ID]` - Verificar saldo
- `/addgift [VALOR]` - Criar voucher

### Usuário
- Clique em "💰 Depositar" no perfil
- Envie o valor em reais
- O saldo é atualizado instantaneamente

## 🔐 Segurança

- ✅ Token guardado em `.env` (não commitado)
- ✅ Senhas e tokens não aparecem nos logs
- ✅ Validação de usuário em cada operação
- ✅ Verificação de canal obrigatória
- ✅ Só admin pode ver comandos admin
- ✅ Banco de dados local com SQLite

## 📊 Comandos de Usuário

| Comando | Descrição |
|---------|----------|
| `/start` | Iniciar bot |
| `/perfil` | Ver perfil e saldo |
| `/historico` | Ver histórico de transações |

## 🎛️ Comandos de Admin

| Comando | Descrição |
|---------|----------|
| `/menu` | Ver menu admin |
| `/addcc` | Adicionar cartões |
| `/addsaldo` | Adicionar saldo |
| `/resaldo` | Remover saldo |
| `/getsaldo` | Ver saldo |
| `/addgift` | Criar voucher |
| `/users` | Listar usuários |
| `/send` | Enviar mensagem em massa |
| `/alteraritem` | Alterar preço |

## 🐛 Troubleshooting

### Bot não conecta

```bash
# Verificar token
echo $BOT_TOKEN

# Verificar internet
ping api.telegram.org
```

### Erro de banco de dados

```bash
# Deletar banco e recriar
rm store.db
python main.py
```

### Erro de imports

```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

## 🔗 Links Úteis

- [python-telegram-bot Docs](https://python-telegram-bot.readthedocs.io/)
- [@BotFather](https://t.me/BotFather) - Criar bot
- [Telegram Bot API](https://core.telegram.org/bots/api)

## 📝 Licença

Este projeto é de uso privado. Todos os direitos reservados.

## 👨‍💻 Autor

Desenvolvido para Haxor Store CC

---

**Status:** ✅ Em desenvolvimento ativo

**Última atualização:** 2026-10-09

**Versão:** 1.0.0-beta