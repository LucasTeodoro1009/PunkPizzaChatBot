# Parte 1: TTS com Amazon Polly

Transforme seu texto em áudio através do Amazon Polly

## 1. Tecnologias Utilizadas

### 1.1.1 Linguagem

[![Python](https://img.shields.io/badge/Python-3.12.4-007fff.svg)](https://github.com/serverless/serverless)
[![Yaml](https://img.shields.io/badge/Yaml-4.4.4-da3287.svg)](https://github.com/serverless/serverless)

### 1.1.2 Infraestrutura
[![Serverless](https://img.shields.io/badge/Serverless-4.4.4-e32636.svg)](https://github.com/serverless/serverless)

### 1.1.3 Amazon Web Services

[![AWS CLI](https://img.shields.io/badge/AWS_Command_Line_Interface-v2-orange.svg)](https://github.com/serverless/serverless)
[![Amazon Lambda](https://img.shields.io/badge/Amazon_Lambda-12/01/2024-red.svg)](https://github.com/serverless/serverless)
[![Amazon Polly](https://img.shields.io/badge/Amazon_Polly-27/08/2024-008b8b.svg)](https://github.com/serverless/serverless)
[![Amazon S3](https://img.shields.io/badge/Amazon_S3-24/09/2024-03c03c.svg)](https://github.com/serverless/serverless)
[![Amazon DynamoDB](https://img.shields.io/badge/Amazon_DynamoDB-03/09/2024-003399.svg)](https://github.com/serverless/serverless)

### 1.1.4 Teste das requisições HTTP

[![ThunderClient](https://img.shields.io/badge/Thunder_Client-2.27.6-purple.svg)](https://github.com/serverless/serverless)

## 1.2 Destrinchando o funcionamento do sistema

### 1.2.1 Serverless Framework

O **Serverless Framework** foi utilizado para construir e gerenciar toda a infraestrutura do sistema, sendo capaz de criar todos os serviços AWS, determinar políticas, instruir regras etc. via código no momento em que o sistema for para o ar.

### 1.2.2 Amazon Polly

O **Amazon Polly** é um potente serviço que será capaz de transformar as mensagens enviadas pelo usuário no corpo da requisição HTTP em áudio. Neste caso, devido à custos, foi utilizada a voz padrão feminina Joanna, com o arquivo de áudio sendo salvo no formato `.mp3`.

### 1.2.2 Amazon S3

O **Amazon S3** é local onde iremos armazenar o arquivo `.mp3` gerado pelo Polly. Esse arquivo será contido em um bucket público, no qual os usuários terão acesso para realizar o download do áudio.

### 1.2.3 Amazon DynamoDB

O **Amazon DynamoDB** é um banco de dados NoSQL e que não prevê gerenciamento de servidores. Nele, teremos uma tabela com as seguintes colunas:

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| ``dynamoapikey`` | string | Chave única gerada com hash md5 da frase do usuário. |
| ``phrase`` | string | Frase original enviada pelo usuário. |
| ``audio_url`` | string | URL do arquivo de áudio gerado pelo Amazon Polly e salvo no S3. |
| ``created_at`` | string | Data e hora em que o áudio foi gerado. |

### 1.2.4 Amazon Lambda

O **Amazon Lambda** será responsável pelo funcionamento em conjunto de todos os serviços da AWS, e a partir disso processar suas funções e constituir a lógica do sistema.

### 1.2.5 Lógica do Sistema

Quando o deploy do **Serverless** é acionado, o bucket público e a tabela são criados respectivamente no S3 e no DynamoDB, além de um endpoint **POST** ser gerado no terminal para o usuário. A partir disso, assim que o usuário inserir uma frase no corpo da requisição HTTP (no formato **JSON**) no endpoint, ele obterá uma resposta de status *_200 OK*_ no seguinte modelo:

```json
  {
    "received_phrase": "bi bi lada",
    "url_to_audio": "https://meu-bucket/audio-xyz.mp3",
    "created_audio": "2024-10-14 10:00:00",
    "unique_id": "123456"
  }
```

Quando o usuário acessar o link do áudio, o download do arquivo `.mp3` será iniciado automaticamente.

Visualize a arquitetura do sistema até este ponto:

![Arquitetura](./assets/arquitetura-tts.png)

## 1.3 Como realizar o deploy localmente

**Especificações**:

- Ter o [**AWS CLI v2**](https://docs.aws.amazon.com/pt_br/cli/latest/userguide/getting-started-install.html) instalado.
- Criar uma conta gratuita no [**Serverless**](https://app.serverless.com/).

### 1.3.1 Configurar o perfil da AWS na máquina

- [Acesse a documentação por aqui](./docs/aws-sso.md)

### 1.3.2 Instalar o Serverless Framework

19. Para instalar o Serverless Framework de forma global na máquina, digite na linha de comando:

```bash
npm install -g serverless
```

20. Verifique se o framework realmente foi instalado.

```bash
serverless --version
```

### 1.3.2 Clonar o repositório

OBS: Recomendo o uso do *Git BASH*, pois ele é um terminal voltado para git, ou seja, tem funcionalidades que auxiliam a gestão do versionamento do código.

21. Clone o repositório abaixo.

```bash
git clone https://github.com/Compass-pb-aws-2024-JULHO-A/sprints-6-7-pb-aws-julho-a.git
```

23. Acesse o diretório sprints-6-7-pb-aws-julho-a.

```bash
cd sprints-6-7-pb-aws-julho-a
```

24. Mude para a branch com o nome de *grupo-2*.

```bash
git checkout grupo-2
```

25. Acesse o diretório api-tts.

```bash
cd api-tts
```

### 1.3.3 Configurando o deploy

26. Crie um arquivo .env

27. Insira o perfil da AWS criado anteriormente, e crie um nome para o bucket do S3 e para a tabela do DynamoDB. Veja o arquivo .envExample caso tenha dúvidas.


PROFILE=my-dev-profile
BUCKET_NAME=bucket-s3-tts
DYNAMODB_TABLE=dynamodb-table-tts


28. Instale o plugin serverless-dotenv-plugin pela linha de comando.

```bash
serverless plugin install -n serverless-dotenv-plugin
```

29. Instale o plugin serverless-python-requirements pela linha de comando.

```bash
serverless plugin install -n serverless-python-requirements
```

30. Suba o sistema.

```bash
serverless deploy
```

O seguinte resultado será exibido no terminal:

```bash
✔ Service deployed to stack api-tts-python-dev

endpoint: POST - https://XXXXXXXXXX.execute-api.us-east-1.amazonaws.com/dev/v1/tts
functions:
  tts: api-tts-python-dev-tts (58 MB)
```

## 1.4 Como testar o sistema

1. Copie o endpoint *POST* que foi gerado no terminal.

2. Utilize alguma ferramenta de API, como o Postman, para testar esse endpoint.

3. Cole o o link do endpoint e certifique que o método selecionado é o *POST*.

4. No corpo da requisição *JSON* digite a frase no formato abaixo:

```json
  {
    "phrase": "bi bi lada"
  }
```

5. A resposta deverá estar no seguinte formato:

```json
  {
    "received_phrase": "bi bi lada",
    "url_to_audio": "https://meu-bucket/audio-xyz.mp3",
    "created_audio": "2024-10-14 10:00:00",
    "unique_id": "123456"
  }
```

6. Caso queira ter acesso ao áudio, copie o link do url_to_audio e cole no navegador, assim, o download do arquivo .mp3 será iniciado automaticamente.

---

# Parte 2: PunkPizza ChatBot

## 2.1 Tecnologias Utilizadas

### 2.1.1 Linguagem

[![Python](https://img.shields.io/badge/Python-3.12.4-007fff.svg)](https://github.com/serverless/serverless)

### 2.1.1 Amazon Web Services

[![Amazon Lex](https://img.shields.io/badge/Amazon_Lex-v2-blue.svg)](https://github.com/serverless/serverless)
[![Amazon Lambda](https://img.shields.io/badge/Amazon_Lambda-12/01/2024-red.svg)](https://github.com/serverless/serverless)

### 2.1.2 Plataforma de Mensageria

[![Slack](https://img.shields.io/badge/Slack-red.svg)](https://github.com/serverless/serverless)

### 2.1.3 API

[![TTS com Amazon Polly](https://img.shields.io/badge/TTS_Amazon_Polly-v1-e32636.svg)](https://github.com/serverless/serverless)

## 2.1 Destrinchando o funcionamento do sistema

### 2.1.2 Amazon Lex

O **Amazon Lex** é um serviço da AWS para a construção de chatbots inteligentes, com capacidade de conversação por texto ou voz. Neste caso, o chatbot em questão é para uma loja fictícia dos EUA chamada PunkPizza, onde através dele será possível realizar compras de pizzas, hambúrgueres e sobremesas.

### 2.1.2 Amazon Lambda

O **Amazon Lambda** será responsável por fazer a integração do chatbot com a API realizada na parte 1. Ele verificará a intenção que usuário buscou no chat, armazenará os slots e construirá uma frase de confirmação que será convertida em um áudio de arquivo `.mp3` e armazenada no S3 pela API.

### 2.1.3 Slack

O **Slack** é uma das plataformas de mensageria disponíveis na internet que tem a funcionalidade de integração com o Amazon Lex, recebendo mensagens, incorporando response cards e botões de interação.

### 2.1.4 TTS com Amazon Polly

O **TTS com Amazon Polly** é todo o serviço que construímos anteriormente, onde ele é capaz de receber uma frase no corpo de uma requisição **JSON**, convertê-la em áudio com extensão `.mp3`, salvar seus dados em uma tabela NoSQL do DynamoDB e armazenar o arquivo no S3.

### 2.1.5 Lógica do Sistema

O chatbot possui cinco **intents**:

| Intent | Descrição |
| --- | --- |
| ``Greeting`` | Onde o diálogo começa, com uma mensagem de boas vindas. |
| ``PizzaOrder`` | Aqui ocorre todo o processo de pedido da pizza, onde é necessário escolher o tamanho e o sabor da pizza. |
| ``BurgerOrder`` | Aqui ocorre todo o processo de pedido do hambúrguer, onde é necessário escolher o tipo de hambúrguer e o ponto da carne. |
| ``DessertOrder`` | Aqui ocorre todo o processo de pedido da sobremesa, onde é necessário escolher o tipo de sobremesa. |
| ``FallbackIntent`` | É uma intent padrão criada pela AWS, que serve como caminho para quando ocorre um erro nas outras intents. |

E também possui 6 **slots**:

| Slot | Descrição |
| --- | --- |
| ``PizzaSize`` | Oferece diferentes opções de tamanho para a pizza. |
| ``PizzaFlavor`` | Oferece diferentes opções de sabores para a pizza. |
| ``BurgerFlavor`` | Oferece diferentes opções de hambúrgueres. |
| ``SteakDoneness`` | Oferece diferentes opções de pontos para a carne do hambúrguer. |
| ``Dessert`` | Oferece diferentes opções de sobremesa. |
| ``PaymentMethod`` | Ofereçe opções de pagamento em dinheiro ou cartão. |
| ``Address`` | Slot padrão da Amazon para endereços. |

O chatbot consiste em apresentar as opções que a loja oferece (pizzas, hambúrgueres e sobremesas), para então seguir o fluxo com base no que o usuário escolher. As opções variam de acordo com o intent seguido, com a pizza, por exemplo, tendo opções de tamanho e sabor, enquanto a sobremesa só possui o tipo. Ao final, caso o pedido seja confirmado, a *API* é acionada, e a opção de download do áudio é enviada para o usuário.

Veja a arquitetura do sistema:

![post-v3-tts](./assets/arquitetura-chatbot.png)

## 2.3 Como testar o sistema

- Acesse o link de convite do [**workspace**](https://join.slack.com/t/compassuolfalar/shared_invite/zt-2s09z0o43-3L6RLfImJ9JM7yDVrZevjA).
- Navegue até o app **PunkPizza** e interaja com o chatbot!

# Dificuldades Enfrentadas

- Configuração das permissões necessárias para o uso do Amazon Polly, garantindo a segurança e o correto funcionamento do serviço.

- Implementação das condicionais nas intents, com foco na integração harmoniosa entre o backend e as respostas do chatbot.

- Desafios técnicos específicos no uso do Amazon Lambda, relacionados à orquestração e execução das funções.

- Otimização da integração entre o Lambda e o Amazon Lex para garantir uma comunicação eficiente e sem falhas entre os serviços.

# Lições Aprendidas

- Coordenação de Serviços em Nuvem: Foi desafiador, mas aprendemos bastante sobre como conectar diferentes serviços da AWS, como Polly, S3, DynamoDB e Lambda, para criar uma solução completa e funcional. Vimos na prática como esses serviços podem trabalhar juntos e a importância de entender cada um para garantir que tudo funcione bem.

- Uso do Serverless Framework: Descobrimos o quanto o Serverless Framework pode facilitar nossa vida quando se trata de criar e gerenciar recursos na AWS. Aprendemos a usar a ferramenta para fazer deploy de serviços de forma mais simples e rápida, sem precisar configurar tudo manualmente.

- Integração com Inteligência Artificial: Foi uma experiência valiosa entender como integrar nosso backend com o Amazon Lex para criar um chatbot. Percebemos que não é só programar; tem muito a ver com ajustar a lógica e criar uma conversa natural que faça sentido para o usuário.

- Configuração de Permissões: Lidamos com a parte de segurança e permissões na AWS, e percebemos que configurar tudo certo é fundamental para que os serviços funcionem de forma segura. No início, parece complicado, mas depois que pega o jeito, dá pra ver como é importante para manter os dados protegidos.

- Criação de APIs Escaláveis: Tivemos a oportunidade de criar uma API que não só funcionasse, mas que também fosse capaz de lidar com mais usuários e demandas no futuro. Isso nos ensinou bastante sobre como construir sistemas que sejam eficientes e possam crescer junto com as necessidades do projeto.

- Trabalho em Equipe: Aprendemos na prática como é importante dividir as tarefas e manter uma comunicação clara com os colegas. Vimos que quando todo mundo entende o que precisa ser feito e está alinhado, o projeto anda muito melhor.

- Resolução de Problemas com Lambda: Enfrentamos algumas dificuldades para entender e ajustar a lógica do Amazon Lambda, mas isso nos ajudou a desenvolver uma abordagem mais prática para resolver problemas e melhorar a integração entre os serviços.

- Foco na Experiência do Usuário: Descobrimos que não adianta só fazer a parte técnica funcionar; o mais importante é garantir que a experiência do usuário seja agradável. Por isso, nos preocupamos em fazer com que o chatbot e o sistema de conversão de texto em áudio fossem fáceis de usar e intuitivos.

# Autores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Ivo-Aragao">
        <img src="https://avatars.githubusercontent.com/u/105293872?s=96&v=4" width="120" alt="Francisco Ivo">
        <p><strong>Francisco Ivo</strong></p>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/KalylSemi">
        <img src="https://avatars.githubusercontent.com/u/157990287?v=4" width="120" alt="Kalyl Semi">
        <p><strong>Kalyl Semi</strong></p>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/LucasTeodoro1009">
        <img src="https://avatars.githubusercontent.com/u/152567868?s=96&v=4" width="120" alt="Lucas Teodoro">
        <p><strong>Lucas Teodoro</strong></p>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Maxrcus">
        <img src="https://avatars.githubusercontent.com/u/175230930?s=96&v=4" width="120" alt="Marcus Vinicius">
        <p><strong>Marcus Vinicius</strong></p>
      </a>
    </td>
  </tr>
</table>
