# Integração do Amazon Lex com o Slack

Como integrar o bot criado no Amazon Lex em uma aplicação Slack

## Requisitos Mínimos

- Crie uma conta e um workspace no Slack
- Crie ou tenha um bot criado do Amazon Lex

**OBS.: Abaixo, teremos instruções da criação da conta Slack, mas usaremos um bot importado do Amazon Lex via arquivo zip, no qual foi disponibilizado pelo Vinicius no grupo do Whatsapp**

## 1. Criando a conta e o workspace no Slack

- Acesse o [Slack](www.slack.com)
- Na página inicial, clique em **Primeiros passos**
- Em seguida, insira seu e-mail **corporativo**
- A seguir, coloque o código que foi enviado para o seu e-mail
- Após carregar a página, clique em **Criar Workspace**
- Digite o nome do time (ou da empresa, se preferir)
- Caso queira adicionar integrantes no workspace, digite o e-mail correspondente a eles, ou copie o link de convite. Caso não, apenas pule esta etapa
- Digite o nome do trabalho que será desenvolvido nesse workspace

## 2. Criando a aplicação Slack

- Acesse o [Slack Api](https://api.slack.com/)
- No cabeçalho, clique em **Your Apps**
- A seguir clique em **Create New App** e **From scratch**, pois assim poderemos configurar o app do zero a partir da interface do Slack
- Digite o nome do app, selecione o workspace criado anteriormente no **Passo 1** e clique em **Create App** 
- Assim que for redirecionado para a página de configurações do aplicativo, Em **Basic Information -> App Credentials**, copie e guarde ao lado (em um bloco de notas) o **Client ID**, o **Client Secret** e o **Verification Token**
- Agora, na mesma página, procure no menu lateral a seção de **Interactive & Shortcuts**
- Ative o **Interactive** e insira em **Request URL** o URL temporário **https://slack.com**. Após isso, clique no botão **Save Changes** no final da tela

**OBS.: Não feche esta página ainda, pois retornaremos a ela mais pra frente**

## 3. Importando o bot no Amazon Lex

**OBS.: Certifique-se que tenha baixado o arquivo zip**

- Acesse o Console de Gerenciamento da AWS
- Procure por **Amazon Lex**
- No lado esquerdo da tela, clique no menu e selecione **Bots**
- Ao lado do botão **Create Bot**, clique em **Actions** e, em seguida, **Import**
- Insira o nome do bot
- Clique no botão **Browse File** e selecione o arquivo zip baixado anteriormente
- Caso queira, insira uma senha (é **opcional**)
- Mais abaixo, em **IAM permissions**, selecione **Create a role with basic Amazon Lex permissions**. Isso fará com que a própria AWS crie uma role
- Em **Children’s Online Privacy Protection Act (COPPA)**, selecione **No**, pois o bot não é direcionado para uso de crianças menores de 13 anos
- No final do formulário, ao lado do botão de **Import**, desative a seleção **Warn before overwriting existing bots with the same name** para evitar um aviso de erro para o caso do bot já existir na sua conta
- Clique em **Import**

## 4. Configurar bot para a integração

- Ainda no Console de Gerenciamento da AWS, no Amazon Lex, clique em **Bots** e selecione o bot importado
- No menu lateral, navegue até **Deployment -> Channel Integrations**
- Clique em **Add Channel**
- Na tela de **Add Channel**, selecione a plataforma **Slack**
- Em **IAM role**, selecione a IAM criada pela Amazon para o nosso bot
- Em **KMS key** selecione a **aws/lex**, que é uma KMS básica criada pela própria Amazon
- Mais abaixo, na seção de **Integration Configuration**, digite o nome desse channel
- Em **Alias**, selecione **TestBotAlias**
- Em **Language**, selecione **English (US)**
- Agora, na seção de **Additional configuration**, insira o **Client ID**, o **Client Secret** e o **Verification Token** que foi guardado anteriormente
- No momento, deixe a opção de **Success page URL** em branco, e clique em **Add**
- Após criar o channel, selecione-o
- Mais abaixo, na seção de **Callback URL**, guarde os links de **Endpoint** e **OAuth Endpoint**, pois serão utilizados no Slack

## 5. Retornando para as configurações do app Slack

- De volta para a página de configurações do app Slack (criado na **Parte 2**), selecione no menu lateral a seção de **OAuth & Permissions**
- Em **Redirect URL**, clique em **Add new Redirect URL**, copie o link do **OAuth Endpoint** guardado anteriormente (na **Parte 4**) e clique em **Add**
- Agora, clique em **Save URLs**
- Mais abaixo, na seção de **Scopes**, serão necessárias duas permissões, a **chat:write** e **team:read**
- Em **Bot Token Scopes**, clique em **Add an OAuth Scope** e procure **chat:write** e **team:read** separadamente
- Após isso, retorne para o menu lateral e acesse novamente a seção de **Interactive & Shortcuts**
- Agora, em **Request URL**, substitua a URL temporária pelo link do **Endpoint** guardado anteriormente (na **Parte 4**)
- Clique em **Save Changes** no final da tela
- Novamente no menu lateral, procure por **Event Subscriptions**
- Ative a opção de **Enable Events**
- Em **Request URL**, insira o mesmo link de **Endpoints**
- Mais abaixo, clique na seção de **Subscribe to bot events**
- Clique em **Add Bot User Event** e procure por **message.im**
- Clique em **Save Changes** no final da tela
- No menu lateral, procure por **App Home**
- Role abaixo até encontrar **Show Tabs**, e marque a seleção de **Allow users to send Slash commands and messages from the messages tab**
- Novamente no menu lateral, procure por **Manage Distribution**
- Clique em **Add to Slack**
- Na página de permissão, clique em **Allow**

### Após isso, você será redirecionado para o workspace. O seu app está no menu lateral, em **Apps**