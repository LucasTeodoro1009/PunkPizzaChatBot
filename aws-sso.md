# Configurar o perfil da AWS na máquina

Deixe o *Portal de Acesso da AWS* aberto, precisaremos informações que residem nele.

Para termos um perfil na AWS, precisaremos configurar o *Single Sign-ON, ou *SSO.

1. Digite na linha de comando o seguinte código:

```bash
aws configure sso
```

2. Insira um nome no formaro apresentado.

```bash
SSO session name (Recommended): my-sso
```

3. No *Portal de Acesso da AWS*, copie a URL inicial do SSO e insira neste campo.

```bash
SSO start URL [None]: https://my-sso-portal.awsapps.com/start
```

4. Pressione Enter para manter a região padrão.

```bash
SSO region [None]: us-east-1
```

5. Pressione Enter para manter o escopo padrão.

```bash
SSO registration scopes [None]: sso:account:access
```

7. Você será redirecionado para o navegador, onde será necessário aceitar as permissões impostas pela AWS.

Após isso, novamente no terminal, será preciso completar as configurações de perfil da AWS.

8. Pressione Enter para manter a região padrão.

```bash
SSO region [None]: us-east-1
```

9. Pressione Enter para manter o formato padrão.

```bash
CLI default output format [None]: json
```

10. Digite o nome do seu perfil no padrão apresentado abaixo.

```bash
CLI profile name [AdministratorAccess-905418180021]: my-dev-profile
```

Agora precisaremos configurar a sso-session

11. Digite na linha de comando o seguinte código:

```bash
aws configure sso-session
```

12. Digite o nome da sessão.

```bash
SSO session name: my-sso
```

13. Copie novamente o URL inicial do SSO.

```bash
SSO start URL [None]: https://my-sso-portal.awsapps.com/start
```

14. Pressione Enter para manter a região padrão.

```bash
SSO region [None]: us-east-1
```

15. Pressione Enter para manter o escopo padrão.

```bash
SSO registration scopes [None]: sso:account:access
```

16. Agora, faça o login em uma sessão do IAM Identity Center digitando o comando:

```bash
aws sso login --profile my-dev-profile
```

17. Você será redirecionado para o navegador, onde será necessário aceitar as permissões impostas pela AWS.

18. Para verificar as credenciais, digite:

```bash
aws sts get-caller-identity --profile my-dev-profile
```