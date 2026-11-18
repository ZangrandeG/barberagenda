package br.com.barberagenda.exception;

/**
 * Violação de regra de negócio que não depende de outros registros
 * (ex.: horário fora do funcionamento). Convertida em HTTP 400.
 * Quando {@code campo} é informado, aparece no mapa "campos" da resposta de erro.
 */
public class RegraNegocioException extends RuntimeException {

    private final String campo;

    public RegraNegocioException(String mensagem) {
        this(null, mensagem);
    }

    public RegraNegocioException(String campo, String mensagem) {
        super(mensagem);
        this.campo = campo;
    }

    public String getCampo() {
        return campo;
    }
}
