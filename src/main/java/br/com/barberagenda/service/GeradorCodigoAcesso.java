package br.com.barberagenda.service;

import java.security.SecureRandom;
import java.util.Locale;

import org.springframework.stereotype.Component;

/**
 * Gera o código de acesso entregue ao cliente quando ele agenda. O código, junto com o e-mail,
 * é exigido para consultar e cancelar o agendamento. É aleatório (SecureRandom) para que não seja
 * possível descobrir agendamentos de outras pessoas testando códigos em sequência.
 * Alfabeto sem caracteres ambíguos (0/O, 1/I/L).
 */
@Component
public class GeradorCodigoAcesso {

    public static final int TAMANHO = 8;
    static final String ALFABETO = "ABCDEFGHJKMNPQRSTUVWXYZ23456789";

    private final SecureRandom aleatorio = new SecureRandom();

    public String gerar() {
        StringBuilder codigo = new StringBuilder(TAMANHO);
        for (int i = 0; i < TAMANHO; i++) {
            codigo.append(ALFABETO.charAt(aleatorio.nextInt(ALFABETO.length())));
        }
        return codigo.toString();
    }

    /** Remove espaços e converte para maiúsculas, aceitando o código digitado em minúsculas. */
    public static String normalizar(String codigo) {
        return codigo == null ? "" : codigo.strip().toUpperCase(Locale.ROOT);
    }
}
