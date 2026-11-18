package br.com.barberagenda.exception;

/**
 * Operação em conflito com o estado atual dos dados
 * (ex.: horário já ocupado, e-mail já cadastrado). Convertida em HTTP 409.
 */
public class ConflitoException extends RuntimeException {

    public ConflitoException(String mensagem) {
        super(mensagem);
    }
}
