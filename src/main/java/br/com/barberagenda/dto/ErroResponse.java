package br.com.barberagenda.dto;

import java.util.Map;

/**
 * Formato padronizado de erro da API.
 * Exemplo: {"status":400,"erro":"Bad Request","mensagem":"...","campos":{"nome":"..."}}
 * O mapa "campos" é sempre enviado (vazio quando o erro não se refere a campos específicos).
 */
public record ErroResponse(int status, String erro, String mensagem, Map<String, String> campos) {

    public static ErroResponse de(int status, String erro, String mensagem) {
        return new ErroResponse(status, erro, mensagem, Map.of());
    }
}
