# prova2-sistemas-distribuidos

roberto conde sato 18/11/26


Situação-problema
Na simulação da Central de Pedidos Distribuídos, três problemas principais precisavam ser resolvidos para garantir o funcionamento correto do sistema:

Limite de processamento simultâneo: era necessário restringir o processamento para no máximo 3 pedidos ao mesmo tempo, evitando sobrecarga por concorrência excessiva.

Falta de sincronização com a réplica: o estoque da réplica não era atualizado conforme o servidor principal, causando divergência de dados entre os nós.

Retorno de erro indevido / falha no fallback: o fluxo de consulta e tratamento apresentava comportamento incorreto mesmo quando o cenário deveria responder com sucesso ou alternar adequadamente para a réplica em caso de falha do principal.
