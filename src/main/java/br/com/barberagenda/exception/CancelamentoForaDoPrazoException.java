package br.com.barberagenda.exception;

/** Cancelamento solicitado depois do prazo mínimo (RF-09). Convertida em HTTP 422. */
public class CancelamentoForaDoPrazoException extends RuntimeException {

    public CancelamentoForaDoPrazoException(String mensagem) {
        super(mensagem);
    }
}
