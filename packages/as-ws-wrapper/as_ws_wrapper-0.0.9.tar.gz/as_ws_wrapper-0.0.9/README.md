# Accestage Webservice Wrapper
Serviço webservice SOAP oferecido pela Accesstage para 
realizar conectividade de troca de arquivos de transações


# Serviços oferecidos via SOAP
- lista de serviços
- envio de mensagem
- lista de mensagens
- recuperação de mensagem
- confirmação de retirada de mensagem

## Lista de serviços
Cada serviço disponível é um tipo de transação bancária possível de ser realizada.

Cada serviço possui seu identificador mnemônico de tipo de transação.

## Envio de mensagem
Uma mensagem representa uma requisição de transação.

Precisa ter o identificador mnemônico da transação a ser realizada e ter o arquivo com os dados da transação.


## Lista de mensagens
Nessa lista só ficam as mensagens com sucesso?

## Recuperação de mensagem
É o 'retrieve' de uma mensagem específica. Contendo seu status e dados!


## Confirmação de retirada de mensagem
Confirma que tal mensagem foi retirada (serve como ack de um pub/sub consumer?). 

Remove da lista de mensagens essa mensagem com sucesso?


# Referências técnicas
- https://docs.python-zeep.org/en/master/
- https://medium.com/@bkaankuguoglu/how-to-send-soap-requests-in-python-using-zeep-9fd78adb5346
- https://medium.com/@ayushi21095/working-with-soap-based-web-service-using-python-8f532195bc6c
